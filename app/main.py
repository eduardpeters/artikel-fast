from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Noun(BaseModel):
    article: str
    noun: str
    is_plural: bool = False


fake_db = {
    1: Noun(article="Die", noun="Zeit"),
    2: Noun(article="Die", noun="Zeiten", is_plural=True),
    3: Noun(article="Der", noun="Tag"),
    4: Noun(article="Die", noun="Tage", is_plural=True),
}

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/nouns/{noun_id}", response_model=Noun)
async def get_noun_by_id(noun_id: int):
    noun = fake_db.get(noun_id)
    if not noun:
        raise HTTPException(status_code=404, detail="Noun not found")
    return noun
