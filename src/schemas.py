import pydantic as _pydantic
import datetime as _dt
from typing import List
""" Basically this file refers creating the serializers for the models,
    meaning serializing the request or responses will look like. """

## while creating the posts, it'll take only this data structures, basically serializing of data
class _PostBase(_pydantic.BaseModel):
    title: str
    content: str

## it is for creating the POST
class PostCreate(_PostBase):
    pass

## it is show or read the POSTS we have
class Post(_PostBase):
    id: int
    onwer_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    ### we define this bcuz defaultly orm_mode=False, and by default sqlalchemy uses LAZY LOADING
    ### using this orm_mode = True will give user with all related posts.
    class Config:
        orm_mode = True


class _UserBase(_pydantic.BaseModel):
    email: str

class UserCreate(_UserBase):
    password: str

class User(_UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True