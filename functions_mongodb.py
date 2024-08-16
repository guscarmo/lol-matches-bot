import logging
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(filename='log/functions_mongodb.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def conectar_mongodb():
    try:
        mongo_uri = os.getenv('MONGO_URI')
        client = MongoClient(mongo_uri)
        db = client[os.getenv('MONGO_DBNAME')]
        collection = db[os.getenv('MONGO_COLLECTION')]
        logging.info("Conexão com MongoDB estabelecida.")
        return collection
    except Exception as e:
        logging.error(f"Erro ao conectar ao MongoDB: {e}")
        return None

def upload_data_to_mongodb(match_details):
    collection = conectar_mongodb()
    if collection is None:
        logging.error("A conexão com o MongoDB falhou. O processo será encerrado.")
        return

    try:        
        collection.insert_one(match_details)
        logging.info("Dados inseridos no MongoDB com sucesso.")
    except FileNotFoundError:
        logging.error("Arquivo 'data' não encontrado.")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Erro ao inserir dados no MongoDB: {e}")

def last_match_id():
    collection = conectar_mongodb()
    if collection is None:
        logging.error("A conexão com o MongoDB falhou. O processo será encerrado.")
        return None

    try:
        last_match = collection.find_one(sort=[('_id', pymongo.DESCENDING)])
        if last_match:
            return last_match.get('metadata', {}).get('matchId')
        else:
            logging.warning("Nenhum documento encontrado no MongoDB.")
            return None
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Erro ao consultar o MongoDB: {e}")
        return None
    
def last_match_data():
    collection = conectar_mongodb()
    if collection is None:
        logging.error("A conexão com o MongoDB falhou. O processo será encerrado.")
        return None
    
    try:
        last_match = collection.find_one(sort=[('_id', pymongo.DESCENDING)])
        if last_match:
            return last_match
        else:
            logging.warning("Nenhum documento encontrado no MongoDB.")
            return None
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Erro ao consultar o MongoDB: {e}")
        return None
    
def match_exists(matchId):
    collection = conectar_mongodb()
    if collection is None:
        logging.error("A conexão com o MongoDB falhou. O processo será encerrado.")
        return None
    
    match_exists = collection.find_one({"metadata.matchId": matchId})
    return match_exists


def summoner_highest_damage():
    collection = conectar_mongodb()
    if collection is None:
        logging.error("A conexão com o MongoDB falhou. O processo será encerrado.")
        return None
    
    summoner_puuids = [
    "RIsZRVaNEiQsiuXoMmJAELbH9FCCt-jdKUsnlaXXKKrEgfVcdBuTtPO8EFhXf-ZgASkWL10P-KwPcA",
    'RJsFuBvBZsXp-dfsuqP_3oqJ9mSQ6OkKRdABaWDuiK87v-xeadwZ_iiXXwm80Vvxg_pLetDYpHjxtg',
    '3rrPAVHMa7h4T0Zr_vldEaSSF0KPj3-bgWKxip4gvQoXZA67Qrirgm_PblHJrMb0YUSaQvade8lJHQ',
    'txDisQ4j_ck-k1QrtZzHGvwK7QFp3940h_PeuV4crR4u7-BDnm_AUwO2yJfMkv7nqyIFr1xCIdkp-g',
    '0T8ntVGlPZeaDtidZ30PSG2uNiIBmmO58ycRkLjHwq3yJA_2URvZG5HqdYNj6UX3mFkRu-Zy6u2CuA'
    ]

    pipeline = [
        {"$unwind": "$info.participants"},

        {
            "$match": {
                "info.participants.puuid": { "$in": summoner_puuids }
            }
        },

        { 
            "$group": {
                "_id": "$metadata.matchId",
                "maxDamageParticipant": { 
                    "$first": {
                        "damageDealt": { "$max": "$info.participants.totalDamageDealt" },
                        "puuid": "$info.participants.puuid",
                        "summonerName": "$info.participants.summonerName"
                    }
                }
            }
        },

        {
            "$group": {
                "_id": "$maxDamageParticipant.summonerName",
                "count": { "$sum": 1 }
            }
        },

        {
            "$sort": { "count": -1 }
        }
    ]

    result = collection.aggregate(pipeline)

    text = 'Top damage:'
    for doc in result:
        text += f"\n{doc['_id']} {doc['count']}"
    return text

if __name__ == "__main__":
    # upload_data_to_mongodb('data')
    print(summoner_highest_damage())
