from sqlmodel import Session

from models import League, RosterSettings, ScoringSettings


def create_league( db: Session, commissioner_id: str, name: str, roster_settings: RosterSettings, scoring_settings: ScoringSettings) -> League:
    league = League(
        commissioner_id=commissioner_id,
        name=name,
        roster_settings=roster_settings,
        scoring_settings=scoring_settings
    )

    db.add(league)
    db.flush()
    return league