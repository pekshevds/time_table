"""refactoring

Revision ID: 606a9a9af5ab
Revises: 326766cb91d4
Create Date: 2024-10-18 18:14:39.155582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '606a9a9af5ab'
down_revision: Union[str, None] = '326766cb91d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
