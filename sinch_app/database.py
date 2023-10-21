from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.logger import logger

SQLALCHEMY_DATABASE_URL = "sqlite:///./location.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    while True:
        try:
            logger(__name__, level='info', message='DB Session has started.')
            db = SessionLocal()
            yield db
            break
        except Exception as error:
            logger(__name__, level='exception', message='An exception has occurred.')
        finally:
            db.close()
            logger(__name__, level='info', message='DB Session was closed.')