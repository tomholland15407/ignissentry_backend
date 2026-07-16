# ai_engine.py (Production Build with Structured Google Gen AI SDK)
import os
import logging
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Literal

# Configure standard logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 1. DEFINE STRUTURED SCHEMA FOR CRISIS DISPATCHING
class CrisisInsights(BaseModel):
    is_crisis: bool = Field(
        description="Set to True only if this text is an active, real-time emergency (e.g. floods, fires, accidents, active physical danger). Set to False for normal traffic updates, weather forecasts, spam, or general commentary.")
    category: Literal["Flood", "Fire", "Earthquake", "Infrastructure", "Medical", "Other"] = Field(
        description="The primary category of the emergency.")
    severity: Literal["Critical", "High", "Medium", "Low"] = Field(
        description="The priority rating of the threat level to human life or structures.")
    location_description: str = Field(
        description="Extract any location identifiers (e.g. '4th avenue near the bakery'). If none are listed, return 'Unknown'.")
    summary: str = Field(description="A concise, single-sentence dispatch summary of what is happening.")
    people_affected: int = Field(
        description="Estimated count of people in immediate danger. If a family or 'two kids' are mentioned, estimate accordingly. Default to 1.")


# 2. RESOLVE ACCESS KEY
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def process_crisis_text(text: str) -> CrisisInsights:
    """
    Ingests text, processes it live with Google Gemini, and returns structured insights.
    Gracefully falls back to local simulation if no cloud key is found.
    """
    if not API_KEY:
        logger.warning("[WARNING]: API Key not found. Running local fallback simulator mode.")
        # Safety Mock Logic to keep the hackathon app demo working offline
        is_crisis = any(word in text.lower() for word in ["help", "water", "fire", "trapped"])
        return CrisisInsights(
            is_crisis=is_crisis,
            category="Flood" if "water" in text.lower() else "Other",
            severity="Critical" if "help" in text.lower() else "Medium",
            location_description="4th avenue near the old bakery" if is_crisis else "Unknown",
            summary="Stranded on roof with two children due to flood waters." if is_crisis else "General commentary.",
            people_affected=4 if is_crisis else 1
        )

    try:
        # Initialize the GenAI Client (natively picks up GEMINI_API_KEY from environment)
        client = genai.Client()

        # Dispatch structured query to Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # Or use 'gemini-1.5-flash' depending on your tier
            contents=f"Analyze this raw incoming feed text: '{text}'",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",  # Restrict model to valid JSON
                response_schema=CrisisInsights,  # Force formatting to match Pydantic
                system_instruction="You are an emergency crisis response dispatcher. Categorize the input efficiently to assist responders."
            )
        )

        # The modern SDK automatically parses the JSON directly back into our Pydantic object!
        insights: CrisisInsights = response.parsed
        return insights

    except Exception as e:
        logger.error(f"[ERROR]: Gemini API dispatch failed: {e}. Reverting to fallback.", exc_info=True)
        # Prevent API blockages or crashes from breaking database ingestion pipeline
        return CrisisInsights(
            is_crisis=True,
            category="Other",
            severity="Medium",
            location_description="Failed to parse due to connection issues",
            summary="System connection error fallback.",
            people_affected=1
        )