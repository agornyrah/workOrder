"""add timestamp to activity log

Revision ID: 24f0c52dd81b
Revises: 9d8f6a2c4b10
Create Date: 2026-05-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "24f0c52dd81b"
down_revision: Union[str, Sequence[str], None] = "9d8f6a2c4b10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("activity_log", sa.Column("timestamp", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("activity_log", "timestamp")
