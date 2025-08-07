import pandas as pd
from utils import supabase, load_orders_csv, get_created_at, gen_uuid, isoformat_timestamp, get_email_to_customer_id

df = load_orders_csv()

stage_map = {
    "Resume Review": "resume_review",
    "Resume Rebuild": "resume_review",
    "Resume & Career Coaching": "career_coaching",
    "Resume and Career Coaching": "career_coaching",
    "Career Coaching": "career_coaching",
    "Discovery Call": "discovery_call",
    "Interview Critique": "interview_prep",
    "Resume Review + Interview Critique": "interview_prep",
    "Technical Interview": "interview_prep",
    "Mock Interview": "interview_prep",
    "Career Coaching + Interview Critique": "interview_prep",
    "PM Coaching": "custom_service",
    "Life Coaching": "custom_service",
    "Resume & PM Coaching": "custom_service",
    "Custom Service": "custom_service"
}

# Select columns from public.orders
orders = df[[
    "Order number",
    "Contact email",
    "Item",
    "Date created",
    "Time"
]].copy()

# clean columns
orders.columns = ["order_number", "email", "item", "date", "time"]
orders = orders.drop_duplicates(subset="order_number")

email_to_customer_id = get_email_to_customer_id()
orders["customer_id"] = orders["email"].map(email_to_customer_id)

# drop orders with no matching customer
orders = orders.dropna(subset=["customer_id"])

orders["created_at"] = df.apply(get_created_at, axis=1)

for i, row in orders.iterrows():
    stage_name = stage_map.get(row["item"], "custom_service")

    stage_row = {
        "id": gen_uuid(),
        "customer_id": row["customer_id"],
        "stage_name": stage_name,
        "entered_at": isoformat_timestamp(row["created_at"]),
        "is_active": True
    }

    print(stage_row)
    supabase.table("stages").insert(stage_row).execute()
