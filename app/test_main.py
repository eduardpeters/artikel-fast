from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_nouns():
    response = client.get("/nouns")
    assert response.status_code == 200


def test_get_missing_noun_id():
    response = client.get("/nouns/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Noun not found"}


def test_get_noun_by_id():
    response = client.get("/nouns/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "article": "Die",
        "noun": "Zeit",
        "is_plural": False,
    }


def test_get_missing_question_noun_by_id():
    response = client.get("/questions/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}


def test_get_question_noun_by_id():
    response = client.get("questions/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "noun": "Zeit"}
