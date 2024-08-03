"""add interests table

Revision ID: 6708f4568177
Revises: 
Create Date: 2024-08-03 09:58:04.234304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6708f4568177'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "interests",
        sa.Column("id", sa.UUID(), autoincrement=False),
        sa.Column("name", sa.String(255)),
        sa.Column("is_academic", sa.Boolean()),
        
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("interests")
