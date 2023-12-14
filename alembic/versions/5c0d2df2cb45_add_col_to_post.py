"""add col to post

Revision ID: 5c0d2df2cb45
Revises: f62dee3cfd5a
Create Date: 2023-12-13 22:45:34.438452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c0d2df2cb45'
down_revision: Union[str, None] = 'f62dee3cfd5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
