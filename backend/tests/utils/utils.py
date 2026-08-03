import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_codpes() -> str:
    return "".join(random.choices(string.digits, k=8))


def mock_login_token_headers(client: TestClient, codpes: str) -> dict[str, str]:
    r = client.post(f"{settings.API_V1_STR}/auth/usp/mock-login/{codpes}")
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
