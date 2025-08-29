"""drop users table

Revision ID: 2eda0dc26294
Revises: 5bed484971b9
Create Date: 2025-08-29 13:14:43.096330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2eda0dc26294'
down_revision: Union[str, Sequence[str], None] = '5bed484971b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("users")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String(225), nullable=False),
        sa.Column("username", sa.String(100), unique=True, nullable=False),
        sa.Column("email", sa.String(225), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(225), nullable=False),
        sa.Column("Role", sa.String(10), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )
