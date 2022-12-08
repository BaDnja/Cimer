from fastapi import FastAPI, HTTPException
import uvicorn

from core.dependencies import DBDependency
from auth import service, models, schemas, router as auth_router
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router,
                   prefix="/auth",
                   tags=["auth"])


@app.get("/users/{user_id}", response_model=schemas.UserReadSchema)
def get_user(user_id: int, db=DBDependency):
    db_user = service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
