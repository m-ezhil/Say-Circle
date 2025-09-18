from sqlalchemy import create_engine,and_,or_
from sqlalchemy.orm import declarative_base,sessionmaker

Base = declarative_base()

def create_db():
    DB_URL = 'sqlite:///app.db'
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine,session