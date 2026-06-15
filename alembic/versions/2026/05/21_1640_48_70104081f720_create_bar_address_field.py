"""create bar address field

Revision ID: 70104081f720
Revises: 5a144be404cc
Create Date: 2026-05-21 16:40:48.540867-03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70104081f720'
down_revision: Union[str, Sequence[str], None] = '5a144be404cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('bar', sa.Column('address', sa.String(200)))


def downgrade() -> None:
    op.drop_column('bar', 'address')
