"""Added all tables

Revision ID: 326766cb91d4
Revises:
Create Date: 2024-10-18 18:13:07.572977

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "326766cb91d4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "course",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=25), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subject",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "student",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("fullname", sa.String(), nullable=True),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mark_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("mark", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["student.id"],
        ),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subject.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("mark_table")
    op.drop_table("student")
    op.drop_table("subject")
    op.drop_table("course")
    # ### end Alembic commands ###
