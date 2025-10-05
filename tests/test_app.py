from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_shorten_and_redirect():
    payload = {"url": "https://example.com/abc"}
    r = client.post("/shorten", json=payload)
    assert r.status_code == 200
    code = r.json()["code"]

    r2 = client.get("/urls")
    assert r2.status_code == 200
    assert any(row["code"] == code for row in r2.json())

    r3 = client.get(f"/{code}", follow_redirects=False)
    assert r3.status_code in (307, 308)
    assert r3.headers["location"] == payload["url"]
