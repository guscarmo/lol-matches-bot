import time
import subprocess
import logging
from process_match_data import load_json 

LOG_FILE = 'log/run_bot.log'
INTERVALO_VERIFICACAO = 50

# Configuração de logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def check_new_match(match_info_json):
    try:
        match_info = load_json(match_info_json)
        if match_info.get("status") == "Nova partida encontrada":
            return True
    except FileNotFoundError:
        logging.error("Arquivo temp_match_info.json não encontrado")

def executar_verificacao():
    resultado_verificacao = subprocess.run(['python', 'check_new_match.py'], capture_output=True, text=True)
    logging.info(resultado_verificacao.stdout)

    if check_new_match('temp_match_info.json'):
        resultado_processamento = subprocess.run(['python', 'process_match_data.py'], shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        logging.info(resultado_processamento.stdout)
        with open('temp_match_result.txt', 'r', encoding='utf-8') as f:
                mensagem = f.read().strip()
                if mensagem:
                    logging.info(f"Mensagem a ser enviada: {mensagem}")
                    comando = ['python', 'bot_send_message.py']
                    logging.info(f"Executando comando: {comando}")
                    resultado_envio = subprocess.run(comando, shell=True)
                    logging.info(f"Resultado do envio: {resultado_envio}")
                else:
                    logging.warning("A saída de 'process_match_data.py' está vazia. Nenhuma mensagem será enviada.")

if __name__ == "__main__":

    bot_process = subprocess.Popen(['python', 'botDisc.py'])

    while True:
        try:
            executar_verificacao()
        except Exception as e:
            logging.error(f"Erro ao executar verificação: {e}")
        time.sleep(INTERVALO_VERIFICACAO)
