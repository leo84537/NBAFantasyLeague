import time, random
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import BoxScoreSummaryV2, playercareerstats, leaguegamefinder, commonplayerinfo, teaminfocommon, teamyearbyyearstats, commonteamroster, BoxScoreTraditionalV2, BoxScoreAdvancedV2
from nba_api.stats.library.http import NBAStatsHTTP
from models.boxscore_model import BoxScoreCard, BoxScoreBase
import pandas as pd
from datetime import date

NBAStatsHTTP.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/"
})

def get_current_team(player_id: str, db):
    team_abbr_to_full = {team["abbreviation"]: team["full_name"] for team in teams.get_teams()}

    recent_game = (
        db.query(BoxScoreBase)
        .filter(BoxScoreBase.player_id == player_id)
        .order_by(BoxScoreBase.game_date.desc())
        .first()
    )
    if not recent_game:
        return None
    abbr = recent_game.team
    return team_abbr_to_full.get(abbr, abbr)

def get_box_score(game_id: str) -> list[BoxScoreCard]:
    time.sleep(random.uniform(0.6, 1.2))  # 🙏 Don't ban me

    # All nba api data
    trad_df = BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[0]
    adv_df = BoxScoreAdvancedV2(game_id=game_id).get_data_frames()[0]
    summary_df = BoxScoreSummaryV2(game_id=game_id).get_data_frames()[0]

    if trad_df.empty or adv_df.empty or summary_df.empty:
        print(f"⚠️ Empty DataFrame for game {game_id}, skipping.")
        return []

    # Game date
    game_date_str = summary_df.loc[0, "GAME_DATE_EST"]
    game_date = pd.to_datetime(game_date_str).date()

    # Build team_id → score and WL mapping
    # Sum team scores
    team_scores = trad_df.groupby("TEAM_ID")["PTS"].sum().to_dict()
    team_ids = list(team_scores.keys())

    # Determine win/loss manually
    if len(team_ids) == 2:
        team1, team2 = team_ids
        score1, score2 = team_scores[team1], team_scores[team2]

        team_wins = {
            team1: "W" if score1 > score2 else "L",
            team2: "W" if score2 > score1 else "L"
        }
    else:
        team_wins = {tid: None for tid in team_ids}  # fallback if weird data

    # Final team stats dictionary
    team_stats = {
        tid: {
            "PTS": team_scores.get(tid),
            "WL": team_wins.get(tid)
        }
        for tid in team_ids
    }


    # Match rows between trad and adv, and clean
    merged = pd.merge(trad_df, adv_df, on="PLAYER_ID", suffixes = ("_trad", "_adv"))

    # Drop only metadata columns from `adv_df`, keep all `E_*` metrics
    cols_to_drop = [
    'GAME_ID_adv', 'TEAM_ID_adv', 'TEAM_ABBREVIATION_adv', 'TEAM_CITY_adv',
    'PLAYER_NAME_adv', 'NICKNAME_adv', 'START_POSITION_adv', 'COMMENT_adv',
    'MIN_adv', 'PACE_PER40', 'POSS'
    ]
    merged = merged.drop(columns=[col for col in cols_to_drop if col in merged.columns])

    # Rename suffixes for trad columns
    rename_map = {
        "GAME_ID_trad": "GAME_ID",
        "TEAM_ID_trad": "TEAM_ID",
        "TEAM_ABBREVIATION_trad": "TEAM_ABBREVIATION",
        "TEAM_CITY_trad": "TEAM_CITY",
        "PLAYER_NAME_trad": "PLAYER_NAME",
        "NICKNAME_trad": "NICKNAME",
        "START_POSITION_trad": "START_POSITION",
        "COMMENT_trad": "COMMENT",
        "MIN_trad": "MIN"
    }
    merged = merged.rename(columns={k: v for k, v in rename_map.items() if k in merged.columns})

    box_score_cards = []

    for _, row in merged.iterrows():
        name = row.get("PLAYER_NAME")
        team_id = row.get("TEAM_ID")

        if not name or pd.isna(name):
            print(f"⚠️ Missing PLAYER_NAME for game {game_id}, row skipped.")
            print(row.to_dict())
            continue

        # 🧠 Parse opponent team from MATCHUP (e.g. "LAL @ DEN" → "DEN")
        matchup = row.get("MATCHUP", "")
        parts = matchup.split(" ")
        opponent_abbr = parts[-1] if len(parts) >= 3 else "UNK"
        home_game = "vs." in matchup

        # 🟦 Scores + Win/Loss
        opponent_id = [tid for tid in team_ids if tid != team_id][0] if team_id in team_ids and len(team_ids) == 2 else None
        team_info = team_stats.get(team_id, {})
        opponent_info = team_stats.get(opponent_id, {})
        row = row.where(pd.notnull(row), None)

        card = BoxScoreCard(
            game_id=game_id,
            game_date=game_date,
            player_name=name,
            player_id=row["PLAYER_ID"],
            team=row["TEAM_ABBREVIATION"],
            opponent=opponent_abbr,

            # Basic stats
            min=row["MIN"],
            fgm=row["FGM"], fga=row["FGA"],
            fg3m=row["FG3M"], fg3a=row["FG3A"],
            ftm=row["FTM"], fta=row["FTA"],
            oreb=row["OREB"], dreb=row["DREB"], reb=row["REB"],
            ast=row["AST"], stl=row["STL"], blk=row["BLK"],
            to=row["TO"], pf=row["PF"], pts=row["PTS"],
            plus_minus=row["PLUS_MINUS"],

            # Advanced stats (both regular and estimated)
            off_rating=row["OFF_RATING"],
            def_rating=row["DEF_RATING"],
            net_rating=row["NET_RATING"],
            ast_pct=row["AST_PCT"],
            ast_tov=row["AST_TOV"],
            ast_ratio=row["AST_RATIO"],
            oreb_pct=row["OREB_PCT"],
            dreb_pct=row["DREB_PCT"],
            reb_pct=row["REB_PCT"],
            tm_tov_pct=row["TM_TOV_PCT"],
            efg_pct=row["EFG_PCT"],
            ts_pct=row["TS_PCT"],
            usg_pct=row["USG_PCT"],
            pace=row["PACE"],
            pie=row["PIE"],

            # Summary
            is_home_game=home_game,
            wl=team_info.get("WL"),
            team_score=team_info.get("PTS"),
            opponent_score=opponent_info.get("PTS")
        )

        box_score_cards.append(card)

    return box_score_cards


