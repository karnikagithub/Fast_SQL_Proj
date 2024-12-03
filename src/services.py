import databases as _database, models as _models, schemas as _schemas

import sqlalchemy.orm as _orm

import fastapi as _fastapi

import datetime as _dt

def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


## creating a session to create user
def get_database():
    ## creating a Session
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


# create user 
def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_pwd = user.password + 'thisisfake'
    db_user = _models.User(email=user.email,hashed_password=fake_hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

## read all users
def get_users(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.User).offset(skip).limit(limit).all()

## read the individual user
def get_user(user_id: int, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.id==user_id).first()
    
## create posts
def create_post(db: _orm.Session, user_id: int, post: _schemas.PostCreate):
    db_post = _models.Post(**post.dict(), onwer_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.Post).offset(skip).limit(limit)


def get_post(db: _orm.Session, post_id: int):
    return db.query(_models.Post).filter(_models.Post.id == post_id).first()


def delete_post(db: _orm.Session, post_id: int):
    db.query(_models.Post).filter(_models.Post.id == post_id).delete()
    db.commit()


def update_post(db: _orm.Session, post_id: int, post: _schemas.PostCreate):
    db_post_update = get_post(db=db, post_id=post_id)
    db_post_update.title = post.title
    db_post_update.content = post.content
    db_post_update.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(db_post_update)
    return db_post_update



## to update the post
# def update_post(post_id: int, db: _orm.Session):
    