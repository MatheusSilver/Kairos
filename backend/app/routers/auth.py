from datetime import timedelta
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.core.senhaunica import MOCK_USERS, get_mock_user
from app.schemas import Token, UserCreate
from app.schemas.usp import USPUser

router = APIRouter(prefix="/auth/usp", tags=["auth"])


@router.get("/mock-users", response_model=list[USPUser])
def list_mock_users() -> Any:
    return MOCK_USERS


@router.post("/mock-login/{codpes}", response_model=Token)
def mock_login(codpes: str, session: SessionDep) -> Any:
    usp_user = get_mock_user(codpes)
    if not usp_user:
        raise HTTPException(status_code=404, detail="Mock USP user not found")

    user = crud.get_user_by_codpes(session=session, codpes=usp_user.loginUsuario)
    if not user:
        user = crud.create_user(
            session=session,
            user_create=UserCreate(
                codpes=usp_user.loginUsuario,
                name=usp_user.nomeUsuario,
                email=usp_user.emailUspUsuario,
                is_apoio=usp_user.loginUsuario == settings.FIRST_APOIO_CODPES,
            ),
        )

    return Token(
        access_token=security.create_access_token(
            user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
    )
