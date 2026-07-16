import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from mock_data import get_prompt_for_post


# Define the structured output Pydantic schema
class CrisisIncidentAnalysis(BaseModel):
    is_crisis: bool = Field(
        description="True if this is an active emergency or safety request. False for casual chat/memes."
    )
    category: str = Field(
        description="Crisis category. Must be one of: Flood, Fire, Earthquake, Severe Weather, Medical, Shelter, Other."
    )
    severity: str = Field(
        description="Severity level. Must be one of: Low, Medium, High."
    )
    location_description: str = Field(
        description="Landmarks, intersections, or addresses mentioned. Set to 'Unknown' if unspecified."
    )
    summary: str = Field(
        description="A clear 1-sentence summary of what is happening."
    )
    people_affected: int = Field(
        description="Estimated number of individuals in danger or stranded. Default to 1."
    )


def analyze_crisis_text(text: str) -> CrisisIncidentAnalysis:
    """
    Connects to the official Google GenAI SDK to categorize data.
    Falls back to a local parser if the key is invalid or blocked.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[WARNING]: GEMINI_API_KEY is missing. Utilizing backup parser.")
        return get_local_fallback_analysis(text)

    try:
        # Initialize client (will automatically load GEMINI_API_KEY from environment)
        client = genai.Client()

        # Build prompt using the template in mock_data.py
        prompt_text = get_prompt_for_post(text)

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_text,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CrisisIncidentAnalysis,
                temperature=0.1,  # Low temperature guarantees consistent categorization
            ),
        )

        # Parse output safely into the Pydantic structure
        analysis = CrisisIncidentAnalysis.model_validate_json(response.text)
        return analysis

    except Exception as e:
        print(f"[ERROR]: Google Gemini API failed with error: {e}")
        return get_local_fallback_analysis(text)


def get_local_fallback_analysis(text: str) -> CrisisIncidentAnalysis:
    """
    A smart local keyword fallback to keep your map working even when the API is offline.
    """
    text_lower = text.lower()

    # Check if crisis
    is_crisis = any(word in text_lower for word in
                    ["help", "flood", "water", "rescue", "roof", "blocked", "trapped", "danger", "fire", "sparking"])

    # Simple rule categorization
    category = "Other"
    if any(word in text_lower for word in ["water", "flood", "boat", "roof"]):
        category = "Flood"
    elif any(word in text_lower for word in ["tree", "traffic", "road", "block", "weather"]):
        category = "Severe Weather"
    elif any(word in text_lower for word in ["shelter", "blanket", "food"]):
        category = "Shelter"
    elif any(word in text_lower for word in ["power", "spark", "fire", "wire"]):
        category = "Fire"

    # Severity detection
    severity = "Low"
    if is_crisis:
        severity = "High" if any(word in text_lower for word in ["help", "roof", "trapped", "danger"]) else "Medium"

    # Location approximation
    location = "Unknown"
    if "4th avenue" in text_lower:
        location = "4th Avenue near old bakery"
    elif "highway" in text_lower:
        location = "Downtown Highway Intersection"
    elif "sports complex" in text_lower:
        location = "Community Sports Complex"
    elif "elm street" in text_lower:
        location = "Elm Street near Public Library"

    return CrisisIncidentAnalysis(
        is_crisis=is_crisis,
        category=category,
        severity=severity,
        location_description=location,
        summary=f"[Local AI Fallback] {text[:50]}...",
        people_affected=4 if "kids" in text_lower else 1
    )