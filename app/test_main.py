import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app, get_session
from models.article import Article
from models.noun import Noun


# Initial Seeding
def load_article_data(session: Session):
    seed_article_data = [
        Article(id=1, article="Der"),
        Article(id=2, article="Die"),
        Article(id=3, article="Das"),
    ]
    for article in seed_article_data:
        session.add(article)
    session.commit()


def load_noun_data(session: Session):
    seed_noun_data = [
        Noun(article_id=2, noun="Zeit"),
        Noun(article_id=2, noun="Zeiten", is_plural=True),
        Noun(article_id=1, noun="Tag"),
        Noun(article_id=2, noun="Tage", is_plural=True),
    ]
    for noun in seed_noun_data:
        session.add(noun)
    session.commit()


def load_seed_data(session: Session):
    load_article_data(session)
    load_noun_data(session)


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


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_nouns(session: Session, client: TestClient):
    load_seed_data(session)
    response = client.get("/nouns")
    assert response.status_code == 200


def test_get_missing_noun_id(session: Session, client: TestClient):
    load_seed_data(session)
    response = client.get("/nouns/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Noun not found"}


def test_get_noun_by_id(session: Session, client: TestClient):
    load_article_data(session)
    noun_1 = Noun(article_id=2, noun="Zeit")
    session.add(noun_1)
    session.commit()

    response = client.get("/nouns/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "article": "Die",
        "noun": "Zeit",
        "is_plural": False,
    }


def test_get_missing_question_noun_by_id(session: Session, client: TestClient):
    load_seed_data(session)
    response = client.get("/questions/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}


def test_get_question_noun_by_id(session: Session, client: TestClient):
    load_article_data(session)
    noun_1 = Noun(article_id=2, noun="Zeit")
    session.add(noun_1)
    session.commit()

    response = client.get("questions/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "noun": "Zeit"}


def test_answer_missing_question(session: Session, client: TestClient):
    load_seed_data(session)

    answer = {"question_id": 9999, "answer": 1}
    response = client.post("answers", json=answer)

    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}


def test_answer_question_incorrectly_returns_feedback(
    session: Session, client: TestClient
):
    load_article_data(session)
    noun_1 = Noun(article_id=2, noun="Zeit")
    session.add(noun_1)
    session.commit()

    answer = {"question_id": 1, "answer": 1}
    response = client.post("answers", json=answer)
    assert response.status_code == 200
    assert response.json() == {"feedback": "KO"}


def test_answer_question_correctly_returns_feedback(
    session: Session, client: TestClient
):
    load_article_data(session)
    noun_1 = Noun(article_id=2, noun="Zeit")
    session.add(noun_1)
    session.commit()

    answer = {"question_id": 1, "answer": 2}
    response = client.post("answers", json=answer)
    assert response.status_code == 200
    assert response.json() == {"feedback": "OK"}
