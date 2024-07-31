import time
import subprocess
import logging

LOG_FILE = 'log/run_bot.log'
INTERVALO_VERIFICACAO = 180

# Configuração de logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def executar_verificacao():
    resultado_verificacao = subprocess.run(['python', 'check_new_match.py'], capture_output=True, text=True)
    logging.info(resultado_verificacao.stdout)

    if "Nova partida encontrada" in resultado_verificacao.stdout:
        resultado_processamento = subprocess.run(['python', 'process_match_data.py'], shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        logging.info(resultado_processamento.stdout)
        subprocess.run(['python', 'botDisc.py', resultado_processamento.stdout])

if __name__ == "__main__":
    while True:
        try:
            executar_verificacao()
        except Exception as e:
            logging.error(f"Erro ao executar verificação: {e}")
        time.sleep(INTERVALO_VERIFICACAO)
