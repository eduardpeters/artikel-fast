import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# client = TestClient(app)


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_nouns(client: TestClient):
    response = client.get("/nouns")
    assert response.status_code == 200


def test_get_missing_noun_id(client: TestClient):
    response = client.get("/nouns/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Noun not found"}


def test_get_noun_by_id(client: TestClient):
    response = client.get("/nouns/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "article": "Die",
        "noun": "Zeit",
        "is_plural": False,
    }


def test_get_missing_question_noun_by_id(client: TestClient):
    response = client.get("/questions/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}


def test_get_question_noun_by_id(client: TestClient):
    response = client.get("questions/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "noun": "Zeit"}
