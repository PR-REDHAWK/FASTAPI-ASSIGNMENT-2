from sqlmodel import SQLModel, create_engine, Session

# Configure SQLite database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    """Create the database and tables on application startup."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to provide a database session for each request."""
    with Session(engine) as session:
        yield session

