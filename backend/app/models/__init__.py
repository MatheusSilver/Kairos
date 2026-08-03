# New table models must be imported here so Alembic can discover them
from app.models.user import User

__all__ = ["User"]
