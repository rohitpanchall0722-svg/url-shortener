from app.repositoires.url_repo import UrlRepository
from sqlalchemy.orm import Session
from app.models.url import Url_Short
from fastapi import HTTPException,status
import random,string


url_repo = UrlRepository()
class UrlService():
    def create_short_url(self,db:Session,original_url:str):
        code = "".join(random .choices(string.ascii_letters+string.digits,k=6)) 
        while url_repo.get_url(db,code) is not None:
            code = "".join(random.choices(string.ascii_letters+string.digits,k=6))
        return url_repo.create(db,original_url,code)

    def get_url(self,db:Session,url:str):
        code = url_repo.get_url(db,url)
        return code
