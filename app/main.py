
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import services  


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



@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    obj = services.get_by_code(db, code)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    obj.hits += 1
    db.commit()
    return RedirectResponse(url=obj.original_url, status_code=307)
