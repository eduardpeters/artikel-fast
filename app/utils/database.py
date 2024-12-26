from pathlib import Path
import json

from sqlmodel import Session, SQLModel, create_engine, select

from models.article import Article
from models.noun import Noun


sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def load_nouns() -> list[Noun]:
    # Assuming server is started from app directory
    noun_file = Path("../seed_data/nouns.json").resolve()
    noun_list: list[Noun] = []
    with noun_file.open() as f:
        parsed_nouns = json.load(f)
        for noun in parsed_nouns:
            match noun["article"]:
                case "Der":
                    article_id = 1
                case "Die":
                    article_id = 2
                case _:  # Das
                    article_id = 3
            noun_list.append(
                Noun(
                    noun=noun["noun"],
                    is_plural=noun["is_plural"],
                    article_id=article_id,
                )
            )

    return noun_list


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # Initial Article Seeding
    seed_article_data = [
        Article(id=1, article="Der"),
        Article(id=2, article="Die"),
        Article(id=3, article="Das"),
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

        seed_noun_data = load_nouns()
        for noun in seed_noun_data:
            session.add(noun)

        session.commit()
