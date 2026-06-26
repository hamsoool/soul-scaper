# Soul Scraper — Web Scraping & Document Aggregation API

A REST API that automatically monitors, scrapes, extracts, and aggregates documents from configurable web sources. Built with FastAPI and deployed on Render, with data stored in Supabase PostgreSQL.

Designed for websites that publish documents (such as PDFs), announcements, reports, bulletins, or datasets on a recurring basis.

> ⚠️ Free-tier Render service — may take 30–60 seconds to wake up after inactivity.

---

# Authentication

All endpoints (except `/health`) require an API key passed via the `X-API-Key` header.

```bash
# Example using curl
curl -H "X-API-Key: your-api-key" https://example.onwebsite.com/documents

# Example using Python requests
import requests

headers = {"X-API-Key": "your-api-key"}
response = requests.get(
    "https://example.onwebsite.com/documents",
    headers=headers
)
```

**Missing or invalid key** → `401 Unauthorized`

---

# Data Sources

The API aggregates structured documents from one or more configured web sources.

Each source can define one or more categories depending on the website being monitored.

Example categories include:

| Category      | Description                    |
| ------------- | ------------------------------ |
| Reports       | Published reports              |
| Bulletins     | News or announcement bulletins |
| Price Updates | Scheduled pricing releases     |
| Documents     | General PDF publications       |

The scraping logic is configurable and can be adapted for different websites without changing the API interface.

---

# API Endpoints

## `GET /health`

Simple health check.

**Response**

```json
{
  "status": "ok"
}
```

---

## `GET /documents`

Returns a paginated list of aggregated documents sorted by newest first.

### Query Parameters

| Parameter | Type    | Default | Description                             |
| --------- | ------- | ------- | --------------------------------------- |
| limit     | integer | 20      | Number of documents to return (max 100) |
| offset    | integer | 0       | Pagination offset                       |
| category  | string  | —       | Filter by document category             |

### Example

```
GET /documents?category=Reports&limit=5
```

### Response

```json
[
  {
    "id": 42,
    "source_category": "Reports",
    "title": "Monthly Report",
    "source_url": "https://example.com/articles/...",
    "pdf_url": "https://example.com/files/report.pdf",
    "published_date": "2026-06-24T00:00:00Z",
    "created_at": "2026-06-25T00:03:12Z",
    "updated_at": "2026-06-25T00:03:12Z"
  }
]
```

---

## `GET /documents/{id}`

Returns full metadata together with the extracted document content.

### Response

```json
{
  "id": 42,
  "source_category": "Reports",
  "title": "Monthly Report",
  "source_url": "https://example.com/articles/...",
  "pdf_url": "https://example.com/files/report.pdf",
  "published_date": "2026-06-24T00:00:00Z",
  "created_at": "2026-06-25T00:03:12Z",
  "updated_at": "2026-06-25T00:03:12Z",
  "content": "Extracted PDF text..."
}
```

---

## `GET /latest`

Returns the latest document from each configured category.

### Response

```json
[
  {
    "id": 42,
    "source_category": "Reports"
  },
  {
    "id": 38,
    "source_category": "Bulletins"
  }
]
```

---

## `GET /stats`

Returns database statistics and scraper status.

### Response

```json
{
  "total_documents": 24,
  "documents_by_category": {
    "Reports": 14,
    "Bulletins": 10
  },
  "last_sync_time": "2026-06-25T00:03:45Z",
  "system_status": "idle"
}
```

---

## `POST /sync`

Triggers a manual synchronization in the background.

### Response

```json
{
  "status": "accepted",
  "message": "Manual synchronization has been queued and is executing in the background.",
  "processed_count": 0,
  "errors": []
}
```

---

# Architecture

Soul Scraper separates document ingestion from API serving.

```
Configured Website(s)
        │
        ▼
    sync.py
        │
        ├── Crawl configured pages
        ├── Discover new documents
        ├── Download supported files
        ├── Extract text & metadata
        └── Store in database
                │
                ▼
       PostgreSQL / SQLite
                │
                ▼
      FastAPI REST API
                │
                ├── GET /documents
                ├── GET /latest
                ├── GET /stats
                └── POST /sync
```

The synchronization process may run:

* manually
* on a schedule
* via Task Scheduler
* via cron
* from another orchestration service

depending on deployment requirements.

---

# Local Setup

## 1. Clone & Install

```bash
git clone https://github.com/hamsoool/soul-scaper.git

cd soul-scaper

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

## 2. Configure Environment

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres

# Or SQLite

# DATABASE_URL=sqlite+aiosqlite:///./scraper.db
```

---

## 3. Start the API

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 4. Run Synchronization

```bash
python sync.py
```

---

# Tech Stack

| Component      | Technology                     |
| -------------- | ------------------------------ |
| Web Framework  | FastAPI                        |
| Database       | PostgreSQL (Supabase) / SQLite |
| ORM            | SQLAlchemy 2.0                 |
| HTTP Client    | HTTPX                          |
| HTML Parsing   | BeautifulSoup4                 |
| PDF Extraction | PyMuPDF                        |
| Scheduler      | APScheduler                    |
| Deployment     | Docker / Render                |

---

# Features

* Configurable scraping sources
* Automatic document discovery
* PDF downloading
* Full-text extraction
* Metadata indexing
* Background synchronization
* REST API
* Pagination
* Category filtering
* API key authentication
* Async architecture
* PostgreSQL and SQLite support

---

# Security

* API Key authentication using constant-time comparison.
* SSRF protection through URL validation and DNS resolution.
* Public-IP validation before downloading remote resources.
* Configurable allowed host/domain whitelist.
* Streamed downloads with configurable file size limits.
* Request timeout protection.
* Async-safe document parsing.

---

# Disclaimer

Soul Scraper is a general-purpose document aggregation API.

Users are responsible for ensuring that scraping activities comply with the terms of service, robots.txt policies, and applicable laws governing each target website.

---

# License

MIT License — see LICENSE for details.
