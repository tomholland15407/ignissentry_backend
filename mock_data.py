# mock_data.py
import random
from datetime import datetime, timezone
from faker import Faker

fake = Faker()

# Real-world styled templates to mimic raw user posts
CRISIS_TEMPLATES = [
    "HELP!!! {hazard} is happening at {location}! We are stuck here, please send emergency teams!",
    "Avoid the {location} intersection. There is a severe {hazard} completely blocking both lanes. Traffic is a nightmare.",
    "A shelter is open at the {shelter_name}. They have {resource} available for those displaced.",
    "Just saw massive {hazard} near {location}. Please be careful and check on your neighbors!",
    "Is anyone else seeing this? The water from the {hazard} is rising fast at {location}."
]

# Non-crisis distractors to test if the Gemini model can ignore noise
NOISE_TEMPLATES = [
    "Just playing some video games today at my house. Weather outside is crazy though. #gametime",
    "Does anyone know if the grocery store near {location} is open today? Need some milk.",
    "Watching the rain fall from my window. Hopefully my commute tomorrow isn't too bad.",
    "My dog really hates this thunder. Hope everyone is staying dry tonight."
]

HAZARDS = ["flooding", "downed power lines", "wildfire", "landslide", "severe sinkhole"]
RESOURCES = ["extra blankets and warm soup", "first aid supplies", "power generators and fresh water"]
SHELTER_NAMES = ["Community Sports Complex", "Downtown High School Gym", "Eastside Civic Center"]


def generate_single_event():
    """Generates a single, randomized post with realistic keys."""
    # 75% chance of crisis, 25% chance of non-crisis noise
    if random.random() < 0.75:
        hazard = random.choice(HAZARDS)
        location = f"{fake.street_name()} near the {fake.company()}"
        shelter = random.choice(SHELTER_NAMES)
        resource = random.choice(RESOURCES)

        text = random.choice(CRISIS_TEMPLATES).format(
            hazard=hazard,
            location=location,
            shelter_name=shelter,
            resource=resource
        )
    else:
        location = f"{fake.street_name()}"
        text = random.choice(NOISE_TEMPLATES).format(location=location)

    return {
        "user": f"@{fake.user_name()}",
        "text": text,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def get_latest_feed():
    """
    Simulates fetching a dynamic batch of 4 real-time messages from the internet.
    Kept small (4 items) to respect Gemini API rate limits and keep execution fast!
    """
    return [generate_single_event() for _ in range(4)]