"""Add new fields for Users

Revision ID: d5de9639de67
Revises: 1ceee0785916
Create Date: 2025-09-25 16:50:34.956423

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d5de9639de67"
down_revision: Union[str, Sequence[str], None] = "1ceee0785916"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("nickname", sa.String(length=20), nullable=False))
    op.drop_column("users", "nickName")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "nickName", sa.VARCHAR(length=20), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "nickname")
