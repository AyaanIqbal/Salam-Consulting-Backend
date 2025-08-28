# wix_test.py
import os, requests
from dotenv import load_dotenv

load_dotenv()

WIX_API_KEY = os.environ["WIX_API_KEY"]
WIX_SITE_ID = os.environ["WIX_SITE_ID"]

BASE = "https://www.wixapis.com"
HEADERS = {
    "Authorization": f"Bearer {WIX_API_KEY}",
    "wix-site-id": WIX_SITE_ID,         # site-level calls
    "Content-Type": "application/json",
}

def _post(url: str, json: dict):
    r = requests.post(url, headers=HEADERS, json=json, timeout=30)
    if r.status_code >= 400:
        raise requests.HTTPError(f"{r.status_code} {r.reason} | {url}\n{r.text}", response=r)
    return r

def _get(url: str):
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code >= 400:
        raise requests.HTTPError(f"{r.status_code} {r.reason} | {url}\n{r.text}", response=r)
    return r

# ---------- Contacts helpers ----------
def _first_email(contact: dict) -> str | None:
    info = contact.get("info") or {}
    if isinstance(info.get("primaryEmail"), str):
        return info["primaryEmail"]
    emails = info.get("emails")
    if isinstance(emails, list) and emails:
        item = emails[0] or {}
        if isinstance(item, dict):
            return item.get("email")
    if isinstance(contact.get("primaryEmail"), str):
        return contact["primaryEmail"]
    return None

# ---------- Orders total helpers ----------
def _money(obj, *path):
    """Safely walk a nested path and return a money dict or number if present."""
    cur = obj
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur

def _total_from_order_payload(o):
    # Common shapes seen in Wix Orders:
    # priceSummary.total.amount / currency
    amt = _money(o, "priceSummary", "total", "amount")
    cur = _money(o, "priceSummary", "total", "currency")
    if amt is not None and cur:
        return float(amt), cur

    # sometimes grandTotal
    amt = _money(o, "priceSummary", "grandTotal", "amount")
    cur = _money(o, "priceSummary", "grandTotal", "currency")
    if amt is not None and cur:
        return float(amt), cur

    # some variants put numeric total directly
    amt = _money(o, "totals", "total")
    cur = o.get("currency") or _money(o, "totals", "currency")
    if amt is not None and cur:
        return float(amt), cur

    # or paymentSummary.totalPaid
    amt = _money(o, "paymentSummary", "totalPaid", "amount")
    cur = _money(o, "paymentSummary", "totalPaid", "currency")
    if amt is not None and cur:
        return float(amt), cur

    return None

def _total_from_transactions(order_id):
    """Fallback: read transactions and sum successful charges/captures."""
    url = f"{BASE}/ecom/v1/order-transactions/{order_id}"
    try:
        data = _get(url).json()
    except requests.HTTPError:
        return None

    # Try common containers
    txs = data.get("transactions") or data.get("payments") or []
    total = 0.0
    currency = None

    for t in txs if isinstance(txs, list) else []:
        # Look for amounts in common fields
        # prefer captured/paid amounts
        status = (t.get("status") or "").lower()
        typ = (t.get("type") or "").lower()
        amount = (
            _money(t, "amount", "amount")
            or _money(t, "amount", "value")
            or t.get("amount")
        )
        cur = _money(t, "amount", "currency") or t.get("currency")

        # Count only successful/paid captures/charges
        if amount is not None and (
            "captur" in status or "paid" in status or "charge" in typ
        ):
            try:
                total += float(amount)
                currency = currency or cur
            except (TypeError, ValueError):
                pass

    if total > 0 and currency:
        return total, currency
    return None

def fetch_recent_orders(limit=10):
    url = f"{BASE}/ecom/v1/orders/search"
    payload = {"cursorPaging": {"limit": limit}, "sort": [{"fieldName": "createdDate", "order": "DESC"}]}
    return _post(url, payload).json().get("orders", [])

def fetch_recent_contacts(limit=10):
    url = f"{BASE}/contacts/v4/contacts/query"
    payload = {"paging": {"limit": limit, "offset": 0}, "sort": [{"fieldName": "createdDate", "order": "DESC"}]}
    return _post(url, payload).json().get("contacts", [])

if __name__ == "__main__":
    print("=== Recent Orders ===")
    for o in fetch_recent_orders():
        total = _total_from_order_payload(o)
        if not total:
            # fallback to transactions endpoint if needed
            total = _total_from_transactions(o.get("id"))
        total_amt, total_cur = (total if total else (None, None))

        print({
            "id": o.get("id"),
            "number": o.get("number"),
            "createdDate": o.get("createdDate"),
            "status": o.get("status"),
            "buyerEmail": (o.get("buyerInfo") or {}).get("email"),
            "total": total_amt,
            "currency": total_cur,
        })

    print("\n=== Recent Contacts ===")
    for c in fetch_recent_contacts():
        info = c.get("info") or {}
        print({
            "id": c.get("id"),
            "name": info.get("name"),
            "email": _first_email(c),
            "createdDate": c.get("createdDate"),
        })
