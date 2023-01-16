import uvicorn
from fastapi import FastAPI, HTTPException

from auth import service, models, schemas, router as auth_router
from core.dependencies import DBDependency
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router,
                   prefix="/auth",
                   tags=["auth"])


@app.get("/users/{user_email}", response_model=schemas.UserReadSchema)
def get_user(user_email: str, db=DBDependency):
    db_user = service.get_user_by_email(db=db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
