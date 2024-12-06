from typing import List
from sqlmodel import Session, select

from models import FantasyTeam, League, RosterSettings, ScoringSettings, Users


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