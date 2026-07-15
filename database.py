# database.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variable secrets
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# Initialize our connection manager instance to communicate with cloud database
supabase: Client = create_client(url, key)

def insert_incident(username: str, original_text: str, ai_insights: dict):
    """Inserts a single structured incident entry record into our Supabase database table."""
    try:
        data, count = supabase.table("incidents").insert({
            "username": username,
            "original_text": original_text,
            "is_crisis": ai_insights.get("is_crisis"),
            "category": ai_insights.get("category"),
            "severity": ai_insights.get("severity"),
            "location_description": ai_insights.get("location_description"),
            "summary": ai_insights.get("summary"),
            "people_affected": ai_insights.get("people_affected_estimate", 1),
            "status": "Pending"
        }).execute()
        print(f"[SUCCESS]: Logged data row item entry sequence: {data}")
        return data
    except Exception as e:
        print(f"[DATABASE ERROR]: Writing sequence failed: {e}")
        return None

def fetch_all_incidents():
    """Queries and returns all recorded entries inside our table database ordered by entry time."""
    try:
        response = supabase.table("incidents").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"[DATABASE ERROR]: Read sequence failed: {e}")
        return []