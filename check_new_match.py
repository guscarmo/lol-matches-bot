import json
import logging
import os
from dotenv import load_dotenv
from functions_mongodb import last_match_id, upload_data_to_mongodb
from api_requests import get_summoner_id, get_recent_matches, get_match_details

load_dotenv()

API_KEY = os.getenv('API_KEY_RIOT')
REGION = 'americas'
SUMMONER_NAME = 'Gusbug'
TAG = 'BR1'
LOG_FILE = 'log/check_new_match.log'

def save_data(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)   

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

matches = []

puuid = get_summoner_id(API_KEY, SUMMONER_NAME, TAG, REGION)

last_matchId = last_match_id()

def get_matches_data():
    if puuid:
        recent_matches = get_recent_matches(API_KEY, puuid, REGION)
        if recent_matches:
            matchId = recent_matches[0]
            if last_matchId != matchId:
                match_details = get_match_details(API_KEY, matchId, REGION)
                if match_details:
                    result = {"status": "Nova partida encontrada", "matchId": matchId}
                    logging.info(result)
                    upload_data_to_mongodb(match_details)
                    save_data(result, 'temp_match_info.json')
                    return True
                else:
                    logging.error("Falha ao obter detalhes da partida.")
                    print("Erro ao obter detalhes da partida.")
            else:
                result = {"status": "Não há nova partida", "matchId": matchId}
                save_data(result, 'temp_match_info.json')
                logging.error(result)

if __name__ == "__main__":
    get_matches_data()