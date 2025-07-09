from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.player_model import PlayerBase
from models.team_model import TeamBase
from nba_api_methods import get_player_card, get_team_card

# Manually specify players or teams and seasons
players = ["Stephen Curry", "LeBron James"]
teams = ["Golden State Warriors", "Los Angeles Lakers"]
seasons = ["2023-24", "2022-23"]

db: Session = SessionLocal()

def seed_players():
    for name in players:
        for season in seasons:
            try:
                card = get_player_card(name, season)
                existing = db.query(PlayerBase).filter_by(name=card["name"], season=card["season"], team=card["team"]).first()
                if not existing:
                    db.add(PlayerBase(**card))
                    print(f"✅ Added: {name} ({season})")
            except Exception as e:
                print(f"❌ Failed: {name} ({season}) - {e}")

def seed_teams():
    for name in teams:
        for season in seasons:
            try:
                card = get_team_card(name, season)
                existing = db.query(TeamBase).filter_by(name=card["name"], season=card["season"]).first()
                if not existing:
                    db.add(TeamBase(**card))
                    print(f"✅ Added team: {name} ({season})")
            except Exception as e:
                print(f"❌ Failed team: {name} ({season}) - {e}")

if __name__ == "__main__":
    seed_players()
    seed_teams()
    db.commit()
    db.close()
    print("🎉 Database seeding complete.")
