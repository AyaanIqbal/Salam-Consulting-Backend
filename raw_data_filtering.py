from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_api_key = os.getenv("SUPABASE_SERVICE_ROLE_API_KEY")

supabase: Client = create_client(supabase_url, supabase_api_key)

df = pd.read_csv("Orders.csv")

print(df)