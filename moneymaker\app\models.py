from pydantic import BaseModel, Field
from typing import Optional, Any


class ExtractRequest(BaseModel):
    url: Optional[str] = Field(None, description="URL to extract content from")
    text: Optional[str] = Field(None, description="Raw text to process")
    format: str = Field("markdown", description="Output format: markdown, text, json")
    extract_type: str = Field("full", description="What to extract: full, article, metadata")


class ExtractResponse(BaseModel):
    success: bool
    url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    text_length: int = 0
    metadata: dict[str, Any] = {}


class ErrorResponse(BaseModel):
    success: bool = False
    error: str


class UsageRecord(BaseModel):
    api_key: str
    endpoint: str
    timestamp: str
    success: bool
