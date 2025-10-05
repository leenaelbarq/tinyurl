# tinyurl

Minimal URL shortener for quick links. Built with **FastAPI** and **SQLite**. Simple UI for creating links plus REST endpoints.

## Features
- Create short URLs  
- Redirect using `/{code}`  
- List all URLs with hit counter  
- Delete a short URL  
- Persistent storage (SQLite)  
- Minimal HTML UI (no frameworks)

## Prerequisites
- Python 3.10+  
- pip  
- Virtual environment (recommended)

## Setup

# clone
git clone https://github.com/leenaelbarq/tinyurl.git
cd tinyurl

# venv
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install
pip install -r requirements.txt

# run
uvicorn app.main:app --reload

Open:
- UI → http://127.0.0.1:8000
- API Docs → http://127.0.0.1:8000/docs

## Endpoints
| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | /shorten | Shorten a long URL ({"url": "https://example.com"}) |
| GET | /{code} | Redirects to the original URL |
| GET | /urls | List all shortened URLs and hit counts |
| DELETE | /urls/{code} | Delete a shortened URL |

## Run Tests
python -m pytest -q

## Project Structure
tinyurl/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + routes
│   ├── db.py            # SQLite engine/session
│   ├── models.py        # SQLAlchemy models
│   ├── services.py      # business logic (create/list/get/delete)
│   ├── templates/
│   │   └── index.html   # minimal UI
│   └── static/          # static assets
├── tests/
│   └── test_app.py      # test for shorten and redirect
├── requirements.txt
├── tinyurl.sqlite3      # local DB (auto-created)
├── .gitignore
└── README.md

## Quick Usage
1. Run the app.  
2. Paste any long URL in the field and click Shorten.  
3. Use the generated short URL to redirect.  
4. View all links and delete unwanted ones.  
5. Optionally, open /docs for the interactive API page.

## SDLC Model
This project followed a Lean / Iterative model.  
It started with the core shorten and redirect functions, then expanded step-by-step with testing, a minimal UI, and cleanup. Each phase allowed fast feedback and improvement without overcomplication.

## DevOps Reflection
To adapt this app for DevOps practices:
- Add a Dockerfile for containerization.  
- Configure GitHub Actions for CI (automatic testing on push).  
- Deploy to a platform like Render or Railway.  
- Later migrate from SQLite to a production database like PostgreSQL.  
- Add monitoring endpoints and automated formatting/linting checks.

## Academic Honesty
I used GitHub Copilot and AI tools occasionally for syntax help, debugging, and structuring repetitive sections (like test setup and function templates).  
All code, logic, and design decisions were fully implemented and verified by me to ensure I understood how every part works.
