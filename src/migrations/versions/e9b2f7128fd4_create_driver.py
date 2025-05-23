"""
Revision: e9b2f7128fd4 - create driver (2025-04-27 18:15:30.952062)
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "e9b2f7128fd4"
down_revision: Union[str, None] = "971fe0d9faa2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "driver",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("registration_number", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("driver")
    # ### end Alembic commands ###
