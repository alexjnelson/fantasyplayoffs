"""removed def_pts field

Revision ID: bb78e0431bb6
Revises: 4e57cfc66347
Create Date: 2024-12-20 17:27:33.167566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bb78e0431bb6'
down_revision: Union[str, None] = '4e57cfc66347'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('defensive_player_stats', 'def_pts')
    op.drop_column('scoring_settings', 'def_pts')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scoring_settings', sa.Column('def_pts', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('defensive_player_stats', sa.Column('def_pts', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
