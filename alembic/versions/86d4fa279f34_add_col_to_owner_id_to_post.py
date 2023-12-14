"""add col to owner id to post

Revision ID: 86d4fa279f34
Revises: 5c0d2df2cb45
Create Date: 2023-12-13 22:48:21.688824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86d4fa279f34'
down_revision: Union[str, None] = '5c0d2df2cb45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','owner_id')
    pass
