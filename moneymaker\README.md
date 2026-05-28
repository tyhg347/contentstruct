# ContentStruct API — Turn Any URL Into Clean Data

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**内容抓取 + 结构化输出，一条 API 搞定。** 给任意 URL 或文本，返回干净的结构化数据 + 智能摘要。

适用于：调研、竞品分析、AI 训练数据准备、内容聚合。

---

## ✨ 功能

- **URL 抓取** — 自动提取文章正文，去噪（跳过 nav/script/广告）
- **纯文本处理** — 清洗、关键词提取、字数统计
- **元数据提取** — title、description、author、word count
- **API Key 鉴权** — 内置简单的计费+用量追踪
- **一键部署** — FastAPI 应用，Python 3.12+

## 🚀 快速开始

### 本地运行

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

首次启动会自动生成 API Key，保存在 `data/api_keys.json`。

### 使用示例

```python
import requests

API_KEY = "cs_你的key"
API_URL = "http://localhost:8000/extract"

# 抓取网页
resp = requests.post(API_URL, json={"url": "https://example.com/article"}, headers={
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
})
print(resp.json())

# 处理文本
resp = requests.post(API_URL, json={"text": "你的原始文本..."}, headers={
    "X-API-Key": API_KEY,
})
print(resp.json())
```

### 查用量

```bash
curl -H "X-API-Key: cs_yourkey" http://localhost:8000/usage
```

## 📋 API 文档

### `POST /extract`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | 否* | 目标网页 URL |
| `text` | string | 否* | 原始文本（与 url 二选一） |
| `format` | string | 否 | 输出格式（默认 markdown） |

### 响应

```json
{
  "success": true,
  "url": "https://...",
  "title": "页面标题",
  "content": "清理后的正文内容...",
  "text_length": 1234,
  "metadata": {
    "word_count": 200,
    "char_count": 1234,
    "domain": "example.com",
    "source": "https://..."
  }
}
```

## 📦 部署

### Railway (推荐 — 免费额度足够起步)

```bash
# 1. Fork 本仓库
# 2. 在 Railway 新建项目，选择 GitHub 仓库
# 3. 启动命令: uvicorn app.main:app --host 0.0.0.0 --port $PORT
# 4. 检查日志获取初始 API Key
```

### Fly.io

```bash
fly launch
fly deploy
```

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 💰 定价计划（建议）

| Plan | 月请求 | 价格 |
|------|--------|------|
| Free | 50 | $0 |
| Starter | 500 | $9/mo |
| Pro | 5,000 | $29/mo |
| Enterprise | 自定义 | 谈 |

## 🧠 为什么有人愿意付钱？

- 做**竞品研究**的人需要批量抓取网页
- **LLM/AI 应用**开发者需要喂结构化数据
- **内容创作者**整理素材
- **数据分析师**准备数据集
- **产品经理**做市场调研

## 📄 License

MIT
