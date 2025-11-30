import sys
from pathlib import Path

# Make the repository root importable so tests can 'import app'
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402 (repo root is inserted into sys.path for tests)
from app.db import engine  # noqa: E402


@pytest.fixture(autouse=True)
def cleanup_db():
    """Automatically dispose of the SQLAlchemy engine after each test to avoid ResourceWarnings."""
    yield
    try:
        engine.dispose()
    except Exception:
        pass
