"""add new col to user

Revision ID: 20ae84c78333
Revises: 45355c465711
Create Date: 2023-12-14 00:10:00.095435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20ae84c78333'
down_revision: Union[str, None] = '45355c465711'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.Boolean, server_default=sa.true()))
    pass


def downgrade() -> None:
    op.drop_column('users','phone')
    pass
