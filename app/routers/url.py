from fastapi import APIRouter,Depends
from app.database.connection import get_db
from app.scheams.url import RequestUrl,ResponseUrl,CoustmRepsponse,CoustmRequest
from app.services.url_short import UrlService
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/short_url",
                   tags=["Short_url"])

url_service = UrlService()

@router.post("/create",response_model=ResponseUrl)
def create(request:RequestUrl,http_request:Request,db:Session=Depends(get_db)):
    short = url_service.create_short_url(db=db,
                            original_url=str(request.original_url)
                            )
    new_url=str(http_request.url_for("redirect_url", short_url=short.short_url))
    return ResponseUrl(
        original_url=str(short.original_url),
        new_url=new_url
    )

@router.get("/all",name="get_all_url")
def get_all_url(db:Session=Depends(get_db)):
    return url_service.get_all_url(db)

@router.delete("/delete/{url_id}",name="delete_url")
def delete_url(url_id:int,db:Session=Depends(get_db)):
    deleted_url = url_service.delete_url(db,url_id)
    return {
        "message": "URL deleted successfully",
        "deleted_url": {
            "id": deleted_url.id,
            "original_url": deleted_url.original_url,
            "short_url": deleted_url.short_url,
            "click_count": deleted_url.click_count,
            "created_at": deleted_url.created_at,
        },
    }

@router.get("/{short_url}")
def redirect_url(short_url:str,db:Session=Depends(get_db)):
    result = url_service.get_short_url(db,short_url)
    return RedirectResponse(url=result.original_url, status_code=302)


@router.post("/coustom_url",response_model=CoustmRepsponse)
def coustm(request:CoustmRequest,http_request:Request,db:Session=Depends(get_db)):
    result = url_service.coustom_url(db=db,original_url=str(request.original_url),
                                     coustom_url=request.coustm_url)
    coustm_url=str(http_request.url_for("redirect_url", short_url=result.short_url))
    return CoustmRepsponse(
        original_url=str(result.original_url),
        coustm_url=coustm_url,
    )



