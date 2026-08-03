from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.senhaunica import MOCK_USERS
from app.db import engine, init_db
from app.main import app
from app.models import User
from tests.utils.utils import mock_login_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        session.execute(delete(User))
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def apoio_token_headers(client: TestClient) -> dict[str, str]:
    # MOCK_USERS[2] matches FIRST_APOIO_CODPES, so it is seeded as Apoio
    return mock_login_token_headers(client, MOCK_USERS[2].loginUsuario)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient) -> dict[str, str]:
    return mock_login_token_headers(client, MOCK_USERS[0].loginUsuario)
