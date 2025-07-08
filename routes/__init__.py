from fastapi import APIRouter
from . import players, teams
#ANY routes would need to be included here to be run in main
router = APIRouter()

router.include_router(players.router, prefix="/api/players", tags=["Players"])
router.include_router(teams.router, prefix="/api/teams", tags=["Teams"])