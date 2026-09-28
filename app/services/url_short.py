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

    def get_short_url(self,db:Session,url:str):
        search = url_repo.get_url(db,url)
        if search is None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="not found ")
        url_repo.click_count_url(db,search)
        return search

