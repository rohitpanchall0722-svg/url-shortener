from pydantic import BaseModel,HttpUrl,Field


class RequestUrl(BaseModel):
    original_url:HttpUrl

class ResponseUrl(BaseModel):
    original_url:HttpUrl
    new_url:str    

class CoustmRequest(BaseModel):
    original_url:HttpUrl
    coustm_url:str = Field(min_length=8,max_length=16,pattern=r"^[a-zA-Z0-9_-]+$")
    

class CoustmRepsponse(BaseModel):
    original_url:HttpUrl
    coustm_url:str    