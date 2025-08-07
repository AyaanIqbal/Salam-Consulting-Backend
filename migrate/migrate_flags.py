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

        # Optional: check for existing flag to avoid duplicates
        existing = supabase.table("flags")\
            .select("id")\
            .eq("customer_id", customer_id)\
            .eq("flag_type", "blocked")\
            .execute()

        if not existing.data:
            flag = {
                "id": gen_uuid(),
                "customer_id": customer_id,
                "flag_type": "blocked",
                "notes": f"Stuck in stage {stage['stage_name']} since {entered_at.isoformat()}"
            }
            print(f"Inserting flag: {flag}")
            supabase.table("flags").insert(flag).execute()
