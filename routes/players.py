from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_, func, desc, and_
from models.player_model import PlayerBase, PlayerCard  
from models.boxscore_model import BoxScoreBase, BoxScoreCard
from database import get_db
from services.nba_api_methods import get_player_card, get_box_score  # NBA fallback
from datetime import datetime
from nba_api.stats.endpoints import playercareerstats, leaguegamefinder, commonplayerinfo, teaminfocommon, teamyearbyyearstats, commonteamroster
from nba_api.stats.static import players, teams


router = APIRouter(prefix="/players", tags=["Players"])
# Get all players
@router.get("/", response_model=list[PlayerCard])
def get_all_players(db: Session = Depends(get_db)):
    return db.query(PlayerBase).all()


# Search players by name (used by search bar) 
# Ensures only one result per player in drop down list (most recent season, could be multiple teams)
@router.get("/search/", response_model=list[PlayerCard])
def search_players(
    query: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    query = query.lower().strip()

    # Find all matching players
    players_query = (
        db.query(PlayerBase)
        .filter(
            or_(
                PlayerBase.name.ilike(f"{query}%"),
                PlayerBase.name.ilike(f"% {query}%")
            )
        )
        .order_by(PlayerBase.name.asc(), PlayerBase.season.desc())
        .all()
    )

    # Find the most recent season across all those players
    if not players_query:
        return []

    seen = set()
    unique = []
    for player in players_query:
        key = player.name.lower().strip()
        if key not in seen:
            unique.append(player)
            seen.add(key)
    return unique[:limit]

# One Page per player defaults to most recent season
@router.get("/{name}", response_model=PlayerCard)
def get_or_fetch_player(name: str, db: Session = Depends(get_db)):
    # Turn lebron james to LeBron James
    name = name.strip().title()

    player = (
        db.query(PlayerBase)
        .filter(PlayerBase.name.ilike(name))
        .order_by(PlayerBase.season.desc())
        .first()
    )

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get latest team from most recent game played (not DNP)
    last_game = (
        db.query(BoxScoreBase)
        .filter(BoxScoreBase.player_id == player.player_id)
        .filter(BoxScoreBase.min != None)  # Skips DNPs
        .order_by(BoxScoreBase.game_date.desc())
        .first()
    )

    if last_game and last_game.team:
        player.team = last_game.team  # Override outdated team info

    return PlayerCard.model_validate(player)

# Last 10 games for stats
@router.get("/{name}/last10", response_model=list[BoxScoreCard])
def get_last_10_games(name: str, db: Session = Depends(get_db)):
    player = (
        db.query(PlayerBase)
        .filter(PlayerBase.name.ilike(f"%{name}%"))
        .order_by(PlayerBase.season.desc())
        .first()
    )
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    last10 = (
    db.query(BoxScoreBase)
    .filter(
        BoxScoreBase.player_id == player.player_id,
        BoxScoreBase.min != None,            # Played at least 1 minute
        BoxScoreBase.pts != None             # at least one stat
    )
    .order_by(BoxScoreBase.game_date.desc())
    .limit(10)
    .all()
)
    if not last10:
        raise HTTPException(status_code=404, detail="No game data available")

    return list(reversed([BoxScoreCard.model_validate(row) for row in last10]))