def get_team_roster(team_name: str, season: str):
    team_list = teams.find_teams_by_full_name(team_name)
    if not team_list:
        raise ValueError(f"Team '{team_name}' not found")

    team_id = team_list[0]["id"]

    time.sleep(random.uniform(0.5, 1.0))

    # Fetch all games played by the team
    games_df = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=team_id,
        player_or_team_abbreviation='P'
    ).get_data_frames()[0]

    if games_df.empty:
        raise ValueError(f"No NBA games found for team '{team_name}'")

    # Convert to correct SEASON_ID format, e.g. "2024-25" → "22024"
    start_year = int(season[:4])
    season_id = f"2{start_year}"

    games_df = games_df[games_df["SEASON_ID"] == season_id]

    if games_df.empty:
        raise ValueError(f"No NBA games for team '{team_name}' in season {season}")

    # Get all players who played in any of those games
    player_names = games_df["PLAYER_NAME"].dropna().unique().tolist()

    return player_names



def get_team_card(name: str, season: str):
    # Search for team by full name
    #[{'id': 1610612744, 'full_name': 'Golden State Warriors', 'abbreviation': 'GSW', 'nickname': 'Warriors', 'city': 'Golden State', 'state': 'California', 'year_founded': 1946}]
    team_list = teams.find_teams_by_full_name(name)
    if not team_list:
        raise ValueError(f"Team '{name}' not found")
    
    # First matching result
    team = team_list[0]
    team_id = team['id']

    team_info = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id).get_data_frames()[0]
    team_common = teaminfocommon.TeamInfoCommon(team_id=team_id).get_data_frames()[0]

    # Check for missing data
    filtered = team_info[team_info["YEAR"] == season]
    if filtered.empty:
        raise ValueError(f"No data for team '{name}' in season {season}")
    target_season = filtered.iloc[0]
    
    city = target_season["TEAM_CITY"]
    full_team_name = team['full_name']
    abbreviation = team_common.iloc[0]["TEAM_ABBREVIATION"]
    # conference = target_common["TEAM_CONFERENCE"]
    # division = target_common["TEAM_DIVISION"]
    wins = int(target_season["WINS"])
    losses = int(target_season["LOSSES"])
    win_pct = round(float(target_season["WIN_PCT"]), 3)

    # Don't wanna get banned
    time.sleep(random.uniform(0.6, 1.2)) 

    return {
        "team_id": team_id,
        "city": city,
        "name": full_team_name,
        "abbreviation": abbreviation,
        # "conference": conference,
        # "division": division,
        "season": season,
        "wins": wins,
        "losses": losses,
        "win_pct": win_pct
    }

