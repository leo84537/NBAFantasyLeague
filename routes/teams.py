from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_, func
from models.team_model import TeamBase, TeamCard
from models.player_model import PlayerCard, PlayerBase
from models.boxscore_model import BoxScoreBase, BoxScoreCard
from datetime import date
from database import get_db
from services.nba_api_methods import get_team_card, get_player_card, get_current_team, get_team_roster
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats

router = APIRouter(prefix="/teams", tags=["Teams"])

current_season = "2024-25"

# Get all teams
@router.get("/", response_model=list[TeamCard])
def get_all_teams(db: Session = Depends(get_db)):
    return db.query(TeamBase).all()

# Search teams in search bar (dropdown menu)
@router.get("/search/", response_model=list[TeamCard])
def search_teams(query: str, db: Session = Depends(get_db), limit: int = 10):
    query = query.lower()

    subquery = (
        db.query(
            TeamBase.name,
            func.max(TeamBase.season).label("latest_season")
        )
        .filter(TeamBase.name.ilike(f"%{query}%"))
        .group_by(TeamBase.name)
        .subquery()
    )

    results = (
        db.query(TeamBase)
        .join(
            subquery,
            (TeamBase.name == subquery.c.name) &
            (TeamBase.season == subquery.c.latest_season)
        )
        .order_by(TeamBase.name)
        .limit(limit)
        .all()
    )

    return results


@router.get("/{team_name}")
def get_or_fetch_team_with_roster(team_name: str, db: Session = Depends(get_db)):
    team_name = team_name.strip().title()

    # Try from DB (get most recent if multiple)
    team = (
        db.query(TeamBase)
        .filter(TeamBase.name.ilike(team_name))
        .order_by(TeamBase.season.desc())
        .first()
    )

    if team:
        season = team.season
        team_id = team.team_id
        abbreviation = team.abbreviation
    else:
        # Fallback to NBA API
        team_list = teams.find_teams_by_full_name(team_name)
        if not team_list:
            raise HTTPException(status_code=404, detail="Team not found")

        team_info = team_list[0]
        team_id = team_info["id"]
        abbreviation = team_info["abbreviation"]

        team_stats_df = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id).get_data_frames()[0]
        team_stats_df = team_stats_df.sort_values("YEAR", ascending=False)
        season = team_stats_df.iloc[0]["YEAR"]

        try:
            team_data = get_team_card(team_name, season)
        except ValueError:
            raise HTTPException(status_code=404, detail="Team card unavailable")

        existing = db.query(TeamBase).filter_by(
            name=team_data["name"],
            season=team_data["season"],
            team=team_data["team"]
        ).first()

        if not existing:
            team_data["team_id"] = team_id
            team_data["abbreviation"] = abbreviation
            new_team = TeamBase(**team_data)
            db.add(new_team)
            db.commit()
            db.refresh(new_team)
            team = new_team
        else:
            team = existing

    # Fetch roster and stats
    try:
#         recent_game = (
#             db.query(BoxScoreBase.game_id, BoxScoreBase.game_date)
#             .filter(BoxScoreBase.team == abbreviation)
#             .order_by(BoxScoreBase.game_date.desc())
#             .first()
#         )
#         roster_boxscores = (
#             db.query(BoxScoreBase)
#             .filter(
#                 BoxScoreBase.team == abbreviation,
#                 BoxScoreBase.game_id == recent_game.game_id
#             )
#             .all()
# )
#         # Fetch most recent stat entry for each player in DB
#         player_ids = [row.player_id for row in roster_boxscores]

        # raw_players = (
        #     db.query(PlayerBase)
        #     .filter(PlayerBase.player_id.in_(player_ids))
        #     .order_by(PlayerBase.name, PlayerBase.season.desc())
        #     .all()
        # )
        raw_players = db.query(PlayerBase).filter(
            PlayerBase.current_team.ilike(team_name),
            PlayerBase.season == get_current_nba_season()
        ).all()

        # Keep only most recent season per player
        seen = set()
        players = []
        for p in raw_players:
            key = p.name.lower().strip()
            if key not in seen:
                players.append(p)
                seen.add(key)
                
        players.sort(key=lambda p: p.ppg or 0, reverse=True)
        players = [PlayerCard.model_validate(p).model_dump() for p in players]

    except Exception as e:
        players = []
        print("Roster error:", e)

    return {
        **TeamCard.model_validate(team).model_dump(),
        "players": players
    }

def get_current_nba_season():
    today = date.today()
    year = today.year
    if today.month >= 10:  # October to December: new season starts
        return f"{year}-{str(year + 1)[-2:]}"
    else:  # January to September: still in previous season
        return f"{year - 1}-{str(year)[-2:]}"