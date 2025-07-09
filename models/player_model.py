from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from database import Base

# Expects data to be in this format
class PlayerCard(BaseModel):
    name: str
    season: str
    team: str
    position: str
    height: str # format example: 6-9
    weight: float # pounds
    ppg: float  # points
    rpg: float  # rebounds
    apg: float  # assists
    blk: float  # blocks
    stl: float  # steals
    tov: float  # turnovers

    # SQLAlchemy returns python ORM (Object-Relational Mapping) objects 
    # Allows .from_orm() to create new pydantic PLayercard or TeamCard 
    # because it allows processing of SQLAlchemy instances (object, not dictionary form)
    model_config = {
    "from_attributes": True
}


# For database queries
class PlayerBase(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    season = Column(String) 
    team = Column(String)
    position = Column(String)
    height = Column(String)
    weight = Column(Float)
    ppg = Column(Float)
    rpg = Column(Float)
    apg = Column(Float)
    blk = Column(Float)
    stl = Column(Float)
    tov = Column(Float)

    __table_args__ = (UniqueConstraint('name', 'season', 'team', name='unique_player_season_team'), )