"""Create a baseline migrations

Revision ID: 22048c3b43fe
Revises: e797d0486a55
Create Date: 2025-06-28 15:56:32.274308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22048c3b43fe'
down_revision: Union[str, None] = 'e797d0486a55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
