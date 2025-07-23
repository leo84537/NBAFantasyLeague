import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import BoxScoreSummaryV2, BoxScoreAdvancedV2, BoxScoreTraditionalV2,playercareerstats, commonplayerinfo,leaguegamefinder, teaminfocommon, teamyearbyyearstats, commonteamroster
from services.nba_api_methods import get_team_roster
def test_api():
    team_name = "Philadelphia 76ers"
    print(get_team_roster(team_name, "2024-25"))
    
    player = players.find_players_by_full_name("Kevin Durant")
    player_list = player[0]
    player_id = player_list["id"]
    #0022401181
    #0022401185
    game_id = "0022401181"
    trad_df = BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[1]
    adv_df = BoxScoreAdvancedV2(game_id=game_id).get_data_frames()[0]
    summary_df = BoxScoreSummaryV2(game_id=game_id).get_data_frames()[0]
    # print(trad_df)
    # merged = pd.merge(trad_df, adv_df, on="PLAYER_ID", suffixes=("_trad", "_adv"))
    # merged = merged.rename(columns={
    #     "GAME_ID_trad": "GAME_ID",
    #     "TEAM_ID_trad": "TEAM_ID",
    #     "TEAM_ABBREVIATION_trad": "TEAM_ABBREVIATION",
    #     "TEAM_CITY_trad": "TEAM_CITY",
    #     "PLAYER_NAME_trad": "PLAYER_NAME",
    #     "NICKNAME_trad": "NICKNAME",
    #     "START_POSITION_trad": "START_POSITION",
    #     "COMMENT_trad": "COMMENT",
    #     "MIN_trad": "MIN"
    # })
    # print(merged.columns)

    stats_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    basic = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]

    stats_df = stats_df.sort_values("SEASON_ID", ascending=False)
    stats_df = stats_df[stats_df["TEAM_ABBREVIATION"] != "TOT"]
    
    # Find most recent team
    most_recent = stats_df.iloc[0]
    
    season = most_recent["SEASON_ID"]
    teamabr = most_recent["TEAM_ABBREVIATION"]
    
    # print(stats_df)

    # roster_df = commonteamroster.CommonTeamRoster(team_id=1610612744).get_data_frames()[0]
    #target = roster_df[roster_df["SEASON"]== "2015-16"]
    #print(roster_df["SEASON"])

    finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=1610612744, season_nullable="2015-16", player_or_team_abbreviation='P').get_data_frames()[0]
    # target = finder[finder["SEASON_ID"]== "22015"]

    #print(finder["TEAM_NAME"])


    #GSW
    team_id = 1610612744
    bruh = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=team_id,
        player_or_team_abbreviation='P'
    ).get_data_frames()[0]
    # print(bruh[bruh["SEASON_ID"]=="22024"])
    #common info only gets recent season
    team_info = teaminfocommon.TeamInfoCommon(team_id=team_id).get_data_frames()[0]
    # print(team_info.columns)
    # print(team_info["TEAM_DIVISION"])

    season1 = "2015-16"
    team_name = "Atlanta Hawks"
    team = teams.find_teams_by_full_name(team_name)
    # print(team)
    id = team[0]["id"]
    team_info = teaminfocommon.TeamInfoCommon(team_id=id).get_data_frames()[0]
    filtered = team_info[team_info["SEASON_YEAR"] == season1]
    #print(team_info)
    #print(team_info.iloc[0]["TEAM_ABBREVIATION"])

    
    moreteam = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id).get_data_frames()[0]
    # print(moreteam.columns)
    #print(moreteam["TEAM_NAME"])
    target_season = moreteam[moreteam["YEAR"] == "2015-16"].iloc[0] 
    # print(target_season)

    #print(teams.find_teams_by_full_name("Golden State Warriors")[0]["full_name"])
    
    
    

    # print(stats.get_data_frames()[0])
    #print(basic.get_data_frames()[0]["TEAM_NAME"])

test_api()
