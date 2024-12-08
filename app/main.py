from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Article(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    article: str


class NounBase(SQLModel):
    noun: str


class Noun(NounBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_plural: bool = False

    article_id: int = Field(foreign_key="article.id")


class NounResponse(NounBase):
    id: int
    article: str


class NounQuestion(NounBase):
    id: int


sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # Initial Seeding
    seed_article_data = [
        Article(id=1, article="Der"),
        Article(id=2, article="Die"),
        Article(id=3, article="Das"),
    ]
    seed_noun_data = [
        Noun(article_id=2, noun="Zeit"),
        Noun(article_id=2, noun="Zeiten", is_plural=True),
        Noun(article_id=1, noun="Tag"),
        Noun(article_id=2, noun="Tage", is_plural=True),
    ]
    with Session(engine) as session:
        existing = session.exec(select(Article)).all()

        if not existing:
            for article in seed_article_data:
                session.add(article)
                session.commit()

        existing = session.exec(select(Noun).limit(1)).all()
        if existing:
            return

        for noun in seed_noun_data:
            session.add(noun)

        session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/nouns/")
async def get_nouns(session: SessionDep):
    nouns = session.exec(select(Noun)).all()
    return nouns


@app.get("/nouns/{noun_id}", response_model=NounResponse)
async def get_noun_by_id(noun_id: int, session: SessionDep):
    result = session.exec(
        select(Noun, Article).where(Noun.id == noun_id, Noun.article_id == Article.id)
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Noun not found")

    noun, article = result

    response = NounResponse(id=noun.id, noun=noun.noun, article=article.article)

    return response


@app.get("/questions/{noun_id}", response_model=NounQuestion)
async def get_question_by_noun_id(noun_id: int, session: SessionDep):
    noun = session.get(Noun, noun_id)

    if not noun:
        raise HTTPException(status_code=404, detail="Question not found")

    return noun
