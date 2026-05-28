"""Web scraping and content extraction module."""

import re
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


def extract_title(soup: BeautifulSoup) -> str | None:
    """Extract page title from various meta tags."""
    for tag in [
        ("meta", {"property": "og:title"}),
        ("meta", {"name": "twitter:title"}),
        ("title", {}),
        ("h1", {}),
    ]:
        el = soup.find(tag[0], tag[1])
        if el and el.get("content" if tag[0] == "meta" else None):
            return el["content"].strip()
        if el and el.name == "title":
            return el.get_text(strip=True)
        if el and el.name == "h1":
            return el.get_text(strip=True)
    return None


def extract_description(soup: BeautifulSoup) -> str | None:
    """Extract page description from meta tags."""
    for attr_name in ["description", "og:description", "twitter:description"]:
        tag = soup.find("meta", {"name": attr_name}) or soup.find("meta", {"property": attr_name})
        if tag and tag.get("content"):
            return tag["content"].strip()
    return None


def extract_author(soup: BeautifulSoup) -> str | None:
    """Extract author info."""
    for tag in [
        ("meta", {"name": "author"}),
        ("meta", {"property": "article:author"}),
    ]:
        el = soup.find(tag[0], tag[1])
        if el and el.get("content"):
            return el["content"].strip()
    return None


def clean_text(text: str) -> str:
    """Normalize whitespace."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def extract_article_content(soup: BeautifulSoup) -> str:
    """Extract main article content using common article containers."""
    # Try article tag first
    article = soup.find("article")
    if article:
        return article.get_text(separator="\n", strip=True)

    # Try common content containers
    for selector in [
        {"role": "main"},
        {"class": re.compile(r"content|article|post|entry|main")},
        {"id": re.compile(r"content|article|post|entry|main")},
    ]:
        el = soup.find(selector) if isinstance(next(iter(selector.keys())), str) else None

    # Fallback: body text with noise removal
    body = soup.find("body")
    if not body:
        return ""

    # Remove unwanted elements
    for tag in ["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe"]:
        for el in body.find_all(tag):
            el.decompose()

    # Remove hidden elements
    for el in body.find_all(True):
        if el.get("aria-hidden") == "true":
            el.decompose()
        style = el.get("style", "")
        if "display:none" in style or "visibility:hidden" in style:
            el.decompose()

    return body.get_text(separator="\n", strip=True)


async def fetch_url(url: str) -> str:
    """Fetch HTML content from a URL."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.text


def parse_html(html: str, source_url: str | None = None) -> dict:
    """Parse HTML and extract structured content."""
    soup = BeautifulSoup(html, "lxml")

    title = extract_title(soup)
    description = extract_description(soup)
    author = extract_author(soup)
    raw_text = extract_article_content(soup)
    cleaned = clean_text(raw_text)
    domain = urlparse(source_url).netloc if source_url else None
    word_count = len(cleaned.split()) if cleaned else 0
    char_count = len(cleaned) if cleaned else 0

    metadata = {
        "title": title,
        "description": description,
        "author": author,
        "domain": domain,
        "word_count": word_count,
        "char_count": char_count,
        "source": source_url,
    }
    # Remove None values
    metadata = {k: v for k, v in metadata.items() if v is not None}

    return {
        "title": title,
        "content": cleaned,
        "text_length": char_count,
        "metadata": metadata,
    }


def extract_keywords(text: str, max_keywords: int = 10) -> list[str]:
    """Simple keyword extraction from text."""
    words = re.findall(r'\b[a-zA-Z]\w+\b', text.lower())
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "by", "with", "from", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "shall", "can", "need", "dare",
        "this", "that", "these", "those", "it", "its", "they", "them", "their",
        "we", "us", "our", "you", "your", "he", "she", "him", "her", "his",
        "not", "no", "nor", "so", "if", "than", "then", "also", "just", "about",
        "above", "after", "again", "all", "any", "as", "because", "before",
        "between", "both", "each", "few", "more", "most", "other", "some",
        "such", "only", "own", "same", "too", "very", "into", "over", "up",
        "out", "off", "down", "back", "here", "there", "when", "where", "why",
        "how", "what", "which", "who", "whom",
    }
    filtered = [w for w in words if w not in stopwords and len(w) > 2]
    freq: dict[str, int] = {}
    for w in filtered:
        freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: -x[1])
    return [w for w, _ in sorted_words[:max_keywords]]
