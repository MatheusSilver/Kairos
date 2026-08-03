from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.core.config import settings
from app.utils import generate_test_email, send_email


def test_health_check(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/utils/health-check/")

    assert r.status_code == 200
    assert r.json() is True


def test_test_email(client: TestClient, apoio_token_headers: dict[str, str]) -> None:
    with (
        patch("app.routers.utils.send_email", return_value=None),
        patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
        patch("app.core.config.settings.EMAILS_FROM_EMAIL", "info@example.com"),
    ):
        r = client.post(
            f"{settings.API_V1_STR}/utils/test-email/?email_to=test@example.com",
            headers=apoio_token_headers,
        )

    assert r.status_code == 201
    assert r.json()["message"] == "Test email sent"


def test_test_email_as_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/utils/test-email/?email_to=test@example.com",
        headers=normal_user_token_headers,
    )

    assert r.status_code == 403


def test_generate_test_email_renders_template() -> None:
    email_data = generate_test_email(email_to="test@example.com")

    assert settings.PROJECT_NAME in email_data.subject
    assert "test@example.com" in email_data.html_content


def test_send_email_uses_smtp_settings() -> None:
    message_mock = MagicMock()
    with (
        patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
        patch("app.core.config.settings.SMTP_USER", "user"),
        patch("app.core.config.settings.SMTP_PASSWORD", "password"),
        patch("app.core.config.settings.EMAILS_FROM_EMAIL", "info@example.com"),
        patch("app.utils.emails.Message", return_value=message_mock),
    ):
        send_email(email_to="test@example.com", subject="s", html_content="<p>x</p>")

    assert message_mock.send.called
    smtp_options = message_mock.send.call_args.kwargs["smtp"]
    assert smtp_options["host"] == "smtp.example.com"
    assert smtp_options["user"] == "user"
