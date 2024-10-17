"""change relationship course with student

Revision ID: 6aa438bbdce9
Revises: 12d5f4e3cfe9
Create Date: 2024-10-17 16:38:58.600153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6aa438bbdce9'
down_revision: Union[str, None] = '12d5f4e3cfe9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
