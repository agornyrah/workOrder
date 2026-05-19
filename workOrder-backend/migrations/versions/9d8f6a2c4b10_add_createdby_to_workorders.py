"""add creator fields to workOrders_table

Revision ID: 9d8f6a2c4b10
Revises: 3b72ec39b1d0
Create Date: 2026-05-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9d8f6a2c4b10"
down_revision: Union[str, Sequence[str], None] = "3b72ec39b1d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("workOrders_table", sa.Column("createdBy", sa.String(), nullable=True))
    op.add_column("workOrders_table", sa.Column("createdById", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_workorders_createdById_user_table",
        "workOrders_table",
        "user_table",
        ["createdById"],
        ["user_id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_workorders_createdById_user_table", "workOrders_table", type_="foreignkey")
    op.drop_column("workOrders_table", "createdById")
    op.drop_column("workOrders_table", "createdBy")
