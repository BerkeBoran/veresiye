"""backfill sale_date and payment_date from created_at

Revision ID: 9ddf82dfde60
Revises: 0c7358795b78
Create Date: 2026-09-26 15:53:06.369863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ddf82dfde60'
down_revision: Union[str, Sequence[str], None] = '0c7358795b78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # created_at UTC olarak saklanıyor (SQLite CURRENT_TIMESTAMP).
    # 'localtime' ile Türkiye saatine çeviriyoruz, gece 00:00-03:00 arası girilen kayıtlar bir önceki güne düşmesin.
    op.execute("UPDATE sales SET sale_date = DATE(created_at, 'localtime') WHERE sale_date IS NULL")
    op.execute("UPDATE payments SET payment_date = DATE(created_at, 'localtime') WHERE payment_date IS NULL")


def downgrade() -> None:
    # Geri alınamaz: tarihlerin hangisinin elle girildiğini, hangisinin burada doldurulduğunu ayırt edemeyiz.
    pass