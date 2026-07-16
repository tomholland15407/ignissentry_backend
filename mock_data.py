# mock_data.py

# A list of dictionaries representing raw, chaotic social media posts during a disaster
RAW_FEED = [
    {
        "user": "@rescue_now_99",
        "text": "HELP!!! Water is coming inside my house on 4th avenue near the old bakery! We are on the roof with two kids. Please send a boat!",
        "timestamp": "2026-07-14T20:45:00Z"
    },
    {
        "user": "@weather_watcher",
        "text": "Avoid the downtown highway intersection. A massive tree fell and completely blocked both lanes. Traffic is totally dead.",
        "timestamp": "2026-07-14T20:46:12Z"
    },
    {
        "user": "@food_bank_volunteer",
        "text": "We have successfully set up a shelter at the Community Sports Complex. We have extra blankets and water bottles if anyone needs them.",
        "timestamp": "2026-07-14T20:48:00Z"
    },
    {
        "user": "@troll_face42",
        "text": "Wow, school is canceled tomorrow! Time to play video games all day long long long. #hurricane",
        "timestamp": "2026-07-14T20:50:00Z"
    },
    {
        "user": "@citizen_safeguard",
        "text": "Live power lines are down on Elm Street right outside the public library! Sparking heavily, very dangerous situation.",
        "timestamp": "2026-07-14T20:52:00Z"
    }
]


def get_latest_feed():
    """
    Simulates fetching real-time messages from a raw social media disaster feed.
    """
    return RAW_FEED


def get_prompt_for_post(post_text: str) -> str:
    """
    Constructs a detailed instruction prompt to guide Gemini's classification engine.
    """
    return f"""
    You are an emergency dispatch AI parsing raw social media feeds during natural disasters.
    Analyze the user post below and extract precise structured incident data.

    User Post:
    "{post_text}"

    Extraction Guidelines:
    1. 'is_crisis': Set to True if there is a real-world hazard, danger, or request for rescue. Set to False for casual discussion, memes, or chat.
    2. 'category': Must be exactly one of: 'Flood', 'Fire', 'Earthquake', 'Severe Weather', 'Medical', 'Shelter', or 'Other'.
    3. 'severity': Must be 'High' (immediate danger to life), 'Medium' (infrastructure blocks, active hazards), or 'Low' (announcements, non-urgent information).
    4. 'location_description': The precise street, landmark, or area mentioned. Set to 'Unknown' if not mentioned.
    5. 'people_affected': The number of people mentioned as in danger. For instance, "We and two kids" means 4. Default to 1 if unspecified.
    """