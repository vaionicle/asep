"""Adding previous_adt to educator

Revision ID: c4a1f6e2b7d3
Revises: df62558905e8
Create Date: 2026-08-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4a1f6e2b7d3'
down_revision: Union[str, Sequence[str], None] = 'df62558905e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('educator', sa.Column('previous_adt', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_educator_previous_adt'), 'educator', ['previous_adt'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_educator_previous_adt'), table_name='educator')
    op.drop_column('educator', 'previous_adt')
