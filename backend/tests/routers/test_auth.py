from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.core.senhaunica import MOCK_USERS
from app.models import User


def test_list_mock_users(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/auth/usp/mock-users")

    assert r.status_code == 200

    data = r.json()

    assert len(data) == len(MOCK_USERS)
    assert {u["loginUsuario"] for u in data} == {u.loginUsuario for u in MOCK_USERS}
    assert data[0]["vinculo"][0]["siglaUnidade"] == "IME"


def test_mock_login_creates_user(client: TestClient, db: Session) -> None:
    usp_user = MOCK_USERS[0]

    r = client.post(
        f"{settings.API_V1_STR}/auth/usp/mock-login/{usp_user.loginUsuario}"
    )

    assert r.status_code == 200
    assert r.json()["access_token"]

    user = db.exec(select(User).where(User.codpes == usp_user.loginUsuario)).first()

    assert user
    assert user.name == usp_user.nomeUsuario
    assert user.email == usp_user.emailUspUsuario
    assert user.is_apoio is False


def test_mock_login_reuses_existing_user(client: TestClient, db: Session) -> None:
    usp_user = MOCK_USERS[1]
    url = f"{settings.API_V1_STR}/auth/usp/mock-login/{usp_user.loginUsuario}"

    assert client.post(url).status_code == 200
    assert client.post(url).status_code == 200

    users = db.exec(select(User).where(User.codpes == usp_user.loginUsuario)).all()

    assert len(users) == 1


def test_mock_login_seeded_user_is_apoio(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/auth/usp/mock-login/{settings.FIRST_APOIO_CODPES}"
    )
    token = r.json()["access_token"]

    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert r.status_code == 200
    assert r.json()["is_apoio"] is True


def test_mock_login_token_authenticates(client: TestClient) -> None:
    usp_user = MOCK_USERS[0]

    r = client.post(
        f"{settings.API_V1_STR}/auth/usp/mock-login/{usp_user.loginUsuario}"
    )
    token = r.json()["access_token"]

    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert r.status_code == 200
    assert r.json()["codpes"] == usp_user.loginUsuario


def test_mock_login_unknown_user(client: TestClient) -> None:
    r = client.post(f"{settings.API_V1_STR}/auth/usp/mock-login/00000000")

    assert r.status_code == 404
