"""3_add events related table

Revision ID: acec5e35cb12
Revises: 8a125ac93fb6
Create Date: 2024-08-03 10:13:14.305789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acec5e35cb12'
down_revision: Union[str, None] = '8a125ac93fb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "events",
        
        sa.Column('id', sa.UUID(), autoincrement=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_deleted', sa.Boolean()),

        sa.Column("name", sa.String(255)),
        sa.Column("organizer", sa.String(255)),
        sa.Column("is_campus_event", sa.Boolean()),
        sa.Column("start_time", sa.TIMESTAMP(timezone=True)),
        sa.Column("end_time", sa.TIMESTAMP(timezone=True)),
        sa.Column("interests", sa.ARRAY(sa.String(255))),
        sa.Column("location", sa.String(255)),
        sa.Column("description", sa.String()),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "events_attendance",

        sa.Column('id', sa.UUID(), autoincrement=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_deleted', sa.Boolean()),

        sa.Column("attendee_id", sa.UUID()),
        sa.Column("event_id", sa.UUID),
        
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["attendee_id"], ["users.id"],
            name="fk_attendances_attendee",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["event_id"], ["events.id"],
            name="fk_attendances_event",
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("events_attendance")
    op.drop_table("events")
