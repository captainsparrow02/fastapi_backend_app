from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import time
# import psycopg2

# SQL_ALCHEMY_DATABASE_URL = 'postgresql://<username>:<password><@ip-address:port/hostname>/<database_name>'
SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres'
                                , password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database conncection successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)
'''