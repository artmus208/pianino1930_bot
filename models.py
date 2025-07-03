#! models.py
from datetime import datetime
import enum

from sqlalchemy import (
    BigInteger, create_engine, Column, 
    Integer, String, Boolean, DateTime,
    Enum
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

Base = declarative_base()

class ConfirmationStatus(enum.Enum):
    unknown = "unknown"
    yes = "yes"
    no = "no"


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    phone = Column(String(256))
    status = Column(String(256))
    char = Column(String(256))
    telegram_id = Column(BigInteger, unique=True)
    consent = Column(Boolean, default=False)
    time_created = Column(DateTime, default=datetime.now())
    confirmed = Column(
        Enum(ConfirmationStatus), 
        default=ConfirmationStatus.unknown
    )


DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
