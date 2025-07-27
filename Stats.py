from dotenv import load_dotenv
load_dotenv()

import os 
import requests 

import pandas as pd 

api_key = os.getenv('riot_API_key')


def get_puuid(summonerID = None, gameName = None, riotTag = None, region = 'americas'):
    """Gets user(Puuid) from a SummonerID or riot ID and the tag associated with the account 
    
    Args: 
        summonerID (str, optional): The Summoner ID; defaults to None/Empty
        gameName (str, optional): Riot ID of the account; defaults to None/Empty
        RiotTag (str, optional): Riot Tag; defaults to None/Empty
        region(str, optional): Region of the account; default is "Americas" 

    Returns: 
        str: puuid
    """
    if summonerID is not None: 
        root_url = f'https://{region}.api.riotgames.com/'
        endpoint = 'lol/summoner/v4/summoners/'
        print(root_url + endpoint + summonerID + '?api_key-' + api_key)

        return response.json()['puuid']
    else:
        root_url = f'https://{region}.api.riotgames.com/'
        endpoint = f'riot/account/v1/accounts/by-riot-id/{gameName}/{riotTag}'

        response = requests.get(root_url + endpoint + '?api_key=' + api_key)
        
        return response.json()['puuid']

def get_idtag_from_puuid(puuid = None): 

    """Gets the riot ID and Riot Tag from puuid 
    
    Args: 
        puuid(str, optional): puuid. Defaults to None 

    Returns: 
        id (dict): Dictionary with riot ID and riot Tag
    """
    root_url = 'https://americas.api.riotgames.com/'
    endpoint = 'riot/account/v1/accounts/by-puuid/'

    response = requests.get(root_url + endpoint + puuid + '?api_key=' + api_key)

    id = {
        'gameNameTag':response.json()['gameNameTag'],
        'riotTag': response.json()['riotTag']
    }

    return id

def get_Ladder(top = 300):
    """Gets the top x players in solo queue
    Args:
        top(int, optional): Number of players to return. Default = 300 as there is 300 challengers at any given moment.

    Returns:
        DataFrame: returns a dataFram of the top n players in solo queue 
    """

    root_url = 'https://na1.api.riotgames.com/'
    challenger = 'lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
    grandmaster = 'lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5'
    master = 'lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5'

    chall_response = requests.get(root_url + challenger + '?api_key=' + api_key)
    chall_df = pd.DataFrame(chall_response.json()['entries']).sort_values('leaguePoints', ascending= False).reset_index(drop=True)

    gm_df = pd.DataFrame()
    masta_df = pd.DataFrame()
    
    if top > 300:
        gm_response = requests.get(root_url + grandmaster + '?api_key=' + api_key)
        gm_df = pd.DataFrame(gm_response.json()['entries']).sort_values('leaguePoints', ascending=False).reset_index(drop=True)
    if top > 1000:
        masta_response = requests.get(root_url + master + '?api_key=' + api_key)
        masta_df = pd.DataFrame(masta_response.json()['entries']).sort_values('leaguePoints', ascending=False).reset_index(drop=True)
    
    df = pd.concat([chall_df, gm_df, masta_df]).reset_index(drop=True)[:top]

    df = df.reset_index().drop(columns = ['rank']).rename(columns={'index' : 'rank'})
    df['rank'] += 1

    return df 

def get_match_history(region=None, puuid=None, start=0, count=20): 
    root_url = f'https://{region}.api.riotgames.com'
    endpoint = f'/lol/match/v5/matches/by-puuid/{puuid}/ids'
    query_params = f'?start={start}&count={count}'

    print(f"Using API Key: {api_key}")  # Debug line

    response = requests.get(root_url + endpoint + query_params + '&api_key=' + api_key)

    return response.json()


def get_match_data_from_id(region = None, matchId = None):

    root_url = f'https://{region}.api.riotgames.com'
    endpoint = f'/lol/match/v5/matches/{matchId}'
    print(root_url + endpoint + '?api_key=' + api_key)
    response = requests.get(root_url + endpoint + '?api_key=' + api_key)

    return response.json()

