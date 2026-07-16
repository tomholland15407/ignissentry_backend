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
    }
]

def get_latest_feed():
    """Simulates fetching real-time messages from a data pipeline."""
    return RAW_FEED