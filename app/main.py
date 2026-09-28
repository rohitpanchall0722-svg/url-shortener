from fastapi import FastAPI
from app.routers.url import router
from app.models.url import Url_Short
from app.database.connection import engine
from app.database.database import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)


