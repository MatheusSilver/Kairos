from sqlmodel import Session

from app import crud
from app.schemas import UserCreate, UserUpdate
from tests.utils.user import create_random_user
from tests.utils.utils import random_codpes, random_email, random_lower_string


def test_create_user(db: Session) -> None:
    codpes = random_codpes()
    name = random_lower_string()
    user_in = UserCreate(codpes=codpes, name=name, email=random_email())
    user = crud.create_user(session=db, user_create=user_in)

    assert user.codpes == codpes
    assert user.name == name
    assert user.is_apoio is False
    assert user.created_at is not None


def test_create_apoio_user(db: Session) -> None:
    user_in = UserCreate(
        codpes=random_codpes(), name=random_lower_string(), is_apoio=True
    )
    user = crud.create_user(session=db, user_create=user_in)

    assert user.is_apoio is True


def test_create_user_without_email(db: Session) -> None:
    user_in = UserCreate(codpes=random_codpes(), name=random_lower_string())
    user = crud.create_user(session=db, user_create=user_in)

    assert user.email is None


def test_get_user_by_codpes(db: Session) -> None:
    user = create_random_user(db)
    found = crud.get_user_by_codpes(session=db, codpes=user.codpes)

    assert found
    assert found.id == user.id


def test_get_user_by_codpes_not_found(db: Session) -> None:
    assert crud.get_user_by_codpes(session=db, codpes="00000000") is None


def test_update_user_promotes_to_apoio(db: Session) -> None:
    user = create_random_user(db)
    assert user.is_apoio is False

    crud.update_user(session=db, db_user=user, user_in=UserUpdate(is_apoio=True))
    db.refresh(user)

    assert user.is_apoio is True


def test_update_user_keeps_unset_fields(db: Session) -> None:
    user = create_random_user(db)
    original_name = user.name

    crud.update_user(session=db, db_user=user, user_in=UserUpdate(is_apoio=True))
    db.refresh(user)

    assert user.name == original_name
    assert user.codpes is not None
