from database import Base, engine
from models.player_model import PlayerBase
from models.team_model import TeamBase

Base.metadata.create_all(bind=engine)