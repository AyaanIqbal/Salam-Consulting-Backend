from utils import supabase, gen_uuid
from datetime import datetime, timedelta
import pytz

# Get all active stages
stages_response = supabase.table("stages").select("*").eq("is_active", True).execute()
stages = stages_response.data

now = datetime.now(pytz.utc)
cutoff = now - timedelta(days=14)

for stage in stages:
    entered_at = datetime.fromisoformat(stage["entered_at"])
    
    if entered_at < cutoff:
        customer_id = stage["customer_id"]

        existing = supabase.table("flags")\
            .select("id")\
            .eq("customer_id", customer_id)\
            .eq("flag_type", "blocked")\
            .execute()

        if existing.data:
            print(f"Skipping existing 'blocked' flag for customer: {customer_id}")
            continue

        flag = {
            "id": gen_uuid(),
            "customer_id": customer_id,
            "flag_type": "blocked",
            "notes": f"Stuck in stage {stage['stage_name']} since {entered_at.isoformat()}"
        }

        print(f"Inserting new 'blocked' flag for customer: {customer_id}")
        supabase.table("flags").insert(flag).execute()
