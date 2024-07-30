import json

# Supondo que o JSON esteja salvo em um arquivo chamado 'dados_partida.json'
nome_do_arquivo = 'data'

# Carregar o JSON do arquivo
with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

# IDs dos participantes específicos
id_participante_1 = "RIsZRVaNEiQsiuXoMmJAELbH9FCCt-jdKUsnlaXXKKrEgfVcdBuTtPO8EFhXf-ZgASkWL10P-KwPcA"
id_participante_2 = "3rrPAVHMa7h4T0Zr_vldEaSSF0KPj3-bgWKxip4gvQoXZA67Qrirgm_PblHJrMb0YUSaQvade8lJHQ"

# Acessar a lista de participantes dentro de 'info'
participantes = dados.get('info', {}).get('participants', [])

# Função para encontrar um participante pelo ID
def encontrar_participante_por_id(participants, participant_id):
    for participant in participants:
        if participant.get('puuid') == participant_id:
            return participant
    return None

# Encontrando os participantes pelos IDs
participante_1 = encontrar_participante_por_id(participantes, id_participante_1)
participante_2 = encontrar_participante_por_id(participantes, id_participante_2)

# Verificar se ambos os participantes foram encontrados
if participante_1 and participante_2:
    # Extrair o dano físico causado para ambos os participantes
    dano_fisico_1 = participante_1.get('physicalDamageDealt', 0)
    dano_fisico_2 = participante_2.get('physicalDamageDealt', 0)
    champion_1 = participante_1.get('championName', 0)
    champion_2 = participante_2.get('championName', 0)

    print(f'{champion_1}: {dano_fisico_1} and {champion_2}: {dano_fisico_2}')
    # print(f{"championName"})

    # Comparar os valores de dano físico
    if dano_fisico_1 > dano_fisico_2:
        print(f"O participante 1 causou mais dano físico: {dano_fisico_1}")
    elif dano_fisico_1 < dano_fisico_2:
        print(f"O participante 2 causou mais dano físico: {dano_fisico_2}")
    else:
        print("Ambos os participantes causaram a mesma quantidade de dano físico.")
else:
    print("Não foi possível encontrar um ou ambos os participantes pelos IDs fornecidos.")
