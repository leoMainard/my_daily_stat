from sqlmodel import Session, select
from my_daily_stat.db.schemas import User, StatObject, HistoricStats
from datetime import datetime
from my_daily_stat.config.env import Environnement

def create_url():
    return f"postgresql+psycopg2://{Environnement.config('DB_USER')}:" \
            f"{Environnement.config('DB_PASSWORD')}@{Environnement.config('DB_HOSTNAME')}:" \
            f"{Environnement.config('DB_PORT')}/{Environnement.config('DB_NAME')}"

class UserService:

    @staticmethod
    def create(session: Session, nom: str, prenom: str, email: str, password: str) -> User:
        user = User(nom=nom, prenom=prenom, email=email, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update(session: Session, user_id: int, **kwargs) -> User:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete(session: Session, user_id: int):
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        session.delete(user)
        session.commit()

class StatObjectService:

    @staticmethod
    def create(session: Session, **data) -> StatObject:
        obj = StatObject(**data)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @staticmethod
    def update(session: Session, id: int, **kwargs):
        obj = session.get(StatObject, id)
        if not obj:
            raise ValueError("StatObject not found")
        for k, v in kwargs.items():
            setattr(obj, k, v)
        session.commit()
        session.refresh(obj)
        return obj

    @staticmethod
    def delete(session: Session, id: int):
        obj = session.get(StatObject, id)
        if not obj:
            raise ValueError("StatObject not found")
        session.delete(obj)
        session.commit()

class HistoricStatsService:

    @staticmethod
    def add_stat(session: Session, statobject_id: int, date: datetime, value: str):
        hs = HistoricStats(statobject_id=statobject_id, date=date, value=value)
        session.add(hs)
        session.commit()
        session.refresh(hs)
        return hs

    @staticmethod
    def update(session: Session, historicstat_id: int, **kwargs):
        hs = session.get(HistoricStats, historicstat_id)
        if not hs:
            raise ValueError("HistoricStats entry not found")
        for key, value in kwargs.items():
            setattr(hs, key, value)
        session.commit()
        session.refresh(hs)
        return hs

    @staticmethod
    def delete(session: Session, historicstat_id: int):
        hs = session.get(HistoricStats, historicstat_id)
        if not hs:
            raise ValueError("HistoricStats entry not found")
        session.delete(hs)
        session.commit()

if __name__ == "__main__":
    from sqlmodel import SQLModel, create_engine
    from dotenv import load_dotenv
    load_dotenv()

    DATABASE_URL = create_url()
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)