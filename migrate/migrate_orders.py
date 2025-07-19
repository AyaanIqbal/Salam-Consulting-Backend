import pandas as pd
from utils import supabase, load_orders_csv, get_created_at, gen_uuid, isoformat_timestamp, get_email_to_customer_id

df = load_orders_csv()

orders = df[[
    "Order number",
    "Contact email",
    "Item",
    "Price",
    "Date created",
    "Time"
]].copy()

orders.columns = ["order_number", "email", "item", "price", "date", "time"]

orders = orders.drop_duplicates(subset="order_number")

email_to_customer_id = get_email_to_customer_id()

orders["customer_id"] = orders["email"].map(email_to_customer_id)

orders = orders.dropna(subset=["customer_id"])

orders["id"] = [gen_uuid() for _ in range(len(orders))]
orders["created_at"] = df.apply(get_created_at, axis=1)

for i, row in orders.iterrows():
    cleaned_row = {
        j: (
            None if pd.isna(k)
            else float(k) if j == "price"
            else isoformat_timestamp(k) if j == "created_at"
            else int(k) if j == "order_number"
            else k
        )
        for j, k in row[["id", "order_number", "customer_id", "item", "price", "created_at"]].to_dict().items()
    }

    print(cleaned_row)
    supabase.table("orders").insert(cleaned_row).execute()