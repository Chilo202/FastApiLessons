"""add_unique for email

Revision ID: 5a7e9c304952
Revises: 64fc623405fa
Create Date: 2025-09-25 17:55:05.655632

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5a7e9c304952"
down_revision: Union[str, Sequence[str], None] = "64fc623405fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
