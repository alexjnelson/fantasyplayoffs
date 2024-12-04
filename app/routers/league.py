from fastapi import APIRouter, Body, Depends, status
from sqlmodel import Session

from db.db import get_session
from models import RosterSettings, ScoringSettings
from models.users import Users
from services import get_current_user, create_league, create_team, get_positions_by_name


router = APIRouter(prefix="/league")


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_league_route(
    name: str = Body(...), 
    team_name: str = Body(...), 
    roster_settings: RosterSettings = Body(...), 
    scoring_settings: ScoringSettings = Body(...), 
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    positions = get_positions_by_name(db)
    
    league = create_league(
        db,
        current_user.id,
        name,
        roster_settings,
        scoring_settings
    )

    team = create_team(
        db,
        current_user.id,
        team_name,
        league,
        positions
    )

    db.commit()
    return {"league": league, "team": team}

