
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import services  
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy import text
import time


app = FastAPI(title="TinyURL")


Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")



class CreateBody(BaseModel):
    url: str



@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):

    items = services.list_urls(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "items": items},
    )


@app.post("/shorten")
def shorten(body: CreateBody, db: Session = Depends(get_db)):

    if not services.validate_url(body.url):
        raise HTTPException(status_code=400, detail="Invalid URL. Must start with http:// or https://")
    u = services.create_short_url(db, body.url)
    return {"code": u.code, "short_url": f"/{u.code}", "original_url": u.original_url}


@app.get("/urls")
def get_urls(db: Session = Depends(get_db)):
    rows = services.list_urls(db)
    return [{"code": r.code, "original_url": r.original_url, "hits": r.hits} for r in rows]



@app.delete("/urls/{code}")
def remove(code: str, db: Session = Depends(get_db)):
    ok = services.delete_by_code(db, code)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": code}



# placeholder for redirect route defined after metrics so static endpoints are matched first
# Prometheus metrics
REQUEST_COUNT = Counter(
    "tinyurl_requests_total", "Total number of requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "tinyurl_request_latency_seconds", "Request latency in seconds", ["method", "endpoint"]
)
REQUEST_ERRORS = Counter("tinyurl_request_errors_total", "Total number of failed requests", ["method", "endpoint"])


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    status = 500
    method = request.method
    path = request.url.path
    try:
        response = await call_next(request)
        status = response.status_code
        if status >= 400:
            REQUEST_ERRORS.labels(method=method, endpoint=path).inc()
        return response
    except Exception:
        REQUEST_ERRORS.labels(method=method, endpoint=path).inc()
        raise
    finally:
        elapsed = time.time() - start
        REQUEST_LATENCY.labels(method=method, endpoint=path).observe(elapsed)
        REQUEST_COUNT.labels(method=method, endpoint=path, http_status=str(locals().get('status', 500))).inc()


@app.get("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    # a simple health status that verifies DB is accessible
    try:
        _ = db.execute(text("SELECT 1")).fetchone()
        status = "ok"
    except Exception:
        status = "error"
    return {"status": status}


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    obj = services.get_by_code(db, code)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    obj.hits += 1
    db.commit()
    return RedirectResponse(url=obj.original_url, status_code=307)
