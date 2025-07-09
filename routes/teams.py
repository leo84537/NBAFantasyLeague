from fastapi import APIRouter, Depends # Depends is used to auto run functions 
from sqlalchemy.orm import Session # Depends(get_db()) runs get_db() automatically
from models.team_model import TeamBase # Update/Record records
from database import get_db
from models.team_model import TeamCard  

router = APIRouter(prefix="/teams", tags=["Teams"]) # Link name /{teams/team_name}

# Data of all teams located in the /teams
@router.get("/", response_model=list[TeamCard]) # db: Session, expect return object to be Session object
def get_all_teams(db: Session = Depends(get_db)): # Session -> call get_db() and inject the result.
    return db.query(TeamBase).all() # SELECT * FROM teams;

# Data of Warriors in /teams/warriors
@router.get("/{team_name}", response_model=TeamCard)
def get_team(team_name: str, db: Session = Depends(get_db)):
    return db.query(TeamBase).filter(TeamBase.name.ilike(team_name)).first() # SELECT name FROM teams WHERE team_name = name

# Search Bar for Teams
@router.get("/search/", response_model=list[TeamCard])
def search_teams(query: str, db: Session = Depends(get_db)):
    return db.query(TeamBase).filter(TeamBase.name.ilike(f"%{query}%")).all()