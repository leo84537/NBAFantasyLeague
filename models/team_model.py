from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from database import Base
from typing import Optional

# Expects data to be in this format
class TeamCard(BaseModel):
    team_id: Optional[int]
    city: str
    name: str
    abbreviation: str
    # conference: str
    # division: str
    season: str
    wins: int
    losses: int
    win_pct: float

    # SQLAlchemy returns python ORM (Object-Relational Mapping) objects 
    model_config = {
    "from_attributes": True
}

# For database queries
class TeamBase(Base):
    __tablename__ = "teams"
    # Always define primary key, speeds up, unique = True prevents duplicates
    team_id = Column(Integer)
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    name = Column(String)
    abbreviation = Column(String)
    # conference = Column(String)
    # division = Column(String)
    season = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    win_pct = Column(Float)

    __table_args__ = (
        UniqueConstraint('name', 'season', name='unique_team_season'),
    )