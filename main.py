import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from mock_data import get_latest_feed
from ai_engine import analyze_crisis_text

app = FastAPI()

# --- ENABLE CORS FOR SECURITY ---
# This permits requests from your Vercel frontend to your Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["https://ignissentry-frontend.vercel.app"] for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("[WARNING]: Supabase configuration credentials are missing!")
    supabase: Client = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/")
def read_root():
    return {"status": "online", "message": "IgnisSentry Ingestion Backend"}


@app.get("/api/incidents")
def get_incidents():
    """
    Fetches list of parsed incidents from Supabase, sorted chronologically.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured.")
    try:
        response = supabase.table("incidents").select("*").order("created_at", desc=True).execute()

        # Wrap the list in the exact structure the Vercel frontend is expecting!
        return {
            "status": "success",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/run-ingestion")
def run_ingestion():
    """
    Parses and ingests incoming raw disaster reports.
    Analyzes them with Gemini structured output and posts them to Supabase.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database client is offline.")

    raw_posts = get_latest_feed()
    saved_records = []

    for post in raw_posts:
        # Run the updated, robust text interpreter
        analysis = analyze_crisis_text(post["text"])

        # Construct the exact database row matching your Supabase table schema
        db_row = {
            "username": post["user"],
            "original_text": post["text"],
            "is_crisis": analysis.is_crisis,
            "category": analysis.category,
            "severity": analysis.severity,
            "location_description": analysis.location_description,
            "summary": analysis.summary,
            "people_affected": analysis.people_affected,
            "status": "Pending"
        }

        try:
            # Write to Supabase table
            response = supabase.table("incidents").insert(db_row).execute()
            saved_records.extend(response.data)
            print(f"[SUCCESS]: Saved row to database: {response.data}")
        except Exception as e:
            print(f"[ERROR]: Failed to write row to Supabase: {e}")
            raise HTTPException(status_code=500, detail=f"Database insertion failed: {e}")

    return {
        "status": "success",
        "processed": len(raw_posts),
        "data": saved_records
    }