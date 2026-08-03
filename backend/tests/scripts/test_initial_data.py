from unittest.mock import MagicMock, patch

from app.initial_data import init, main


def test_init_calls_init_db() -> None:
    session_mock = MagicMock()

    with (
        patch("app.initial_data.Session", return_value=session_mock),
        patch("app.initial_data.init_db") as init_db_mock,
    ):
        init()

    assert init_db_mock.called


def test_main_creates_initial_data() -> None:
    with patch("app.initial_data.init") as init_mock:
        main()

    assert init_mock.called
