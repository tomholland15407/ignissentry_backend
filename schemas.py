# schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class StructuredEmergency(BaseModel):
    is_crisis: bool = Field(description="Set to True if the text represents an actual emergency or safety risk. Set to False if it is noise, chatter, or irrelevant.")
    category: str = Field(description="Must be one of: 'Flood', 'Fire', 'Medical', 'Blocked Road', 'Resource Offer', or 'Irrelevant'.")
    severity: str = Field(description="Must be one of: 'Critical', 'Moderate', 'Low', or 'None'.")
    location_description: Optional[str] = Field(None, description="The descriptive landmark, street name, or location mentioned in text.")
    summary: str = Field(description="A clean, concise 10-word summary of the core emergency situation.")
    people_affected_estimate: int = Field(default=1, description="Estimated number of people in immediate danger. Defaults to 1 if unknown.")