from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Noun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    article: str
    noun: str
    is_plural: bool = False


sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # Initial Seeding
    seed_data = [
        Noun(article="Die", noun="Zeit"),
        Noun(article="Die", noun="Zeiten", is_plural=True),
        Noun(article="Der", noun="Tag"),
        Noun(article="Die", noun="Tage", is_plural=True),
    ]
    with Session(engine) as session:
        existing = session.exec(select(Noun).limit(1)).all()
        if existing:
            return

        for noun in seed_data:
            session.add(noun)

        session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager  # type: ignore
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


"""
@app.get("/nouns/{noun_id}", response_model=Noun)
async def get_noun_by_id(noun_id: int):
    noun = fake_db.get(noun_id)
    if not noun:
        raise HTTPException(status_code=404, detail="Noun not found")
    return noun
"""
