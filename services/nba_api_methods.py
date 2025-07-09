from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, teaminfocommon, teamyearbyyearstats

def get_team_card(name: str, season: str):
    # Search for team by full name
    team_list = teams.find_teams_by_full_name(name)
    if not team_list:
        raise ValueError(f"Team '{name}' not found")
    
    #First matching result
    team = team_list[0]
    team_id = team_id['id']
    team_info = teaminfocommon.TeamInfoCommon(team_id=team_id)[0]
    city = team_info.loc[0,"TEAM_CITY"]
    name = team_info.loc[0, "TEAM_NAME"]
    abbreviation = team_info.loc[0, "TEAM_ABBREVIATION"]
    conference = team_info.loc["TEAM_CONFERENCE"]
    division = team_info.loc[0,"TEAM_DIVISION"]
    wins = int(team_info.loc[0,"W"])
    losses = int(team_info.loc[0,"L"])
    win_pct = round(float(team_info.loc[0,"WIN_PCT"]), 3)

    season_start = season.split("-")[0] 

    return {
        
        "city": city,
        "name": name,
        "abbreviation": abbreviation,
        "conference": conference,
        "division": division,
        "season": season_start,
        "wins": wins,
        "losses": losses,
        "win_pct": win_pct
    }

def get_player_card(name: str, season: str):
    # Search for the player by full name
    player_list = players.find_players_by_full_name(name)
    if not player_list:
        raise ValueError(f"Player '{name}' not found")

    # Take the first matching result
    player = player_list[0]
    player_id = player['id']

    # Fetch player info (contains position, team, birthdate, weight, height, etc.)
    info_df = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
    team = info_df.loc[0, "TEAM_NAME"]
    position = info_df.loc[0, "POSITION"]
    height = info_df.loc[0, "HEIGHT"]
    weight = info_df.loc[0, "WEIGHT"]

    # First entry of list is seasonal performance (chrono order 2003-2025)
    stats_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    latest_season = stats_df.iloc[-1]

    season_start = season.split("-")[0] 

    return {
        "name": player['full_name'],
        "season": season_start,
        "team": team,
        "position": position,
        "height": height,
        "weight": weight,
        "ppg": round(latest_season["PTS"]/latest_season["GP"], 1),
        "rpg": round(latest_season["REB"]/latest_season["GP"], 1),
        "apg": round(latest_season["AST"]/latest_season["GP"], 1),
        "blk": round(latest_season["BLK"]/latest_season["GP"], 1),
        "stl": round(latest_season["STL"]/latest_season["GP"], 1),
        "tov": round(latest_season["TOV"]/latest_season["GP"], 1)
    }
