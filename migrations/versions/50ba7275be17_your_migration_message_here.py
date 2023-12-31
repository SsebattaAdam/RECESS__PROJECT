"""Your migration message here

Revision ID: 50ba7275be17
Revises: 0ecf60ba8453
Create Date: 2023-08-03 11:20:20.833978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50ba7275be17'
down_revision = '0ecf60ba8453'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=False),
    sa.Column('citizenship', sa.String(length=50), nullable=True),
    sa.Column('date_of_birth', sa.String(length=10), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('cv_filename', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job_application')
    # ### end Alembic commands ###
