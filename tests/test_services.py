import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
import app.services as services
from app.models import Url


def create_in_memory_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def test_validate_url():
    assert services.validate_url("http://example.com")
    assert services.validate_url("https://example.com")
    assert not services.validate_url("ftp://example.com")


def test_create_short_url_with_custom_generator():
    db = create_in_memory_db()

    def gen():
        return "TESTCODE"

    u = services.create_short_url(db, "https://example.com/1", code_generator=gen)
    assert u.code == "TESTCODE"
    # Create again for same URL returns existing
    u2 = services.create_short_url(db, "https://example.com/1", code_generator=lambda: "OTHER")
    assert u2.id == u.id
    db.close()


def test_generate_unique_code_avoids_collision():
    db = create_in_memory_db()
    # Create an existing row with code COLLIDE
    url = Url(original_url="https://exist.com", code="COLLIDE")
    db.add(url)
    db.commit()

    calls = ["COLLIDE", "COL2"]

    def gen():
        return calls.pop(0)

    code = services.generate_unique_code(db, code_generator=gen)
    assert code == "COL2"
    db.close()


def test_delete_by_code():
    db = create_in_memory_db()
    u = Url(original_url="https://d.com", code="D")
    db.add(u)
    db.commit()
    ok = services.delete_by_code(db, "D")
    assert ok
    assert services.get_by_code(db, "D") is None
    db.close()