def process_match_json(match_json, puuid):
    """Processes the match json into a dataframe.

    Args:
        match_json (dict): Match JSON.
        puuid (str): Player's puuid.

    Returns:
        dataframe: Dataframe of the processed match data.
    """
    side_dict = {
        100:'blue',
        200:'red'
    }

    try:
        info = match_json['info']


        metadata = match_json['metadata']
        matchId = metadata['matchId']
        participants = metadata['participants']

        player = info['participants'][participants.index(puuid)]

        gameCreation = info['gameCreation']
        gameStartTimestamp = info['gameStartTimestamp']
        gameEndTimestamp = info['gameEndTimestamp']
        timePlayed = (gameEndTimestamp-gameStartTimestamp)/1000
        gameMode = info['gameMode']
        gameVersion = info['gameVersion']
        platformId = info['platformId']
        queueId = info['queueId']
        puuid = player['puuid']
        riotIdGameName = player['summonerName']
        try:
            riotIdTagLine = player['riotIdTagline']
        except:
            riotIdTagLine = ''
        side = side_dict[player['teamId']]
        win = player['win']

        champion = player['championName']
        kills = player['kills']
        deaths = player['deaths']
        assists = player['assists']
        summOne = player['summoner1Id']
        summTwo = player['summoner2Id']
        earlySurrender = player['gameEndedInEarlySurrender']
        surrender = player['gameEndedInSurrender']
        firstBlood = player['firstBloodKill']
        firstBloodAssist = player['firstBloodAssist']
        firstTower = player['firstTowerKill']
        firstTowerAssist = player['firstTowerAssist']
        dragonKills = player['dragonKills']

        damageDealtToBuildings = player['damageDealtToBuildings']
        damageDealtToObjectives = player['damageDealtToObjectives']
        damageSelfMitigated = player['damageSelfMitigated']
        goldEarned = player['goldEarned']
        teamPosition = player['teamPosition']
        lane = player['lane']
        largestKillingSpree = player['largestKillingSpree']
        longestTimeSpentLiving = player['longestTimeSpentLiving']
        objectivesStolen = player['objectivesStolen']
        totalMinionsKilled = player['totalMinionsKilled']
        totalAllyJungleMinionsKilled = player['totalAllyJungleMinionsKilled']
        totalEnemyJungleMinionsKilled = player['totalEnemyJungleMinionsKilled']
        totalNeutralMinionsKilled = totalAllyJungleMinionsKilled + totalEnemyJungleMinionsKilled
        totalDamageDealtToChampions = player['totalDamageDealtToChampions']
        totalDamageShieldedOnTeammates = player['totalDamageShieldedOnTeammates']
        totalHealsOnTeammates = player['totalHealsOnTeammates']
        totalDamageTaken = player['totalDamageTaken']
        totalTimeCCDealt = player['totalTimeCCDealt']
        totalTimeSpentDead = player['totalTimeSpentDead']
        turretKills = player['turretKills']
        turretsLost = player['turretsLost']
        visionScore = player['visionScore']
        controlWardsPlaced = player['detectorWardsPlaced']
        wardsKilled = player['wardsKilled']
        wardsPlaced = player['wardsPlaced']

        item0 = player['item0']
        item1 = player['item1']
        item2 = player['item2']
        item3 = player['item3']
        item4 = player['item4']
        item5 = player['item5']
        item6 = player['item6']

        perks = player['perks']

        perkKeystone = perks['styles'][0]['selections'][0]['perk']
        perkPrimaryRow1 = perks['styles'][0]['selections'][1]['perk']
        perkPrimaryRow2 = perks['styles'][0]['selections'][2]['perk']
        perkPrimaryRow3 = perks['styles'][0]['selections'][3]['perk']
        perkPrimaryStyle = perks['styles'][0]['style']
        perkSecondaryRow1 = perks['styles'][1]['selections'][0]['perk']
        perkSecondaryRow2 = perks['styles'][1]['selections'][1]['perk']
        perkSecondaryStyle = perks['styles'][1]['style']
        perkShardDefense = perks['statPerks']['defense']
        perkShardFlex = perks['statPerks']['flex']
        perkShardOffense = perks['statPerks']['offense']


        matchDF = pd.DataFrame({
            'match_id': [matchId],
            'participants': [participants],
            'game_creation': [gameCreation],
            'game_start_timestamp': [gameStartTimestamp],
            'game_end_timestamp': [gameEndTimestamp],
            'game_version': [gameVersion],
            'queue_id': [queueId],
            'game_mode': [gameMode],
            'platform_id': [platformId],
            'puuid': [puuid],
            'riot_id': [riotIdGameName],
            'riot_tag': [riotIdTagLine],
            'time_played': [timePlayed],
            'side': [side],
            'win': [win],
            'team_position': [teamPosition],
            'lane': [lane],
            'champion': [champion],
            'kills': [kills],
            'deaths': [deaths],
            'assists': [assists],
            'summoner1_id': [summOne],
            'summoner2_id': [summTwo],
            'gold_earned': [goldEarned],
            'total_minions_killed': [totalMinionsKilled],
            'total_neutral_minions_killed': [totalNeutralMinionsKilled],
            'total_ally_jungle_minions_killed': [totalAllyJungleMinionsKilled],
            'total_enemy_jungle_minions_killed': [totalEnemyJungleMinionsKilled],
            'early_surrender': [earlySurrender],
            'surrender': [surrender],
            'first_blood': [firstBlood],
            'first_blood_assist': [firstBloodAssist],
            'first_tower': [firstTower],
            'first_tower_assist': [firstTowerAssist],
            'damage_dealt_to_buildings': [damageDealtToBuildings],
            'turret_kills': [turretKills],
            'turrets_lost': [turretsLost],
            'damage_dealt_to_objectives': [damageDealtToObjectives],
            'dragonKills': [dragonKills],
            'objectives_stolen': [objectivesStolen],
            'longest_time_spent_living': [longestTimeSpentLiving],
            'largest_killing_spree': [largestKillingSpree],
            'total_damage_dealt_champions': [totalDamageDealtToChampions],
            'total_damage_taken': [totalDamageTaken],
            'total_damage_self_mitigated': [damageSelfMitigated],
            'total_damage_shielded_teammates': [totalDamageShieldedOnTeammates],
            'total_heals_teammates': [totalHealsOnTeammates],
            'total_time_crowd_controlled': [totalTimeCCDealt],
            'total_time_spent_dead': [totalTimeSpentDead],
            'vision_score': [visionScore],
            'wards_killed': [wardsKilled],
            'wards_placed': [wardsPlaced],
            'control_wards_placed': [controlWardsPlaced],
            'item0': [item0],
            'item1': [item1],
            'item2': [item2],
            'item3': [item3],
            'item4': [item4],
            'item5': [item5],
            'item6': [item6],
            'perk_keystone': [perkKeystone],
            'perk_primary_row_1': [perkPrimaryRow1],
            'perk_primary_row_2': [perkPrimaryRow2],
            'perk_primary_row_3': [perkPrimaryRow3],
            'perk_secondary_row_1': [perkSecondaryRow1],
            'perk_secondary_row_2': [perkSecondaryRow2],
            'perk_primary_style': [perkPrimaryStyle],
            'perk_secondary_style': [perkSecondaryStyle],
            'perk_shard_defense': [perkShardDefense],
            'perk_shard_flex': [perkShardFlex],
            'perk_shard_offense': [perkShardOffense],
        })
    
        return matchDF
    except:
        return pd.DataFrame()

