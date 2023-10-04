from alembic import op
import sqlalchemy as sa


revision = '1696377583'
down_revision = '1696377511'

def upgrade():
    op.create_table(
        'selections',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('event_id', sa.Integer, sa.ForeignKey('events.id'), nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('outcome', sa.Enum('unsettled', 'void', 'lose', 'win', name='selectionoutcome'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    op.drop_table('selections')

