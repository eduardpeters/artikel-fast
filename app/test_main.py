from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_missing_noun_id():
    response = client.get("/nouns/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Noun not found"}


def test_get_noun_by_id():
    response = client.get("/nouns/1")
    assert response.status_code == 200
    assert response.json() == {"article": "Die", "noun": "Zeit", "is_plural": False}
