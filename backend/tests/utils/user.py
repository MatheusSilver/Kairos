from sqlmodel import Session

from app import crud
from app.models import User
from app.schemas import UserCreate
from tests.utils.utils import random_codpes, random_email, random_lower_string


def create_random_user(db: Session, *, is_apoio: bool = False) -> User:
    user_in = UserCreate(
        codpes=random_codpes(),
        name=random_lower_string(),
        email=random_email(),
        is_apoio=is_apoio,
    )
    return crud.create_user(session=db, user_create=user_in)
