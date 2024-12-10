from sqlmodel import Field, SQLModel  # type: ignore


class NounBase(SQLModel):
    noun: str


class Noun(NounBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_plural: bool = False

    article_id: int = Field(foreign_key="article.id")


class NounResponse(NounBase):
    id: int
    is_plural: bool
    article: str


class NounQuestion(NounBase):
    id: int
