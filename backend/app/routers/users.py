import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_apoio_user
from app.models import User
from app.schemas import Message, UserPublic, UsersPublic, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependencies=[Depends(get_current_apoio_user)],
    response_model=UsersPublic,
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(User)).one()
    statement = select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id and not current_user.is_apoio:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_apoio_user)],
    response_model=UserPublic,
)
def update_user(user_id: uuid.UUID, user_in: UserUpdate, session: SessionDep) -> Any:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(session=session, db_user=db_user, user_in=user_in)


@router.delete("/{user_id}")
def delete_user(
    user_id: uuid.UUID,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_apoio_user)],
) -> Message:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(
            status_code=403, detail="Apoio users are not allowed to delete themselves"
        )
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
