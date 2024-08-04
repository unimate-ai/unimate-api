"""4_add chat related tables

Revision ID: 3c9b34fe8b62
Revises: acec5e35cb12
Create Date: 2024-08-03 10:23:43.305013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c9b34fe8b62'
down_revision: Union[str, None] = 'acec5e35cb12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chatrooms",
        
        sa.Column('id', sa.UUID(), autoincrement=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_deleted', sa.Boolean()),

        sa.Column("user_one_id", sa.UUID()),
        sa.Column("user_two_id", sa.UUID()),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["user_one_id"], ["users.id"],
            name="fk_chatroom_user_one",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_two_id"], ["users.id"],
            name="fk_chatroom_user_two",
            ondelete="CASCADE",
        )
    )

    op.create_table(
        "chat_messages",

        sa.Column('id', sa.UUID(), autoincrement=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_deleted', sa.Boolean()),

        sa.Column("chatroom_id", sa.UUID()),
        sa.Column("sender_id", sa.UUID()),
        sa.Column("message", sa.String()),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["chatroom_id"], ["chatrooms.id"],
            name="fk_message_chatroom",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["sender_id"], ["users.id"],
            name="fk_message_sender",
            ondelete="CASCADE",
        )
    )


def downgrade() -> None:
    op.drop_table("chat_messages")
    op.drop_table("chatrooms")
