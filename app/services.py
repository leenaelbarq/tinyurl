
import re
import string
import random
from typing import Callable
from sqlalchemy.orm import Session
from .models import Url

URL_RE = re.compile(r"^https?://")


def validate_url(url: str) -> bool:
    """Return True if the URL starts with http:// or https://"""
    return bool(URL_RE.match(url.strip()))


def _rand_code(n: int = 6) -> str:
    """Generate a random alphanumeric code of length n"""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(n))


def generate_unique_code(db: Session, code_generator: Callable[[], str] = _rand_code) -> str:
    """Return a unique code that does not exist in the DB.

    Accepts a code_generator function so tests can inject a deterministic generator.
    """
    code = code_generator()
    while db.query(Url).filter_by(code=code).first():
        code = code_generator()
    return code


def create_short_url(db: Session, original_url: str, code_generator: Callable[[], str] = _rand_code) -> Url:
    """Create or return an existing short URL entry.

    Using code_generator parameter for easier testing and separation of concerns.
    """
    existing = db.query(Url).filter_by(original_url=original_url).first()
    if existing:
        return existing
    code = generate_unique_code(db, code_generator)
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
