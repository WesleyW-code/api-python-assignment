"""my first migration

Revision ID: 3b7eb9b6c64c
Revises: 
Create Date: 2021-10-10 10:14:22.334494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7eb9b6c64c'
down_revision = None
branch_labels = None
depends_on = None

# This function tells what to do when upgrading to this revision
def upgrade():
    op.create_table(
    'patients',
    sa.Column('id', sa.Integer(),autoincrement=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('contact_number', sa.VARCHAR(200)),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
    'appointments',
    sa.Column('id', sa.Integer(),autoincrement=True),
    sa.Column('patient_id', sa.Integer()),
    sa.Column('appt_length', sa.Integer()),
    sa.Column('appt_time', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'],['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    

# This function tells what to do when downgrading from this revision.
def downgrade():
    op.drop_table('patients')
    op.drop_table('appointments')



