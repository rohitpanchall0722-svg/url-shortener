from app.database.database import Base
from app.models.url import Url_Short
from sqlalchemy import select
from sqlalchemy.orm import Session


class UrlRepository():
    def create(self,db:Session,url:str,new_url:str):
        url_shoter = Url_Short(
            original_url=url,short_url=new_url
        )
        db.add(url_shoter)
        db.commit()
        db.refresh(url_shoter)
        return url_shoter

    def get_url(self,db:Session,short_url:str):
        search = select(Url_Short).where(Url_Short.short_url==short_url)
        return db.execute(search).scalar_one_or_none()


    def click_count_url(self,db:Session,click_link:Url_Short):
        click_link.click_count+=1
        db.commit()
        return click_link
    
