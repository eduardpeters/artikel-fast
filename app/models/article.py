from sqlmodel import Field, SQLModel  # type: ignore


class Article(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    article: str
