import pandas as pd
from utils import supabase, load_orders_csv, get_created_at, gen_uuid, isoformat_timestamp

df = load_orders_csv()

# customers table
customers = df[[
    "Contact email",
    "Billing name",
    "Billing phone",
]].copy()

customers.columns = ["email", "name", "phone"]
customers = customers.drop_duplicates(subset="email")

customers["id"] = [gen_uuid() for i in range(len(customers))]

df["created_at"] = df.apply(get_created_at, axis=1)
email_to_created_at = df.groupby("Contact email")["created_at"].min().to_dict()
customers["created_at"] = customers["email"].map(email_to_created_at)

for i, row in customers.iterrows():
    cleaned_row = {
        key: (None if pd.isna(val) else isoformat_timestamp(val)) for key, val in row.to_dict().items()
    }
    print(cleaned_row)
    supabase.table("customers").insert(cleaned_row).execute()

