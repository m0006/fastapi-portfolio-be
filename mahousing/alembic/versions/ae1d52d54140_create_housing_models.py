"""create housing models

Revision ID: ae1d52d54140
Revises: 
Create Date: 2024-05-27 21:23:03.572205

"""
from typing import Sequence, Union

from alembic import op
import geoalchemy2
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae1d52d54140'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('housinglisting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('region', sa.String(length=25), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=15), nullable=False),
    sa.Column('sqfeet', sa.Integer(), nullable=False),
    sa.Column('beds', sa.Integer(), nullable=False),
    sa.Column('baths', sa.Float(), nullable=False),
    sa.Column('cats_allowed', sa.Integer(), nullable=False),
    sa.Column('dogs_allowed', sa.Integer(), nullable=False),
    sa.Column('smoking_allowed', sa.Integer(), nullable=False),
    sa.Column('wheelchair_access', sa.Integer(), nullable=False),
    sa.Column('electric_vehicle_charge', sa.Integer(), nullable=False),
    sa.Column('comes_furnished', sa.Integer(), nullable=False),
    sa.Column('laundry_options', sa.String(length=20), nullable=False),
    sa.Column('parking_options', sa.String(length=20), nullable=False),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # Removing:
    # op.create_index('idx_housinglisting_geom', 'housinglisting', ['geom'], unique=False, postgresql_using='gist')
    op.create_table('mbtaline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='MULTILINESTRING', srid=26986, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # Removing:
    # op.create_index('idx_mbtaline_geom', 'mbtaline', ['geom'], unique=False, postgresql_using='gist')
    op.create_table('mbtastation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('line', sa.String(length=30), nullable=False),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=26986, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # Removing:
    # op.create_index('idx_mbtastation_geom', 'mbtastation', ['geom'], unique=False, postgresql_using='gist')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Removing:
    # op.drop_index('idx_mbtastation_geom', table_name='mbtastation', postgresql_using='gist')
    op.drop_table('mbtastation')
    # Removing:
    # op.drop_index('idx_mbtaline_geom', table_name='mbtaline', postgresql_using='gist')
    op.drop_table('mbtaline')
    # Removing:
    # op.drop_index('idx_housinglisting_geom', table_name='housinglisting', postgresql_using='gist')
    op.drop_table('housinglisting')
    # ### end Alembic commands ###
