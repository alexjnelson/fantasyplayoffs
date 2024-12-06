from typing import Dict, List
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from db.db import get_session
from models import FantasyTeam, League, Position, RosterSlot, Users
from services.auth import validate_user


def validate_user_owns_team(team_id: str, user: Users = Depends(validate_user), db: Session = Depends(get_session)) -> FantasyTeam:
    statement = select(FantasyTeam).where(FantasyTeam.id == team_id).where(FantasyTeam.user_id == user.id)
    team_owned_by_user = db.exec(statement).first()

    if team_owned_by_user is None:
        raise HTTPException(401, "User does not own this team")
    
    return team_owned_by_user


def create_roster_slot(db: Session, fantasy_team_id: int, week_no: int, position_id: int) -> RosterSlot:
    roster_slot = RosterSlot(
        fantasy_team_id=fantasy_team_id,
        week_no=week_no,
        position_id=position_id
    )
    
    db.add(roster_slot)
    return roster_slot


def create_roster_slots_by_position(db: Session, position: Position, slots: int, team_id: int) -> List[RosterSlot]:
    roster_slots = []

    for _ in range(slots):
        for week_no in range(1, 5):
            roster_slot = create_roster_slot(db, team_id, week_no, position.id)
            roster_slots.append(roster_slot)
    
    return roster_slots


def populate_roster_slots(db: Session, team: FantasyTeam, league: League, positions: Dict) -> List[RosterSlot]:
    if league.roster_settings is None:
        raise HTTPException(400, "No roster settings found for league when creating team")

    roster_slots = []
    roster_slots.append(create_roster_slots_by_position(db, positions["qb"], league.roster_settings.qb, team.id))
    roster_slots.append(create_roster_slots_by_position(db, positions["rb"], league.roster_settings.rb, team.id))
    roster_slots.append(create_roster_slots_by_position(db, positions["wr"], league.roster_settings.wr, team.id))
    roster_slots.append(create_roster_slots_by_position(db, positions["te"], league.roster_settings.te, team.id))
    roster_slots.append(create_roster_slots_by_position(db, positions["pk"], league.roster_settings.pk, team.id))
    roster_slots.append(create_roster_slots_by_position(db, positions["dst"], league.roster_settings.dst, team.id))
    return [x for xx in roster_slots for x in xx]


def create_team(db: Session, user_id: str, team_name: str, league: League, positions: Dict) -> FantasyTeam:
    team = FantasyTeam(
        user_id=user_id, 
        team_name=team_name,
        league_id=league.id
    )
    team.roster_slots = populate_roster_slots(db, team, league, positions)

    db.add(team)
    db.flush()
    return team        


def update_team_name(team: FantasyTeam, new_team_name: str) -> FantasyTeam:
    team.team_name = new_team_name
    return team