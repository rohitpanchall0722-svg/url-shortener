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

    def get_all_url(self,db:Session):
        return url_repo.get_all_url(db)

    def delete_url(self,db:Session,url_id:int):
        url = url_repo.delete_url(db,url_id)
        if url is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="not found ")
        return url

    def get_short_url(self,db:Session,url:str):
        search = url_repo.get_url(db,url)
        if search is None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="not found ")
        url_repo.click_count_url(db,search)
        return search

    def coustom_url(self,db:Session,original_url:str,coustom_url:str):
        existing = url_repo.get_url(db,coustom_url)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="try with diffresnt coustm name")
        save = url_repo.create(db,original_url,coustom_url)
        return save
        

