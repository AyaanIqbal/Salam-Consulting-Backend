import pandas as pd
import uuid
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_API_KEY")

# strip accidental quotes/whitespace
def _clean(v: str | None) -> str:
    return (v or "").strip().strip('"').strip("'")

supabase_url = _clean(os.getenv("SUPABASE_URL"))
supabase_key = _clean(os.getenv("SUPABASE_SERVICE_ROLE_API_KEY"))

# Helpful validation
if not supabase_url.startswith("https://") or ".supabase.co" not in supabase_url:
    raise RuntimeError(f"SUPABASE_URL looks wrong: {supabase_url!r}")
if not supabase_key:
    raise RuntimeError("SUPABASE_SERVICE_ROLE_API_KEY is missing/empty")

supabase: Client = create_client(supabase_url, supabase_key)

def load_orders_csv():
    return pd.read_csv("Orders.csv")

est = pytz.timezone("US/Eastern")
def get_created_at(row):
    try:    
        full_str = f"{row['Date created']} {row['Time']}"
        dt = datetime.strptime(full_str, "%b %d, %Y %I:%M:%S %p")
        return est.localize(dt).astimezone(pytz.utc)
    except Exception:
        return None

def gen_uuid():
    return str(uuid.uuid4())


def isoformat_timestamp(val):
    if isinstance(val, pd.Timestamp):
        return val.isoformat()
    elif isinstance(val, datetime):
        return val.astimezone(pytz.utc).isoformat()
    return val

def get_email_to_customer_id():
    res = supabase.table("customers").select("id,email").execute()
    records = res.data or []
    return {record["email"]: record["id"] for record in records}