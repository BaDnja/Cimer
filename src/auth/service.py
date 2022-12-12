import re

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from auth import models, schemas
from auth.models import User

# CONSTANTS
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Intermediate function helpers
def get_password_hash(password: str):
    """Return password hash from plain password"""
    password = bcrypt_context.hash(password)
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Return true if plain password matches hashed password from the db after verification"""
    return bcrypt_context.verify(plain_password, hashed_password)


def find_detail_in_error(substring: str, message: str):
    """Handle search for substring in error message. Used in exception handling."""
    return re.search(str(substring), str(message))


# Database interactive functions
def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    print(password)
    print(user.password)
    print(user)
    print(bcrypt_context.verify(password, user.password))
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, data: schemas.UserCreateSchema):
    db_user = User()
    db_user.email = data.email
    db_user.first_name = data.first_name
    db_user.last_name = data.last_name
    hashed_password = get_password_hash(data.password)
    db_user.password = hashed_password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
