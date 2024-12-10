from sqlmodel import Session, SQLModel, create_engine, select

from models.article import Article
from models.noun import Noun


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
