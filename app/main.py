from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, text

from config.config import settings
from models.article import Article
from models.answer import AnswerFeedback, QuestionAnswer
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

origins = settings.cors_origins.split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"])


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


@app.get("/questions/random")
async def get_random_question(session: SessionDep):
    query = text(
        """
        SELECT id, noun FROM noun 
        WHERE _ROWID_ >= (abs(random()) % (SELECT max(_ROWID_) FROM noun))
        LIMIT 1
        """
    )

    result = session.connection().execute(query).first()

    if not result:
        raise HTTPException(500)

    return NounQuestion(id=result[0], noun=result[1])


@app.get("/questions/{noun_id}", response_model=NounQuestion)
async def get_question_by_noun_id(noun_id: int, session: SessionDep):
    noun = session.get(Noun, noun_id)

    if not noun:
        raise HTTPException(status_code=404, detail="Question not found")

    return noun


@app.post("/answers", response_model=AnswerFeedback)
async def post_answer_question(answer: QuestionAnswer, session: SessionDep):
    noun = session.get(Noun, answer.question_id)

    if not noun:
        raise HTTPException(status_code=404, detail="Question not found")

    feedback = AnswerFeedback(feedback="KO", article_id=noun.article_id)
    if noun.article_id == answer.answer:
        feedback.feedback = "OK"

    return feedback
