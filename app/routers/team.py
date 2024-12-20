from fastapi import APIRouter, Body, Depends
from sqlmodel import Session

from db.db import get_session
from models import FantasyTeam
from services.team import update_team_name, validate_user_owns_team


router = APIRouter(prefix="/team")


@router.put("/{team_id}/team-name")
def update_team_name_route(
    new_team_name: str = Body(...), 
    team: FantasyTeam = Depends(validate_user_owns_team), 
    db: Session = Depends(get_session)
):
    updated_team = update_team_name(team, new_team_name)
    db.commit()
    return updated_team