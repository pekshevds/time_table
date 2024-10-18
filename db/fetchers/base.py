from typing import Any
from sqlalchemy import select
from db import session


def fetch_instance_by(model: Any, field_name: str, value: Any) -> Any | None:
    return session.scalars(
        select(model).where(getattr(model, field_name) == value)
    ).first()
