from typing import Literal

from pydantic import BaseModel, Field


class SentimentResponse(BaseModel):
    """
    Expected structured response from Gemini.
    """

    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="Overall sentiment of the customer review."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1."
    )

    reason: str = Field(
        description="Short explanation for the sentiment classification."
    )