def get_stored_matches(): 
    '''gets stored data that is already in the data base. (most recent matches for given player)'''

    #need SQL on laptop cannot do it right now. 





#testing the functions: prints out a table of different values of runes and such but without any context (i.e. rune names and stuff)

#print(get_match_history(region = 'americas', puuid= 'ParV2EB9IEOAPSyGumCFmbdPfVXawhGTrePL9HRSY7er6i3c2UAqgvRYxPdXPchGX9Y1l5y6cemDCw'))
#game = get_match_data_from_id(region = 'americas', matchId= 'NA1_5216932918')
match_ids = get_match_history(region = 'americas', puuid = 'ParV2EB9IEOAPSyGumCFmbdPfVXawhGTrePL9HRSY7er6i3c2UAqgvRYxPdXPchGX9Y1l5y6cemDCw')

df = pd.DataFrame()
for match_id in match_ids:
    game = get_match_data_from_id(region = 'americas', matchId=match_id)
    matchDF = process_match_json(game, puuid= 'ParV2EB9IEOAPSyGumCFmbdPfVXawhGTrePL9HRSY7er6i3c2UAqgvRYxPdXPchGX9Y1l5y6cemDCw')

    df = pd.concat([df,matchDF])

#print(df)


def json_extract(obj, key):
    arr = []
    #looks through dictionary and all key-value pairing in the dicttionary 
    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k,v in obj.items():
                #if the key is the key that we are looking for then give value
                if k == key:
                    arr.append(v)
                #if not then check another dicitionary, if it is, recursion 
                elif isinstance(v,(dict,list)):
                    extract(v,arr,key)
        #does the same thing for the list of all the dictionaries 
        elif isinstance(obj, list):
            for item in obj:
                extract(item,arr,key)
        
        return arr 
    #extract original dictionary that was input, list of dictionaries and then return 
    values = extract(obj,arr,key)
    return values


#Test json_extract 
perk = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json'
perk_style = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perkstyles.json'

perk_json = requests.get(perk).json()
perk_style_json = requests.get(perk_style).json()

perk_ids = json_extract(perk_json, 'id')
perk_names = json_extract(perk_json, 'name')

perk_dict = dict(map(lambda i, j : (int(i),j), perk_ids, perk_names))

perk_style_ids = json_extract(perk_style_json, 'id')
perk_style_names = json_extract(perk_style_json, 'name')

perk_style_dict = dict(map(lambda i, j: (int(i), j), perk_style_ids, perk_style_names))

pd.options.display.max_columns = 100
pd.options.display.max_rows = 100
print(df.replace(perk_dict).replace(perk_style_dict))


