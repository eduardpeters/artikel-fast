from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from models.article import Article
from models.noun import Noun, NounQuestion, NounResponse
from utils.database import create_db_and_tables, engine


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
    assert noun.id is not None

    response = NounResponse(
        id=noun.id, noun=noun.noun, is_plural=noun.is_plural, article=article.article
    )

    return response


@app.get("/questions/{noun_id}", response_model=NounQuestion)
async def get_question_by_noun_id(noun_id: int, session: SessionDep):
    noun = session.get(Noun, noun_id)

    if not noun:
        raise HTTPException(status_code=404, detail="Question not found")

    return noun
