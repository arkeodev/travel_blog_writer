from typing import List, Optional

from pydantic import BaseModel, Field


class TravelDestination(BaseModel):
    """
    Represents a travel destination with various attributes.
    """

    destination_name: str = Field(..., description="The name of the destination.")
    confidence_score: float = Field(
        ..., description="Confidence score of the identification (0-1)."
    )
    attractions: Optional[List[str]] = Field(
        None, description="Attractions at the destination."
    )
    transportation: Optional[List[str]] = Field(
        None, description="Transportation options to the destination."
    )
    accommodation: Optional[List[str]] = Field(
        None, description="Hotels near the destination."
    )
    restaurants: Optional[List[str]] = Field(
        None, description="Restaurants near the destination."
    )
    description: Optional[str] = Field(
        None, description="Description of the destination."
    )
