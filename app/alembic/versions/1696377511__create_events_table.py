from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

revision = '1696377511'
down_revision = '1696377178'

def upgrade():
    op.create_table(
        'events',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('slug', sa.String, nullable=False, unique=True),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('type', sa.Enum('preplay', 'inplay', name='eventtype'), nullable=False),
        sa.Column('sport_id', sa.Integer, sa.ForeignKey('sports.id'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'started', 'ended', 'cancelled', name='eventstatus'), nullable=False),
        sa.Column('scheduled_start', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actual_start', sa.DateTime),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    op.drop_table('events')

