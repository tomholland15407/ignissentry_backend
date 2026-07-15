# main.py (Final Assembly Engine)
from fastapi import FastAPI, HTTPException
import mock_data
from ai_engine import process_crisis_text
import database

app = FastAPI(title="IgnisSentry Engine Core v1.0")


@app.get("/")
def read_root():
    return {"status": "online", "system": "IgnisSentry Engine Engine Core Core Framework"}


@app.post("/api/run-ingestion")
def run_ingestion_pipeline():
    """
    Triggers ingestion: processes raw data feeds, runs AI extraction,
    and archives valid crisis events automatically into Supabase.
    """
    raw_posts = mock_data.get_latest_feed()
    ingested_count = 0

    for post in raw_posts:
        # Step 1: Run through the AI classification layer
        ai_insights = process_crisis_text(post["text"])

        # Step 2: Safety Check. If it's not a real crisis, skip it to save space!
        if not ai_insights.is_crisis:
            continue

        # Step 3: Write out to our persistent remote SQL engine
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
    """Fetches our active structural incident data feeds directly from our live cloud database."""
    records = database.fetch_all_incidents()
    return {"status": "success", "count": len(records), "data": records}