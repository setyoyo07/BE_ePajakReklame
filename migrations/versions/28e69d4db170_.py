"""empty message

Revision ID: 28e69d4db170
Revises: 
Create Date: 2020-02-13 09:52:56.298248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28e69d4db170'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('objek_pajak', sa.Column('jangka_waktu_pajak', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('objek_pajak', 'jangka_waktu_pajak')
    # ### end Alembic commands ###
