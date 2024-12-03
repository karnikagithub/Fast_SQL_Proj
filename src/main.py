import fastapi as _fastapi
import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm
from typing import List


## initiating the FASTAPI().
app = _fastapi.FastAPI()

_services.create_database()


### creating the users
@app.post("/users/", response_model=_schemas.User)
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session=_fastapi.Depends(_services.get_database)
):
    
    db_user = _services.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise _fastapi.HTTPException(status_code=400,detail="Oops Email in use!")
    
    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User])
async def read_users(
    skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_database)
):
    
    db_user = _services.get_users(db=db,skip=skip,limit=limit)

    return db_user


@app.get("/users/{user_id}", response_model=_schemas.User)
async def read_user(
    user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_database)
):
    
    db_user = _services.get_user(db=db, user_id=user_id)

    if db_user is None:
        return _fastapi.HTTPException(
            status_code=404, detail="No user is found with this id"
        )
    
    return db_user


@app.post("/users/{user_id}/posts/", response_model=_schemas.Post)
async def create_post(
    user_id: int, post: _schemas.PostCreate, db: _orm.Session = _fastapi.Depends(_services.get_database)
):
    
    ### first check for the user, if exists or not
    db_user = _services.get_user(db=db, user_id=user_id)

    if db_user is None:
        return _fastapi.HTTPException(
            status_code=404, detail="No user is found with this id"
        )
    
    return _services.create_post(post=post, user_id=user_id, db=db)


@app.get("/posts/", response_model=List[_schemas.Post])
async def read_posts(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_database)
):
    
    posts = _services.get_posts(db=db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=_schemas.Post)
async def get_post(
    post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_database)
):
    
    db_post = _services.get_post(db=db, post_id=post_id)

    if db_post is None:
        return _fastapi.HTTPException(
            status_code=404, detail="No POST is found with this id"
        )

    return db_post


@app.delete("/posts/{post_id}", response_model= _schemas.Post)
def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_database)):
    _services.delete_post(db=db, post_id=post_id)
    return {"Message": f"Successfully deleted post with id:{post_id}"}
    


@app.patch("/users/{post_id}/posts", response_model= _schemas.Post)
async def update_post(
    post_id: int, post: _schemas.PostCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_database),
):
    
    update_post = _services.update_post(db=db, post_id=post_id, post=post)
    # return {"Message": f"Successfully updated post with id:{post_id}"}
    return update_post
