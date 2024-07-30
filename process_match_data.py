import json
import logging
import subprocess

# Configuração de logging
LOG_FILE = 'process_match_data.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Lista de IDs (puuid) dos amigos
ids_amigos = [
    "RIsZRVaNEiQsiuXoMmJAELbH9FCCt-jdKUsnlaXXKKrEgfVcdBuTtPO8EFhXf-ZgASkWL10P-KwPcA",
    "3rrPAVHMa7h4T0Zr_vldEaSSF0KPj3-bgWKxip4gvQoXZA67Qrirgm_PblHJrMb0YUSaQvade8lJHQ",
    ]

nome_do_arquivo = 'data'


# Carregar o JSON do arquivo
def carregar_dados_partida(nome_do_arquivo):
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
            dano_fisico = amigo.get('physicalDamageDealt', 0)

            amigos_info.append((puuid, nome_campeao, dano_fisico))

            if dano_fisico > maior_dano_fisico:
                maior_dano_fisico = dano_fisico
                melhor_amigo = amigo

        # Exibir o resultado do amigo com maior dano
        puuid_melhor_amigo = melhor_amigo.get('puuid')
        nick_melhor_amigo = melhor_amigo.get('riotIdGameName')
        nome_campeao_melhor_amigo = melhor_amigo.get('championName', 'Desconhecido')
        text = f"Quem que causou mais dano físico ({maior_dano_fisico}) foi o jogador {nick_melhor_amigo}, usando o campeão {nome_campeao_melhor_amigo}."

        # Exibir informações dos demais amigos
        for puuid, nome_campeao, dano_fisico in amigos_info:
            if puuid != puuid_melhor_amigo:
                text += f"\nE o {nick} feedou de {nome_campeao}, só deu {dano_fisico} de dano"
        logging.info(text)
        print(text)
        subprocess.run(['python', 'botDisc.py', text])
    else:
        print("Não há amigos suficientes na lista para comparação.")

if __name__ == "__main__":
    dados = carregar_dados_partida(nome_do_arquivo)
    if dados:
        process_data(dados)