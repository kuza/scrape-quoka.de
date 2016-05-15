from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///quoka.sqlite')

db = scoped_session(sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine))

Base = declarative_base()
