from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo

def get_player_card(name: str):
    # Search for the player by full name
    player_list = players.find_players_by_full_name(name)
    if not player_list:
        raise ValueError(f"Player '{name}' not found")

    # Take the first matching result
    player = player_list[0]
    player_id = player['id']

    # Fetch player info (like position, team, birthdate, weight, height)
    info_df = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
    team = info_df.loc[0, "TEAM_NAME"]
    position = info_df.loc[0, "POSITION"]
    height = info_df.loc[0, "HEIGHT"]
    weight = info_df.loc[0, "WEIGHT"]
    # First entry of list is seasonal performance (chrono order 2003-2025)
    stats_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    latest_season = stats_df.iloc[-1]

    return {
        "name": player['full_name'],
        "height": height,
        "weight": weight,
        "team": team,
        "position": position,
        "ppg": round(latest_season["PTS"]/latest_season["GP"], 1),
        "rpg": round(latest_season["REB"]/latest_season["GP"], 1),
        "apg": round(latest_season["AST"]/latest_season["GP"], 1),
        "blk": round(latest_season["BLK"]/latest_season["GP"], 1),
        "stl": round(latest_season["STL"]/latest_season["GP"], 1),
        "tov": round(latest_season["TOV"]/latest_season["GP"], 1)
    }
