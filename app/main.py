from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.exceptions import global_exception_handel
from app.routers.url import router

app = FastAPI(title="URL Shortener")

app.add_middleware(
                    TrustedHostMiddleware,
                   allowed_hosts=["127.0.0.1","localhost"]
                   )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handel)
app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "try to build an url shortner"
    }


@app.middleware("/http")
async def excaution_time(request:Request,call_next):
    start_time = time.perf_counter()
    respose = await call_next(request)

    end_time = time.perf_counter()
    exceution_time = end_time-start_time
    print(f"Execution time: {exceution_time:.4f} seconds")
    return respose

