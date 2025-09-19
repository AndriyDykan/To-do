from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base =declarative_base()

def get_db():
    database = Session()
    try:
        yield database
    finally:
        database.close()
