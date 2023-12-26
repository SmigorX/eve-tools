from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base


class Database:
    """
    Base classes making the ORM
    """
    class UserSessions(declarative_base()):
        """
        This class represents the user_sessions table in the database.
        """
        __tablename__ = 'user_sessions'

        session_token = Column(String, primary_key=True)
        character_id = Column(Integer)
        access_token = Column(String)
        refresh_token = Column(String)
        creation_time = Column(Float)
        access_token_expiration_time = Column(Float)

    def __init__(self, db_url):
        """
        :param db_url: the link to the database in the format postgresql://user:password@host:port/database
        it is passed during the creation in order to make the engine and link to database
        """
        try:
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()

            self.UserSessions.metadata.create_all(self.engine)

        except Exception as e:
            print(e)
            raise e

    """
    Functions used to operate on the database
    """

    def retrieve_character_id(self, session_token: str) -> int:
        try:
            result = self.session.query(self.UserSessions.character_id).filter_by(session_token=session_token).first()
            return result.character_id
        except Exception as e:
            raise e

    def retrieve_access_token_expiration(self, session_token: str) -> float:
        try:
            return self.session.query(self.UserSessions.access_token_expiration_time).filter_by(
                session_token=session_token).first()
        except Exception as e:
            raise e

    def retrieve_refresh_token(self, session_token: str) -> str:
        try:
            return self.session.query(self.UserSessions.refresh_token).filter_by(session_token=session_token).first()
        except Exception as e:
            raise e

    def refresh_access_token(self, access_token: str, refresh_token: str, new_access_token_expiration: float):
        try:
            self.session.query(self.UserSessions).filter_by(refresh_token=refresh_token).update({
                self.UserSessions.access_token: access_token,
                self.UserSessions.access_token_expiration_time: new_access_token_expiration
            })
            self.session.commit()
        except Exception as e:
            raise e

    def close(self):
        self.session.close()
        self.engine.dispose()
