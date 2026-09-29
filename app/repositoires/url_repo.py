from app.database.database import Base
from app.models.url import Url_Short
from sqlalchemy import select,update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class UrlRepository():
    def create(self,db:Session,url:str,new_url:str):
        url_shoter = Url_Short(
            original_url=str(url),
            short_url=new_url,
        )
        db.add(url_shoter)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(url_shoter)
        return url_shoter

    def get_url(self,db:Session,short_url:str):
        search = select(Url_Short).where(Url_Short.short_url==short_url)
        return db.execute(search).scalar_one_or_none()


    def click_count_url(self,db:Session,click_link:Url_Short):
        stmt = update(Url_Short).where(Url_Short.id==click_link.id).values(
            click_count=Url_Short.click_count + 1
        )
        db.execute(stmt)
        db.commit()

        db.refresh(click_link)
        return click_link 
    

    def get_all_url(self,db:Session):
        stmt = select(Url_Short)
        return db.execute(stmt).scalars().all()

    def delete_url(self,db:Session,url_id:int):
        url = db.get(Url_Short,url_id)
        if url is None:
            return None
        db.delete(url)
        db.commit()
        return url