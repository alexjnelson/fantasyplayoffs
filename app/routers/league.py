from fastapi import APIRouter, Body, Depends, status
from sqlmodel import Session

from db import get_session
from models import League, RosterSettings, ScoringSettings, Users
from services.auth import validate_user
from services.league import create_league, get_leagues_for_user, get_teams_in_league, validate_league
from services.position import get_positions_by_name
from services.team import create_team


router = APIRouter(prefix="/league")


@router.get("/")
def get_leagues_route(user: Users = Depends(validate_user), db: Session = Depends(get_session)):
    return get_leagues_for_user(db, user)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_league_route(
    name: str = Body(...), 
    team_name: str = Body(...), 
    roster_settings: RosterSettings = Body(...), 
    scoring_settings: ScoringSettings = Body(...), 
    user: Users = Depends(validate_user),
    db: Session = Depends(get_session)
):
    positions = get_positions_by_name(db)
    league = create_league(
        db,
        user.id,
        name,
        roster_settings,
        scoring_settings
    )
    team = create_team(
        db,
        user.id,
        team_name,
        league,
        positions
    )

    db.commit()
    return {"league": league, "team": team}


@router.get("/{league_id}/teams")
def get_teams_in_league_route(league: League = Depends(validate_league), db: Session = Depends(get_session)):
    return get_teams_in_league(db, league)