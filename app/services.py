
import re, string, random
from sqlalchemy.orm import Session
from .models import Url

URL_RE = re.compile(r"^https?://")

def validate_url(url: str) -> bool:
    return bool(URL_RE.match(url.strip()))

def _rand_code(n: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(n))

def unique_code(db: Session) -> str:
    code = _rand_code()
    while db.query(Url).filter_by(code=code).first():
        code = _rand_code()
    return code

def create_short_url(db: Session, original_url: str) -> Url:
    existing = db.query(Url).filter_by(original_url=original_url).first()
    if existing:
        return existing
    code = unique_code(db)
    url = Url(original_url=original_url, code=code)
    db.add(url)
    db.commit()
    db.refresh(url)
    return url

def get_by_code(db: Session, code: str):
    return db.query(Url).filter_by(code=code).first()

def list_urls(db: Session):
    return db.query(Url).order_by(Url.id.desc()).all()

def delete_by_code(db: Session, code: str) -> bool:
    obj = get_by_code(db, code)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
