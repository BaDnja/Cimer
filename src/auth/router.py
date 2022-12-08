from fastapi import APIRouter, HTTPException, status, Response

from sqlalchemy import exc

from auth import schemas, service
from core.dependencies import DBDependency

router = APIRouter()


@router.post("/register/")
def register_user(data: schemas.UserCreateSchema, db=DBDependency):
    try:
        service.create_user(db, data)
    except exc.IntegrityError as e:
        error_info = e.orig.args
        if service.find_detail_in_error("email", error_info):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with specified email already exists")
    return Response(status_code=status.HTTP_201_CREATED)
