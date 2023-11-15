from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Настройка базы данных
engine = create_engine('sqlite:///DBs/PhaverAccounts.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    gqlID = Column(String, primary_key=True)

    owner = Column(String)
    refresh_token = Column(String)
    email = Column(String)
    password = Column(String)
    email_password = Column(String)

    username = Column(String)
    name = Column(String)
    credLevel = Column(Integer, default=1)
    createdAt = Column(DateTime)

    postsCount = Column(Integer, default=0)
    followings = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    likesCount = Column(Integer, default=0)
    retweetsCount = Column(Integer, default=0)

class Account2(Base):
    __tablename__ = 'account_s'
    gqlID = Column(String, primary_key=True)

    owner = Column(String)
    refresh_token = Column(String)
    email = Column(String)
    password = Column(String)
    email_password = Column(String)

    username = Column(String)
    name = Column(String)
    proxy = Column(String)
    credLevel = Column(Integer, default=1)
    createdAt = Column(DateTime)

    postsCount = Column(Integer, default=0)
    followings = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    likesCount = Column(Integer, default=0)
    retweetsCount = Column(Integer, default=0)

if __name__ == '__main__':

    Base.metadata.create_all(engine)