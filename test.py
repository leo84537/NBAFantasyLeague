import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, teaminfocommon

def test_api():
    #lebron
    player_id = 2544
    stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    basic = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    #GSW
    team_id = 1610612744
    team_info = teaminfocommon.TeamInfoCommon(team_id=team_id)
    print(team_info.get_data_frames()[0])

    # print(stats.get_data_frames()[0])
    #print(basic.get_data_frames()[0]["TEAM_NAME"])

test_api()
