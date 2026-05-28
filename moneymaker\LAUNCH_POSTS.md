# LAUNCH POSTS

---

## 🐍 HN Post (Hacker News)

**Title:** Show HN: I built an MCP server that gives Claude Code/Cursor web browsing ability

**Body:**

MCP (model context protocol) is great, but most MCP servers are toys. I wanted something practical.

ContentStruct is an MCP server + REST API that lets any AI agent (Claude Code, Cursor, Claude Desktop, any MCP client) fetch web pages, search content, and extract keywords.

**3 tools:**
- fetch_webpage — get clean text from any URL (no ads/scripts)
- search_webpage — find specific content within a page
- extract_keywords — understand what a page is about instantly

**Stack:** Python, FastAPI, BeautifulSoup4, MCP SDK

**Why it's useful:** AI coding agents are powerful but can't browse the web. Now they can read docs, check APIs, and research on the fly.

**Source:** [GitHub link]
**Demo:** `python mcp_server/server.py` + connect Claude/Cursor

Open source / source available. Happy to answer questions.

---

## 🔴 Reddit r/MCP

**Title:** Built an MCP server for web browsing — fetch_webpage, search, keyword extraction

**Body:**

Hey all, I built ContentStruct — an MCP server that gives AI agents real web access. It works with Claude Desktop, Claude Code, Cursor, Continue.dev, and any MCP-compatible client.

**3 tools:**
- `fetch_webpage(url)` → clean text, metadata, word count
- `search_webpage(url, query)` → find specific content
- `extract_keywords(url)` → get top keywords

**Setup is 2 minutes:**
```json
"contentstruct": {
  "command": "python",
  "args": ["-m", "mcp_server.server"],
  "cwd": "/path/to/contentstruct"
}
```

Technologies: Python, FastAPI, httpx, BeautifulSoup4.

Happy to share the source — let me know what you think!

---

## 🔴 Reddit r/SideProject

**Title:** I made a tool that gives AI agents web browsing — $49 one-time, self-hosted

**Body:**

I built ContentStruct — an MCP server + REST API that lets Claude, Cursor, and any MCP client browse the web.

It does 3 things:
1. Fetches any URL and returns clean text (no ads, nav, scripts)
2. Searches within pages for specific keywords
3. Extracts topic keywords from any page

I'm selling it as a source code package for $49 (one-time, self-hosted) because I think MCP tools should be a one-time purchase, not another subscription.

Includes: MCP server, REST API, Docker support, deployment guides for Railway/Fly.io, landing page template.

Is $49 a fair price? Would you buy this?

---

## 📢 X/Twitter Thread

**Tweet 1:**
Your AI coding agent is blind. It can't browse the web, read docs, or check APIs.

Until now.

I built ContentStruct — an MCP server that lets Claude Code/Cursor actually use the web.

**Tweet 2:**
3 tools:
• fetch_webpage → clean text from any URL
• search_webpage → find keywords in a page
• extract_keywords → understand content at a glance

**Tweet 3:**
Works with:
• Claude Desktop
• Claude Code  
• Cursor
• Windsurf
• Continue.dev
• Any MCP-compatible AI

Setup: 2 minutes. Self-hosted. Your data stays yours.

**Tweet 4:**
Built with Python + FastAPI + BeautifulSoup4.

Source available for $49 one-time (no subscriptions).

Who wants web-browsing AI agents? 👇

---

## 🇨🇳 V2EX 发帖

**标题：** 让你的 Claude/Cursor 能上网 — 我写了个 MCP 浏览器工具

**正文：**

AI 编程助手（Claude Code、Cursor 等）很强，但有个致命缺陷：**上不了网**。它们看不到文档、查不了 API、没法搜索。

所以我写了个 MCP Server，让 AI 能浏览网页。

**3 个工具：**
- fetch_webpage — 抓取网页，自动去广告去脚本，返回干净文本
- search_webpage — 在网页里搜索关键词
- extract_keywords — 提取网页核心关键词

**支持的客户端：**
- Claude Desktop / Claude Code
- Cursor
- Windsurf
- Continue.dev
- 任何支持 MCP 协议的 AI

**技术栈：** Python + FastAPI + BeautifulSoup4

**定价：** 买断制 $49（约 ¥349），自部署，不限使用次数

感兴趣吗？想问问大家觉得这价格怎么样？

---

## 🇨🇳 即刻/小红书

**标题：** 让你的 Claude 能上网！MCP 浏览器工具分享

**正文：**
做 AI 开发的应该都知道，Claude Code 虽然强但上不了网。
写个 MCP Server 解决了这个问题，分享给大家～

功能：
✅ 抓取网页（自动去广告）
✅ 搜索页面内容
✅ 提取关键词

支持 Claude、Cursor 等主流 AI 客户端。
源码买断 ¥349，自部署无限制。

大家觉得有用吗？
