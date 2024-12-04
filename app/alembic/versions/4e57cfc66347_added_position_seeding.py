"""added position seeding

Revision ID: 4e57cfc66347
Revises: 8e0be8caaa8a
Create Date: 2024-12-04 02:26:36.179336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from models import Position


# revision identifiers, used by Alembic.
revision: str = '4e57cfc66347'
down_revision: Union[str, None] = '8e0be8caaa8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Get a database connection
    bind = op.get_bind()
    session = sqlmodel.Session(bind=bind)

    # Seed data
    positions = [
        Position(name="qb"),
        Position(name="wr"),
        Position(name="rb"),
        Position(name="te"),
        Position(name="pk"),
        Position(name="dst"),
    ]

    try:
        session.add_all(positions)
        session.commit()
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Failed to seed data: {e}")
    finally:
        session.close()


def downgrade():
    # Get a database connection
    bind = op.get_bind()
    session = sqlmodel.Session(bind=bind)

    try:
        # Delete seeded data
        session.query(Position).filter(Position.name.in_(["qb", "wr", "rb", "te", "pk", "dst"])).delete(synchronize_session=False)
        session.commit()
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Failed to remove seeded data: {e}")
    finally:
        session.close()