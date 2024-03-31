from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
import os

Base = declarative_base()

class UserSessions(Base):
    __tablename__ = "user_sessions"

    session_token = Column(String, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.character_id'))

class Characters(Base):
    __tablename__ = "characters"

    character_id = Column(Integer, primary_key=True)
    access_token = Column(String)
    refresh_token = Column(String)
    creation_time = Column(Float)
    access_token_expiration_time = Column(Float)
    character_name = Column(String)
    character_portrait = Column(String)

def database_connection():
    try:
        postgres_user = os.getenv("POSTGRES_USER", "postgres")
        postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
        db_url = f"postgresql://{postgres_user}:{postgres_password}@localhost:5432/evetoolsdb"
        engine = create_engine(db_url)
        with Session(engine) as session:
            Base.metadata.create_all(bind=engine)
            return session

    except Exception:
        print("Could not connect to database")

def add_new_session(session: Session, session_token: str, character_id: int):
    try:
        new_session = UserSessions.insert().values(
            session_token=session_token, character_id=character_id)
        session.execute(new_session)
        session.commit()
    except Exception as e:
        raise e

def retrieve_session(session: Session, session_token: str) -> int:
    try:
        result = session.query(UserSessions.character_id).filter_by(
            session_token=session_token).first()
        if result:
            return result.character_id
        else:
            raise ValueError("No character found for session token")
    except Exception as e:
        raise e