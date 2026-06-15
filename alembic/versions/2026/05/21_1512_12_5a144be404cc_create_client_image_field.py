"""create client image field

Revision ID: 5a144be404cc
Revises: 
Create Date: 2026-05-21 15:12:12.809334-03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a144be404cc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('client', sa.Column('picture', sa.String(500)))


def downgrade() -> None:
    op.drop_column('client', 'picture')
