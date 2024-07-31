import requests
import json

def get_summoner_id(api_key, summoner_name, tag, region):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}'
    headers = {'X-Riot-Token': api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['puuid']
    else:
        print(f"Erro ao obter Summoner ID: {response.status_code}")
        return None

def get_recent_matches(api_key, puuid, region):
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
    headers = {'X-Riot-Token': api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        matches = response.json()
        return matches
    else:
        print(f"Erro ao obter partidas recentes: {response.status_code}")
        return None

def get_match_details(api_key, matchId, region):
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}'
    headers = {'X-Riot-Token': api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter detalhes da partida: {response.status_code}")
        return None
