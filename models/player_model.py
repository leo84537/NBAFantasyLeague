from pydantic import BaseModel

class PlayerCard(BaseModel):
    name: str
    height: str
    weight: float
    team: str
    position: str
    ppg: float  # points
    rpg: float  # rebounds
    apg: float  # assists
    blk: float  # blocks
    stl: float  # steals
    tov: float  # turnovers