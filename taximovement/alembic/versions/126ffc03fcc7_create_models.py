"""create models

Revision ID: 126ffc03fcc7
Revises: 
Create Date: 2024-05-17 15:23:22.629667

"""
from typing import Sequence, Union

from alembic import op
import geoalchemy2
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '126ffc03fcc7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('taxilocations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=40), nullable=False),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # Removing:
    # op.create_index('idx_taxilocations_geom', 'taxilocations', ['geom'], unique=False, postgresql_using='gist')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Removing:
    # op.drop_index('idx_taxilocations_geom', table_name='taxilocations', postgresql_using='gist')
    op.drop_table('taxilocations')
    # ### end Alembic commands ###
