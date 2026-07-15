# ai_engine.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from schemas import StructuredEmergency

# Load keys from the secret .env file safely
load_dotenv()

# Initialize the OpenAI web client manager
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def process_crisis_text(raw_text: str) -> StructuredEmergency:
    """
    Sends raw text to OpenAI using Structured Outputs,
    forcing the AI model to conform exactly to our Pydantic schema.
    """
    # Fallback simulation if you do not have an active OpenAI API Key yet
    if not api_key or api_key.startswith("your_"):
        print("[WARNING]: API Key not found. Running local fallback simulator mode.")
        if "HELP" in raw_text.upper():
            return StructuredEmergency(
                is_crisis=True,
                category="Flood",
                severity="Critical",
                location_description="4th avenue near the old bakery",
                summary="Stranded on roof with two children due to flood waters.",
                people_affected_estimate=4
            )
        return StructuredEmergency(
            is_crisis=False,
            category="Irrelevant",
            severity="None",
            location_description=None,
            summary="General non-emergency chatter or noise.",
            people_affected_estimate=0
        )

    try:
        # Call the OpenAI API using structured data parsing tools
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",  # Highly cost-efficient, blazing fast model ideal for hackathons
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert emergency dispatch coordinator AI. Extract structured data from chaotic public disaster reports."
                },
                {
                    "role": "user",
                    "content": raw_text
                }
            ],
            response_format=StructuredEmergency, # This binds OpenAI directly to our Pydantic guardrail schema!
        )
        return response.choices[0].message.parsed
    except Exception as e:
        print(f"Error calling OpenAI API pipeline: {e}")
        # Return a fallback safe record so our backend doesn't crash mid-demo
        return StructuredEmergency(
            is_crisis=False,
            category="Error",
            severity="None",
            summary="Failed to parse text due to system exception errors.",
            people_affected_estimate=0
        )