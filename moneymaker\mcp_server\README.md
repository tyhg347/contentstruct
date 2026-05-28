# ContentStruct MCP — Give AI Agents the Power to Browse the Web

让你的 AI 编程助手（Claude Code、Cursor、Windsurf）直接浏览网页、提取内容、分析关键词。

## ✨ Agents Can Now...

- **Fetch any webpage** — Read articles, docs, and get clean text (no ads/scripts)
- **Search within pages** — Find specific info on any URL
- **Extract keywords** — Understand what a page is about at a glance

## 🚀 Quick Start

### Claude Code / Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "contentstruct": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/contentstruct"
    }
  }
}
```

### Cursor

In Cursor settings → MCP Servers → Add:

| Field | Value |
|-------|-------|
| Name | contentstruct |
| Type | command |
| Command | `python -m mcp_server.server` |
| Working Dir | `/path/to/contentstruct` |

### VS Code + Continue.dev

Add to your Continue config:

```json
{
  "experimental": {
    "mcpServers": {
      "contentstruct": {
        "command": "python",
        "args": ["-m", "mcp_server.server"],
        "cwd": "/path/to/contentstruct"
      }
    }
  }
}
```

## 🔧 Available Tools

| Tool | Description |
|------|-------------|
| `fetch_webpage` | Fetch URL → clean text + metadata + keywords |
| `search_webpage` | Search within a page for specific terms |
| `extract_keywords` | Extract top keywords from any URL |

## 💰 Why This Is Valuable

AI coding agents are powerful but **can't browse the web natively**. This MCP server gives them that ability:

- 🧠 Claude/Cursor can read documentation, examples, and tutorials
- 🔍 Research competitors, APIs, and libraries in real-time  
- 📚 Fetch and analyze content during coding sessions
- 🤖 Fully autonomous web research for your AI agent

## 📦 Deployment

```bash
pip install mcp httpx beautifulsoup4 lxml
python mcp_server/server.py
```

The server communicates over stdio (standard MCP protocol). No ports to open, no internet required for self-hosted use.
