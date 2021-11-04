from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost:3306/fastapp"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

conn = engine.connect()
