from typing import List
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from models import FantasyTeam, League, RosterSettings, ScoringSettings, Users
from services.auth import validate_user


def validate_league(league_id: str, user: Users = Depends(validate_user), db: Session = Depends(get_session)) -> League:
    statement = select(FantasyTeam).where(FantasyTeam.league_id == league_id).where(FantasyTeam.user_id == user.id)
    team_owned_by_user = db.exec(statement).first()

    if team_owned_by_user is None:
        raise HTTPException(401, "User does not have a team in this league")
    
    return team_owned_by_user.league


def get_league(db: Session, league_id: str) -> League:
    statement = select(League).where(League.id == league_id)
    league = db.exec(statement).first()
    return league


def get_leagues_for_user(db: Session, user: Users) -> List[League]:
    statement = select(FantasyTeam).where(FantasyTeam.user_id == user.id).join(League)
    leagues = db.exec(statement).all()
    return leagues


def create_league(db: Session, commissioner_id: str, name: str, roster_settings: RosterSettings, scoring_settings: ScoringSettings) -> League:    
    league = League(
        commissioner_id=commissioner_id,
        name=name,
    )
    db.add(league)
    db.flush()

    roster_settings.league_id = league.id
    scoring_settings.league_id = league.id

    league.roster_settings = roster_settings
    league.scoring_settings = scoring_settings

    return league


def get_teams_in_league(db: Session, league: League) -> List[FantasyTeam]:
    statement = select(FantasyTeam).where(FantasyTeam.league_id == league.id)
    teams = db.exec(statement).all()
    return teams
