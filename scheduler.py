# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from models.player_model import PlayerBase
from services.nba_api_methods import get_player_card
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from time import sleep
import random

from database import SessionLocal
from services.nba_api_methods import get_team_roster, get_current_nba_season
from nba_api.stats.static import teams
from models.player_model import PlayerBase

# def update_all_team_rosters():
#     db = SessionLocal()
#     season = get_current_nba_season()
#     all_teams = teams.get_teams()

#     for team in all_teams:
#         try:
#             name = team["full_name"]
#             print(f"🔄 Updating {name}")
#             roster = get_team_roster(name, season)

#             # Clean out old roster if needed
#             db.query(PlayerBase).filter(PlayerBase.team == name, PlayerBase.season == season).delete()

#             for player in roster:
#                 player["team"] = name
#                 player["season"] = season
#                 db.add(PlayerBase(**player))
#             db.commit()
#         except Exception as e:
#             print(f"❌ Failed {name}: {e}")

#     db.close()

def update_players():
    db: Session = SessionLocal()
    all_players = db.query(PlayerBase.name).distinct().all()
    
    print("🔁 Starting nightly update...")
    for name_tuple in all_players:
        name = name_tuple[0]
        try:
            # Get player ID
            player_list = players.find_players_by_full_name(name)
            if not player_list:
                continue
            player_id = player_list[0]['id']

            # Get most recent season + team
            stats_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
            stats_df = stats_df[stats_df["TEAM_ABBREVIATION"] != "TOT"]
            stats_df = stats_df.sort_values("SEASON_ID", ascending=False)

            most_recent = stats_df.iloc[0]
            season = most_recent["SEASON_ID"]
            teamabr = most_recent["TEAM_ABBREVIATION"]

            # Get updated card
            data = get_player_card(name, season, teamabr)

            # Save to DB
            new_player = PlayerBase(**data)
            db.add(new_player)
            db.commit()
            db.refresh(new_player)

            print(f"✅ Updated {name} for {season} ({teamabr})")

            sleep(random.uniform(0.6, 1.2))  # avoid rate limit
        except Exception as e:
            print(f"❌ Error updating {name}: {e}")
            continue

    db.close()
    print("🌙 Nightly update complete.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_players, "cron", hour=2, minute=0)  # Run every day at 2:00 AM
    scheduler.start()
