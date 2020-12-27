"""Add templates table

Revision ID: a2e49567641a
Revises: e2de0ea03287
Create Date: 2018-03-27 17:26:38.816926

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'a2e49567641a'
down_revision = 'e2de0ea03287'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('templates',
        sa.Column('template_name', sa.String(length=50), nullable=False),
        sa.Column('template', mysql.TEXT(), nullable=False),
        sa.Column('is_modified', mysql.TINYINT(), nullable=False),
        sa.PrimaryKeyConstraint('template_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('templates')
    # ### end Alembic commands ###
