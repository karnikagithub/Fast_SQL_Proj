### import SQLAlchemy to create database.

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import sqlalchemy.ext.declarative as _declarative


## database url

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

## creating sql engine, by using connect_args={"check_same_thread":False} 
## this we can use "n" threads with DATABASE

engine = _sql.create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False} )


## Creating Session, to creating the database sessions

SessionLocal = _orm.sessionmaker(autocommit=False,autoflush=False,bind=engine)

## Creating BASE, which is used in models

Base = _declarative.declarative_base()

