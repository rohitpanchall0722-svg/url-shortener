from pydantic import BaseModel


class RequestUrl(BaseModel):
    original_url:str

class ResponseUrl(BaseModel):
    original_url:str
    new_url:str    