import os

from fastapi import HTTPException, Request, Response, status, Depends
from jose import jwt, JOSEError

from core.settings import AUTH_TOKEN


def has_valid_token(request: Request, response: Response):
    token = request.cookies.get(AUTH_TOKEN)
    if not isinstance(token, str):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
        return token
    except JOSEError as e:
        response.delete_cookie(key=AUTH_TOKEN)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


ValidToken = Depends(has_valid_token)
