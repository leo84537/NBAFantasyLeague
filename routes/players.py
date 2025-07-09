from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.player_model import PlayerBase
from database import get_db
from models.player_model import PlayerCard

router = APIRouter(prefix="/players", tags=["Players"])

#
@router.get("/players/{name}", response_model=PlayerCard)
def get_or_fetch_player(name: str, db: Session = Depends(get_db)):
    player = db.query(PlayerBase).filter(PlayerBase.name.ilike(name)).first()
    if player:
        return PlayerCard.from_orm(player)
    
    # If not found, fetch from NBA API
    try:
        data = get_player_card(name)  # ← HERE
    except ValueError:
        raise HTTPException(status_code=404, detail="Player not found via NBA API")

    # Optionally: insert into database
    new_player = PlayerBase(**data)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return PlayerCard.from_orm(new_player)

# All Players
@router.get("/", response_model=list[PlayerCard])
def get_all_players(db: Session = Depends(get_db)):
    return db.query(PlayerBase).all()
# Search for One PLayer
@router.get("/{player_name}", response_model=PlayerCard)
def get_player(player_name: str, db: Session = Depends(get_db)):
    return db.query(PlayerBase).filter(PlayerBase.name.ilike(player_name)).first()

# Search Bar for Players
@router.get("/search/", response_model=list[PlayerCard])
def search_players(query: str, db: Session = Depends(get_db)):
    return db.query(PlayerCard).filter(PlayerCard.name.ilike(f"%{query}%")).all()

