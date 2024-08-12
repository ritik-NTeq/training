from pydantic import BaseModel
from typing import List

# Pydantic models are schemas used as request and response models to specify the details to be shown in request/response body. 
# They also help in validations and hiding sensitive data. 

class Blog(BaseModel):
    title:str
    body:str

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title:str
    body:str
    creator: ShowUser
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None