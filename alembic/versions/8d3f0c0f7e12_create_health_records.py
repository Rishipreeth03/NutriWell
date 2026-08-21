"""create health records

Revision ID: 8d3f0c0f7e12
Revises: 6b5abc9c01b1
Create Date: 2026-08-21 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "8d3f0c0f7e12"
down_revision: str | Sequence[str] | None = "6b5abc9c01b1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "health_records",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("bmi", sa.Float(), nullable=False),
        sa.Column("exercise_frequency", sa.Integer(), nullable=False),
        sa.Column("diet_quality", sa.Float(), nullable=False),
        sa.Column("sleep_hours", sa.Float(), nullable=False),
        sa.Column("smoking_status", sa.Integer(), nullable=False),
        sa.Column("alcohol_consumption", sa.Float(), nullable=False),
        sa.Column("prediction", sa.Float(), nullable=True),
        sa.Column("risk_level", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_health_records_email"), "health_records", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_health_records_email"), table_name="health_records")
    op.drop_table("health_records")