def get_player_card(name: str, season: str, teamabr: str, db):
    # Search for the player by full name
    player_list = players.find_players_by_full_name(name)
    if not player_list:
        raise ValueError(f"Player '{name}' not found")

    # Take the first matching result
    player = player_list[0]
    player_id = player['id']


    # Fetch player info (contains position, team, birthdate, weight, height, etc.)
    info_df = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
    position = info_df.loc[0, "POSITION"]
    height = info_df.loc[0, "HEIGHT"]
    weight = info_df.loc[0, "WEIGHT"]

    # Calculate inches in height for other processing
    raw_height = height
    if "-" in raw_height:
        feet, inches = map(int, raw_height.split("-"))
        height_inches = round(feet * 12 + inches, 1)
    else:
        height_inches = None  


    # Specific Season Stats
    stats_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]

    # Check for missing data
    target_season = stats_df[stats_df["SEASON_ID"] == season]
    target_season = target_season[target_season["TEAM_ABBREVIATION"]==teamabr]

    if target_season.empty:
        raise ValueError(f"No stats for '{name}' in season {season}")
    target_season = target_season.iloc[0]

    # Lookup team name
    team_id = target_season["TEAM_ID"]
    team = next(
        (t["full_name"] for t in teams.get_teams() if t["id"] == team_id), 
        target_season["TEAM_ABBREVIATION"]
    )
    games_played = target_season["GP"] or 1

    current_team = get_current_team(player_id, db)

    # Don't wanna get banned
    time.sleep(random.uniform(0.6, 1.2)) 

    return {
        "player_id": player_id,
        "name": player['full_name'],
        "season": season,
        "team": team,
        "current_team": current_team,
        "position": position,
        "height": height,
        "height_inches": height_inches,
        "weight": weight,
        "ppg": float(round(target_season["PTS"]/games_played, 1)),
        "rpg": float(round(target_season["REB"]/games_played, 1)),
        "apg": float(round(target_season["AST"]/games_played, 1)),
        "blk": float(round(target_season["BLK"]/games_played, 1)),
        "stl": float(round(target_season["STL"]/games_played, 1)),
        "tov": float(round(target_season["TOV"]/games_played, 1))
    }

def get_current_nba_season():
    today = date.today()
    year = today.year
    if today.month >= 10:  # New season starts in October
        return f"{year}-{str(year + 1)[-2:]}"
    else:  # Still in previous season
        return f"{year - 1}-{str(year)[-2:]}"
