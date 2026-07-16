# main.py (Cleaned & Streamlined Production Build)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mock_data
from ai_engine import process_crisis_text
import database

app = FastAPI(title="IgnisSentry Engine Core v1.0")

# --- 1. MIDDLEWARE FIRST (Perfect Order!) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Unlocks access for localhost, Vercel, and mobile testing
    allow_credentials=False,   # Required by browsers when using the "*" wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. ENDPOINTS SECOND ---
@app.get("/")
def read_root():
    return {"status": "online", "system": "IgnisSentry Engine Core Framework"}


@app.post("/api/run-ingestion")
def run_ingestion_pipeline():
    """
    Triggers ingestion: processes raw data feeds, runs AI extraction,
    and archives valid crisis events automatically into Supabase.
    """
    raw_posts = mock_data.get_latest_feed()
    ingested_count = 0

    for post in raw_posts:
        ai_insights = process_crisis_text(post["text"])

        if not ai_insights.is_crisis:
            continue

        database.insert_incident(
            username=post["user"],
            original_text=post["text"],
            ai_insights=ai_insights.model_dump()
        )
        ingested_count += 1

    return {
        "status": "completed",
        "messages_analyzed": len(raw_posts),
        "critical_incidents_logged": ingested_count
    }


@app.get("/api/incidents")
def get_stored_incidents():
    records = database.fetch_all_incidents()
    return {"status": "success", "count": len(records), "data": records}