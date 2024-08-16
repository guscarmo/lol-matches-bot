import json
import logging
from functions_mongodb import last_match_data

# Configuração de logging
LOG_FILE = 'log/process_match_data.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# Lista de IDs (puuid) dos amigos
ids_amigos = [
    "RIsZRVaNEiQsiuXoMmJAELbH9FCCt-jdKUsnlaXXKKrEgfVcdBuTtPO8EFhXf-ZgASkWL10P-KwPcA",
    'RJsFuBvBZsXp-dfsuqP_3oqJ9mSQ6OkKRdABaWDuiK87v-xeadwZ_iiXXwm80Vvxg_pLetDYpHjxtg',
    '3rrPAVHMa7h4T0Zr_vldEaSSF0KPj3-bgWKxip4gvQoXZA67Qrirgm_PblHJrMb0YUSaQvade8lJHQ',
    'txDisQ4j_ck-k1QrtZzHGvwK7QFp3940h_PeuV4crR4u7-BDnm_AUwO2yJfMkv7nqyIFr1xCIdkp-g',
    '0T8ntVGlPZeaDtidZ30PSG2uNiIBmmO58ycRkLjHwq3yJA_2URvZG5HqdYNj6UX3mFkRu-Zy6u2CuA'
    ]

match_info_json = 'temp_match_info.json'
nome_do_arquivo = 'data'

def check_new_match(match_info_json):
    try:
        match_info = load_json(match_info_json)
        if match_info.get("status") == "Nova partida encontrada":
            return True
    except FileNotFoundError:
        logging.error("Arquivo temp_match_info.json não encontrado")
    
def load_json(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        logging.error(f"Arquivo {nome_do_arquivo} não encontrado.")
        return None

def process_data(dados):
    text = ''
    participantes = dados.get('info', {}).get('participants', [])

    # Filtrar participantes que são amigos
    participantes_amigos = [p for p in participantes if p.get('puuid') in ids_amigos]

    if len(participantes_amigos) >= 2:
        maior_dano_fisico = 0
        melhor_amigo = None
        amigos_info = []

        for amigo in participantes_amigos:
            puuid = amigo.get('puuid')
            nick = amigo.get('riotIdGameName')
            nome_campeao = amigo.get('championName', 'Desconhecido')
            dano_fisico = amigo.get('totalDamageDealtToChampions', 0)

            amigos_info.append((puuid, nick, nome_campeao, dano_fisico))

            if dano_fisico > maior_dano_fisico:
                maior_dano_fisico = dano_fisico
                melhor_amigo = amigo

        # Exibir o resultado do amigo com maior dano
        puuid_melhor_amigo = melhor_amigo.get('puuid')
        nick_melhor_amigo = melhor_amigo.get('riotIdGameName')
        nome_campeao_melhor_amigo = melhor_amigo.get('championName', 'Desconhecido')
        text = f"Maior dano: ({maior_dano_fisico}) {nick_melhor_amigo}, de {nome_campeao_melhor_amigo}."

        # Exibir informações dos demais amigos
        for puuid, nick, nome_campeao, dano_fisico in amigos_info:
            if puuid != puuid_melhor_amigo:
                text += f"\nFeeder: {nick} {nome_campeao}, {dano_fisico} de dano"
        logging.info(text)
        with open('temp_match_result.txt', 'w', encoding='utf-8') as f:
            f.write(text)
    else:
        print("Não há amigos suficientes na lista para comparação.")

if __name__ == "__main__":
    new_match = check_new_match(match_info_json)
    if new_match:
        dados = last_match_data()
        if dados:
            process_data(dados)