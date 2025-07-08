from fastapi import APIRouter, Query, HTTPException
from services.nba_api_methods import get_player_card
from models.player_model import PlayerCard

router = APIRouter()

@router.get("/search", response_model=PlayerCard)
def search_player(name: str = Query(..., example="LeBron James")):
    try:
        return get_player_card(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
