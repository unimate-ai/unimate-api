"""add users, socials, and friends table

Revision ID: 8a125ac93fb6
Revises: 6708f4568177
Create Date: 2024-08-03 10:02:02.367509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a125ac93fb6'
down_revision: Union[str, None] = '6708f4568177'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        
        sa.Column('id', sa.UUID(), autoincrement=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_deleted', sa.Boolean()),

        sa.Column("name", sa.String(255)),
        sa.Column("student_email", sa.String(255)),
        sa.Column("major", sa.String(255), nullable=True),
        sa.Column("cohort_year", sa.Integer(), nullable=True),
        sa.Column("graduation_year", sa.Integer(), nullable=True),
        sa.Column("interests", sa.ARRAY(sa.String(255)), nullable=True),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_email"),

    )

    op.create_table(
        "socials",

        sa.Column('id', sa.UUID(), autoincrement=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_deleted', sa.Boolean()),

        sa.Column("owner_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("social_type", sa.String(255)),
        sa.Column("url", sa.String()),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"],
            name="fk_socials_owner",
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "friends",

        sa.Column('id', sa.UUID(), autoincrement=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_deleted', sa.Boolean()),

        sa.Column("friend_one", sa.UUID(), nullable=False),
        sa.Column("friend_two", sa.UUID(), nullable=False),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["friend_one"], ["users.id"],
            name="fk_friend_one",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["friend_two"], ["users.id"],
            name="fk_friend_two",
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("friends")
    op.drop_table("socials")
    op.drop_table("users")
