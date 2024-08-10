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

# if __name__ == "__main__":
#     upload_data_to_mongodb('data')
    # print(last_match_id())
