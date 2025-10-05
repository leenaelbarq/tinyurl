
# tinyurlr — Minimal URL Shortener (FastAPI + SQLite)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000` for the simple UI.

## API
- `POST /shorten` JSON: `{"url":"https://..."}`
- `GET /{code}` → 307 redirect to original URL
- `GET /urls` → list all
- `DELETE /urls/{code}` → delete one

## SDLC model (summary)
For this tiny, well-understood app we used a **Lean/Iterative** approach:
1) **Planning & Requirements** — defined features + feasibility.  
2) **Design** — sketched architecture & DB model.  
3) **Implementation** — small increments with tests.  
4) **Verification** — `pytest` + manual UI checks.  
5) **Future Ops** — ready for containerization & CI.

## Run tests
```bash
pytest -q
```

## AI assistance (academic honesty)
I wrote the code and documentation and used AI tools **sparingly** to speed up boilerplate (e.g., generating basic FastAPI snippets and README polish) and GitHub Copilot for minor autocompletions. All design choices, architecture, and final validation are my own.
