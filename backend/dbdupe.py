from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


class UserSessions(declarative_base()):
    session_token = Column(String)
    character_id = Column(Integer, ForeignKey('characters.character_id'))

def retrieve_character_id(session_token: str) -> int:



class Database:
    Base = declarative_base()

    def __init__(self, db_url):
        try:
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()

            self.Base.metadata.create_all(bind=self.engine)

        except Exception as e:
            print(e)
            raise e

    class UserSessions(Base):
        __tablename__ = "user_sessions"

        session_token = Column(String, primary_key=True)
        character_id = Column(Integer, ForeignKey('characters.character_id'))

        character = relationship("Characters", back_populates="sessions")

        def retrieve_character_id(self, session, session_token: str) -> int:
            try:
                result = session.query(self.character_id).filter_by(
                    session_token=session_token).first()
                if result:
                    return result.character_id
                else:
                    raise ValueError("No character found for session token")
            except Exception as e:
                raise e

        def insert_new_session(self, session_token: str, character_id: int):
            try:
                new_session = self.UserSessions.insert().values(
                    session_token=session_token, character_id=character_id)
                self.session.execute(new_session)
                self.session.commit()
            except Exception as e:
                raise e

    class Characters(Base):
        __tablename__ = "characters"

        character_id = Column(Integer, primary_key=True)
        access_token = Column(String)
        refresh_token = Column(String)
        creation_time = Column(Float)
        access_token_expiration_time = Column(Float)
        character_name = Column(String)
        character_portrait = Column(String)

        sessions = relationship("UserSessions", back_populates="character")

        def insert_new_character(self, session, character_id: int, access_token: str, refresh_token: str, creation_time: float, access_token_expiration_time: float, character_name: str, character_portrait: str):
            try:
                new_character = self.Characters.insert().values(
                    character_id=character_id,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    creation_time=creation_time,
                    access_token_expiration_time=access_token_expiration_time,
                    character_name=character_name,
                    character_portrait=character_portrait)
                session.execute(new_character)
                session.commit()
            except Exception as e:
                raise e

        def retrieve_access_token_expiration(self, session, session_token: str) -> float:
            try:
                result = session.query(self.UserSessions.character.access_token_expiration_time).filter_by(
                    session_token=session_token).first()
                if result:
                    return result.access_token_expiration_time
                else:
                    raise ValueError("No character found for session token")
            except Exception as e:
                raise e

        def retrieve_refresh_token(self, session, session_token: str) -> str:
            try:
                result = session.query(self.UserSessions.character.refresh_token).filter_by(
                    session_token=session_token).first()
                if result:
                    return result.refresh_token
                else:
                    raise ValueError("No character found for session token")
            except Exception as e:
                raise e

        def refresh_access_token(self, session, access_token: str, refresh_token: str, new_access_token_expiration: float):
            try:
                session.query(self.UserSessions.character).filter_by(refresh_token=refresh_token).update({
                    self.access_token: access_token,
                    self.access_token_expiration_time: new_access_token_expiration
                })
                session.commit()
            except Exception as e:
                raise e

        def retrieve_character_name(self, session, session_token: str) -> str:
            try:
                result = session.query(self.UserSessions.character.character_name).filter_by(
                    session_token=session_token).first()
                if result:
                    return result.character_name
                else:
                    raise ValueError("No character found for session token")
            except Exception as e:
                raise e1
    # class HistoricalMarketData(declarative_base()):
    #    """
    #    This class is for storing historical prices and trading volumes for items in main trade regions.
    #    """
    #    __tablename__ = "historical_market_data"
#
    #    date = Column(Date)
    #    region = Column(Integer)
    #    item = Column(Integer)
    #    average = Column(Float)
    #    highest = Column(Float)
    #    lowest = Column(Float)
    #    volume = Column(Integer)

    # class LPStores(declarative_base()):
    #    """
    #    This class stores loyality point stores offers.
    #    """
    #    __tablename__ = "lp_stores"
#
    #    item = Column(Integer)
    #    corporation = Column(Integer)
    #    isk_cost = Column(Integer)
    #    lp_cost = Column(Integer)
    #    required_items = Column(String)
    #    amount = Column(Integer)

    class LPConvertion(Base):
        """
        Conversion rates for CONCORD LP.
        """
        __tablename__ = "lp_conversion"

        corporation = Column(Integer, primary_key=True)
        conversion_rate = Column(Float)

        def insert_new_corporation(self, Corporation, Conversion_rate):
            try:
                new_corporation = self.LPConvertion.insert().values(Corporation, Conversion_rate)
                self.session.execute(new_corporation)
                self.session.commit()
            except Exception as e:
                raise e

        def retrieve_exchange_rate(self, Corporation):
            try:
                result = self.session.query(
                    self.LPConvertion.conversion_rate).filter_by(corporation=Corporation)
                return result.conversion_rate
            except Exception as e:
                raise e

    # class Blueprints(declarative_base()):
    #    """
    #    This class stores the production information about blueprints.
    #    """
    #    __tablename__ = "blueprints"
#
    #    inputs = Column(String)
    #    output = Column(String)
    #    base_production_cost = Column(Float)
    #    base_production_time = Column(Float)
    #    base_research_cost = Column(Float)
    #    base_research_time = Column(Float)

    def close(self):
        self.session.close()
        self.engine.dispose()
