import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.user import create_random_user


def test_read_user_me(client: TestClient, apoio_token_headers: dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=apoio_token_headers)

    assert r.status_code == 200

    current_user = r.json()

    assert current_user["is_apoio"] is True
    assert current_user["codpes"] == settings.FIRST_APOIO_CODPES


def test_read_user_me_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)

    assert r.status_code == 200
    assert r.json()["is_apoio"] is False


def test_read_user_me_without_token(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me")

    assert r.status_code == 401


def test_read_user_me_invalid_token(client: TestClient) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": "Bearer not-a-token"},
    )

    assert r.status_code == 403


def test_read_users_as_apoio(
    client: TestClient, db: Session, apoio_token_headers: dict[str, str]
) -> None:
    create_random_user(db)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=apoio_token_headers)

    assert r.status_code == 200

    data = r.json()

    assert data["count"] >= 1
    assert len(data["data"]) >= 1
    for item in data["data"]:
        assert "codpes" in item
        assert "is_apoio" in item


def test_read_users_as_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers)

    assert r.status_code == 403


def test_read_user_by_id_self(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    me = client.get(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers
    ).json()

    r = client.get(
        f"{settings.API_V1_STR}/users/{me['id']}", headers=normal_user_token_headers
    )

    assert r.status_code == 200
    assert r.json()["id"] == me["id"]


def test_read_user_by_id_other_as_apoio(
    client: TestClient, db: Session, apoio_token_headers: dict[str, str]
) -> None:
    user = create_random_user(db)

    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}", headers=apoio_token_headers
    )

    assert r.status_code == 200
    assert r.json()["codpes"] == user.codpes


def test_read_user_by_id_other_as_normal_user(
    client: TestClient, db: Session, normal_user_token_headers: dict[str, str]
) -> None:
    user = create_random_user(db)

    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}", headers=normal_user_token_headers
    )

    assert r.status_code == 403


def test_read_user_by_id_not_found(
    client: TestClient, apoio_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/{uuid.uuid4()}", headers=apoio_token_headers
    )

    assert r.status_code == 404


def test_update_user_promotes_to_apoio(
    client: TestClient, db: Session, apoio_token_headers: dict[str, str]
) -> None:
    user = create_random_user(db)

    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=apoio_token_headers,
        json={"is_apoio": True},
    )

    assert r.status_code == 200
    assert r.json()["is_apoio"] is True

    db.refresh(user)
    assert user.is_apoio is True


def test_update_user_as_normal_user(
    client: TestClient, db: Session, normal_user_token_headers: dict[str, str]
) -> None:
    user = create_random_user(db)

    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=normal_user_token_headers,
        json={"is_apoio": True},
    )

    assert r.status_code == 403


def test_update_user_not_found(
    client: TestClient, apoio_token_headers: dict[str, str]
) -> None:
    r = client.patch(
        f"{settings.API_V1_STR}/users/{uuid.uuid4()}",
        headers=apoio_token_headers,
        json={"is_apoio": True},
    )

    assert r.status_code == 404


def test_delete_user(
    client: TestClient, db: Session, apoio_token_headers: dict[str, str]
) -> None:
    user = create_random_user(db)

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.id}", headers=apoio_token_headers
    )

    assert r.status_code == 200
    assert r.json()["message"] == "User deleted successfully"

    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}", headers=apoio_token_headers
    )

    assert r.status_code == 404


def test_delete_user_self_not_allowed(
    client: TestClient, apoio_token_headers: dict[str, str]
) -> None:
    me = client.get(
        f"{settings.API_V1_STR}/users/me", headers=apoio_token_headers
    ).json()

    r = client.delete(
        f"{settings.API_V1_STR}/users/{me['id']}", headers=apoio_token_headers
    )

    assert r.status_code == 403


def test_delete_user_as_normal_user(
    client: TestClient, db: Session, normal_user_token_headers: dict[str, str]
) -> None:
    user = create_random_user(db)

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.id}", headers=normal_user_token_headers
    )

    assert r.status_code == 403
