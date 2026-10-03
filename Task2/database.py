from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine


DATABASE_PATH = Path(__file__).resolve().parent / "database.db"
sqlite_url = f"sqlite:///{DATABASE_PATH.as_posix()}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    """Create the Task 2 database tables when the application starts."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Provide one database session per request."""
    with Session(engine) as session:
        yield session
