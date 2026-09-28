from fastapi import APIRouter,Depends
from app.database.connection import get_db
from app.scheams.url import RequestUrl,ResponseUrl
from app.services.url_short import UrlService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/short_url",
                   tags=["Short_url"])

url_service = UrlService()

@router.post("create",response_model=ResponseUrl)
def create(request:RequestUrl,db:Session=Depends(get_db)):
    short = url_service.create_short_url(db=db,
                            original_url=request.original_url
                            )
    return ResponseUrl(
        original_url=short.original_url,
        new_url=short.short_url
    )

    
