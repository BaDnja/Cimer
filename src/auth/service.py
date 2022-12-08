import re

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from auth import models, schemas
from auth.models import User

# CONSTANTS
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Intermediate function helpers
def get_password_hash(password: str):
    """Return password hash from plain password"""
    password = bcrypt_context.hash(password)
    return bcrypt_context.hash(password)


def find_detail_in_error(substring: str, message: str):
    """Handle search for substring in error message. Used in exception handling."""
    return re.search(str(substring), str(message))


# Database interactive functions
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, data: schemas.UserCreateSchema):
    db_user = User()
    db_user.email = data.email
    hashed_password = get_password_hash(data.password)
    db_user.password = hashed_password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
