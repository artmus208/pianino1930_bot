from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


Base = declarative_base()

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    age = Column(Integer)
    height = Column(Integer)
    phone = Column(String(256))
    photo_id = Column(String(256))
    consent = Column(Boolean, default=False)



DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
