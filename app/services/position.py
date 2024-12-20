from typing import Dict
from sqlmodel import Session

from models import Position


def get_positions_by_name(db: Session) -> Dict:
    """
    Query all positions from the database and create a mapping by name.
    """
    positions = db.query(Position).all()  # Fetch all positions
    return {position.name: position for position in positions}  # Map by name
