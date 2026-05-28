"""ContentStruct API - Turn messy web content into structured data."""

import sys
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware

from .models import ExtractRequest, ExtractResponse, ErrorResponse
from .scraper import fetch_url, parse_html, extract_keywords
from .auth import verify_key, record_usage, init_default_keys, get_usage_report


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create default keys
    init_default_keys()
    yield


app = FastAPI(
    title="ContentStruct API",
    description="Turn any URL or text into clean, structured data. Built for researchers, analysts, and AI apps.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def auth_dependency(x_api_key: str = Header(None, alias="X-API-Key")):
    """Validate API key from header."""
    record = verify_key(x_api_key)
    if not record:
        raise HTTPException(status_code=401, detail=ErrorResponse(error="Invalid or missing API key").model_dump())
    # Check usage limits
    if record.get("usage_this_month", 0) >= record.get("monthly_limit", 100):
        raise HTTPException(status_code=429, detail=ErrorResponse(error="Monthly usage limit exceeded").model_dump())
    return x_api_key


@app.get("/")
def root():
    return {
        "name": "ContentStruct API",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "POST /extract": "Extract content from a URL or raw text",
            "GET /usage": "Check your API usage and limits",
        }
    }


@app.post("/extract", response_model=ExtractResponse)
async def extract(
    request: ExtractRequest,
    api_key: str = Depends(auth_dependency),
):
    """Extract structured content from a URL or raw text.

    Provide either a `url` to scrape, or `text` to process directly.
    Returns cleaned content, title, metadata, and stats.
    """
    try:
        if request.url:
            # Scrape a URL
            html = await fetch_url(request.url)
            result = parse_html(html, source_url=request.url)
            record_usage(api_key, "extract", True)
            return ExtractResponse(
                success=True,
                url=request.url,
                title=result["title"],
                content=result["content"],
                text_length=result["text_length"],
                metadata=result["metadata"],
            )

        elif request.text:
            # Process raw text directly
            from .scraper import clean_text
            cleaned = clean_text(request.text)
            word_count = len(cleaned.split())
            char_count = len(cleaned)

            result = ExtractResponse(
                success=True,
                content=cleaned,
                text_length=char_count,
                metadata={
                    "word_count": word_count,
                    "char_count": char_count,
                    "keywords": extract_keywords(cleaned),
                },
            )
            record_usage(api_key, "extract", True)
            return result

        else:
            raise HTTPException(status_code=400, detail=ErrorResponse(error="Provide either 'url' or 'text'").model_dump())

    except HTTPException:
        raise
    except Exception as e:
        record_usage(api_key, "extract", False)
        raise HTTPException(status_code=500, detail=ErrorResponse(error=str(e)).model_dump())


@app.get("/usage")
def usage(api_key: str = Depends(auth_dependency)):
    """Get your API usage statistics and plan limits."""
    return get_usage_report(api_key)
