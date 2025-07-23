from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from database import Base
from pydantic import BaseModel
from datetime import date
from typing import Optional

class BoxScoreCard(BaseModel):
    game_id: str
    game_date: date
    player_name: str
    player_id: int
    team: str
    opponent: str

    # Basic stats
    min: Optional[str]
    fgm: Optional[int]
    fga: Optional[int]
    fg3m: Optional[int]
    fg3a: Optional[int]
    ftm: Optional[int]
    fta: Optional[int]
    oreb: Optional[int]
    dreb: Optional[int]
    reb: Optional[int]
    ast: Optional[int]
    stl: Optional[int]
    blk: Optional[int]
    to: Optional[int]
    pf: Optional[int]
    pts: Optional[int]
    plus_minus: Optional[float]

    # Advanced stats
    off_rating: Optional[float]
    def_rating: Optional[float]
    net_rating: Optional[float]
    e_off_rating: Optional[float]= None
    e_def_rating: Optional[float]= None
    e_net_rating: Optional[float]= None
    ast_pct: Optional[float]
    ast_tov: Optional[float]
    ast_ratio: Optional[float]
    oreb_pct: Optional[float]
    dreb_pct: Optional[float]
    reb_pct: Optional[float]
    tm_tov_pct: Optional[float]
    efg_pct: Optional[float]
    ts_pct: Optional[float]
    usg_pct: Optional[float]
    e_usg_pct: Optional[float]= None
    pace: Optional[float]
    e_pace: Optional[float]= None
    pie: Optional[float]

    # Summary
    is_home_game: Optional[bool]
    wl: Optional[str]
    team_score: Optional[int]
    opponent_score: Optional[int]

    model_config = {
        "from_attributes": True
    }


class BoxScoreBase(Base):
    __tablename__ = "box_scores"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, index=True)
    game_date = Column(Date)

    player_name = Column(String)
    player_id = Column(Integer, index=True)
    team = Column(String)
    opponent = Column(String)

    # Basic stats
    min = Column(String)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    ftm = Column(Integer)
    fta = Column(Integer)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    to = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Float)

    # Advanced stats
    off_rating = Column(Float)
    def_rating = Column(Float)
    net_rating = Column(Float)
    e_off_rating = Column(Float)
    e_def_rating = Column(Float)
    e_net_rating = Column(Float)
    ast_pct = Column(Float)
    ast_tov = Column(Float)
    ast_ratio = Column(Float)
    oreb_pct = Column(Float)
    dreb_pct = Column(Float)
    reb_pct = Column(Float)
    tm_tov_pct = Column(Float)
    efg_pct = Column(Float)
    ts_pct = Column(Float)
    usg_pct = Column(Float)
    e_usg_pct = Column(Float)
    pace = Column(Float)
    e_pace = Column(Float)
    pie = Column(Float)

    # Summary
    is_home_game = Column(Boolean)
    wl = Column(String)
    team_score = Column(Integer)
    opponent_score = Column(Integer)