"""add user activity hidden

Revision ID: 7d3f46b973aa
Revises: 24f0c52dd81b
Create Date: 2026-05-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7d3f46b973aa"
down_revision: Union[str, Sequence[str], None] = "24f0c52dd81b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS user_activity_hidden (
            user_id INTEGER NOT NULL,
            log_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, log_id)
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_user_activity_hidden_user_id ON user_activity_hidden (user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_user_activity_hidden_log_id ON user_activity_hidden (log_id)")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_user_activity_hidden_log_id"), table_name="user_activity_hidden")
    op.drop_index(op.f("ix_user_activity_hidden_user_id"), table_name="user_activity_hidden")
    op.drop_table("user_activity_hidden")
