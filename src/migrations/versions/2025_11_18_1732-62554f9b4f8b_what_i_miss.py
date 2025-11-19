"""what I miss

Revision ID: 62554f9b4f8b
Revises: ee96b3985002
Create Date: 2025-11-18 17:32:09.207881

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "62554f9b4f8b"
down_revision: Union[str, Sequence[str], None] = "ee96b3985002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
