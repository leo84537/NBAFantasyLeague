from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
import pandas as pd

def test_api():
    #lebron
    player_id = 2544
    stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    basic = commonplayerinfo.CommonPlayerInfo(player_id=player_id)

    # print(stats.get_data_frames()[0])
    print(basic.get_data_frames()[0]["HEIGHT"])
test_api()
