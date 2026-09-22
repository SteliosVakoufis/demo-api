"""Create the initial parcel table."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001_create_parcel"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "parcel",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=40), nullable=False),
        sa.Column("owner_tax_number", sa.String(length=16), nullable=False),
        sa.Column("area", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_parcel_code", "parcel", ["code"], unique=True)
    op.create_index("ix_parcel_owner_tax_number", "parcel", ["owner_tax_number"])


def downgrade() -> None:
    op.drop_index("ix_parcel_owner_tax_number", table_name="parcel")
    op.drop_index("ix_parcel_code", table_name="parcel")
    op.drop_table("parcel")

