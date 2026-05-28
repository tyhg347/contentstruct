"""
ContentStruct MCP Server
=======================
Give AI coding agents (Claude Code, Cursor, Windsurf, etc.)
the ability to browse the web and extract structured content.

Usage:
  python mcp_server/server.py

Then connect any MCP-compatible AI agent to this server.
"""

import sys
import os
import re
from urllib.parse import urlparse

# Add parent directory to path so we can import the scraper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from app.scraper import fetch_url, parse_html, extract_keywords, clean_text

server = Server("contentstruct")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="fetch_webpage",
            description="Fetch a webpage and extract clean, structured content. "
                        "Removes ads, navigation, scripts. Returns title, clean text, "
                        "metadata (word count, author, description).",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full URL to fetch (e.g., https://example.com/article)",
                    },
                },
                "required": ["url"],
            },
        ),
        Tool(
            name="search_webpage",
            description="Search within a webpage's content for specific keywords. "
                        "Returns matching paragraphs with context.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to search within",
                    },
                    "query": {
                        "type": "string",
                        "description": "Keyword or phrase to search for",
                    },
                },
                "required": ["url", "query"],
            },
        ),
        Tool(
            name="extract_keywords",
            description="Extract the most important keywords from a webpage. "
                        "Useful for understanding what a page is about at a glance.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to analyze",
                    },
                    "max_keywords": {
                        "type": "integer",
                        "description": "Maximum number of keywords to return (default 15)",
                        "default": 15,
                    },
                },
                "required": ["url"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    if name == "fetch_webpage":
        url = arguments["url"]
        try:
            html = await fetch_url(url)
            result = parse_html(html, source_url=url)
            content = result["content"]
            title = result.get("title", "")
            meta = result.get("metadata", {})
            keywords = extract_keywords(content)

            # Truncate very long content to fit in context window
            max_chars = 8000
            if len(content) > max_chars:
                content = content[:max_chars] + f"\n\n[... content truncated, original length: {len(content)} chars]"

            response = f"""# {title}

## Content
{content}

## Stats
- Words: {meta.get('word_count', 'N/A')}
- Characters: {meta.get('char_count', 'N/A')}
- Keywords: {', '.join(keywords[:10])}
- Domain: {meta.get('domain', 'N/A')}
"""
            return [TextContent(type="text", text=response.strip())]
        except Exception as e:
            return [TextContent(type="text", text=f"Error fetching {url}: {str(e)}")]

    elif name == "search_webpage":
        url = arguments["url"]
        query = arguments["query"]
        try:
            html = await fetch_url(url)
            result = parse_html(html, source_url=url)
            content = result["content"]
            title = result.get("title", "")

            # Simple search: find paragraphs containing the query
            paragraphs = content.split("\n")
            matches = []
            for i, para in enumerate(paragraphs):
                if query.lower() in para.lower():
                    # Get context: 1 paragraph before and after
                    start = max(0, i - 1)
                    end = min(len(paragraphs), i + 2)
                    context = "\n".join(paragraphs[start:end])
                    matches.append(f"[Match at paragraph {i}]\n{context.strip()}")

            if matches:
                result_text = f"# Search Results for '{query}' in {title}\n\n"
                result_text += "\n---\n".join(matches[:10])
                if len(matches) > 10:
                    result_text += f"\n\n... and {len(matches) - 10} more matches"
                return [TextContent(type="text", text=result_text)]
            else:
                return [TextContent(type="text", text=f"No matches found for '{query}' in {title}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error searching {url}: {str(e)}")]

    elif name == "extract_keywords":
        url = arguments["url"]
        max_kw = arguments.get("max_keywords", 15)
        try:
            html = await fetch_url(url)
            result = parse_html(html, source_url=url)
            content = result["content"]
            title = result.get("title", "")
            keywords = extract_keywords(content, max_keywords=max_kw)

            response = f"# Keywords: {title}\n\n"
            response += f"Top {len(keywords)} keywords:\n"
            for i, kw in enumerate(keywords, 1):
                response += f"  {i}. {kw}\n"

            return [TextContent(type="text", text=response)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error extracting keywords: {str(e)}")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
