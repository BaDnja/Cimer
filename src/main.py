from fastapi import FastAPI, Depends, HTTPException, status, Response
import uvicorn
from sqlalchemy import exc

from core.dependencies import DBDependency
from auth import service, models, schemas
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/register/")
def register_user(data: schemas.UserCreateSchema, db=DBDependency):
    try:
        service.create_user(db, data)
    except exc.IntegrityError as e:
        error_info = e.orig.args
        if service.find_detail_in_error("email", error_info):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with specified email already exists")
    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/users/{user_id}", response_model=schemas.UserReadSchema)
def get_user(user_id: int, db=DBDependency):
    db_user = service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
