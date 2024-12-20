from fastapi import APIRouter, Body, Depends, status
from sqlmodel import Session

from db import get_session
from models import League, RosterSettings, ScoringSettings, Users
from services.auth import validate_user
from services.league import create_league, get_league, get_leagues_for_user, update_league_name, update_scoring_settings, validate_league_for_commissioner, validate_league_for_user
from services.position import get_positions_by_name
from services.team import create_team, get_teams_in_league


router = APIRouter(prefix="/league")


@router.get("/")
def get_leagues_route(user: Users = Depends(validate_user), db: Session = Depends(get_session)):
    return get_leagues_for_user(db, user)


@router.get("/{league_id}")
def get_league_route(league: League = Depends(validate_league_for_user), db: Session = Depends(get_session)):
    league = get_league(db, league.id)

    league_with_all_data = league.model_dump()
    league_with_all_data["roster_settings"] = league.roster_settings.model_dump()
    league_with_all_data["scoring_settings"] = league.scoring_settings.model_dump()
    
    return league_with_all_data


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
def get_teams_in_league_route(league: League = Depends(validate_league_for_user), db: Session = Depends(get_session)):
    return get_teams_in_league(db, league)


@router.put("/{league_id}/name")
def update_league_name_route(
    new_league_name: str = Body(...), 
    league: League = Depends(validate_league_for_commissioner),
    db: Session = Depends(get_session)
):
    updated_league = update_league_name(league, new_league_name)
    db.commit()
    return updated_league


@router.put("/{league_id}/scoringsettings")
def update_league_scoring_route(
    scoring_settings: ScoringSettings = Body(...),
    league: League = Depends(validate_league_for_commissioner),
    db: Session = Depends(get_session)
):
    updated_league = update_scoring_settings(db, league, scoring_settings)
    db.commit()
    return updated_league.scoring_settings
