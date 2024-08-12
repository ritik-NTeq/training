from fastapi import FastAPI
from . import models
from .database import engine
from .routes import blog, user, authentication
# import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)