from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


async def global_exception_handel(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "something went wrong"},
    )

