import os
import sys
import requests
import pandas as pd

# Função para obter o caminho correto dos arquivos quando empacotado com PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Caminho para os arquivos CSV e de versão
message_templates_path = resource_path('message_templates.csv')
solucionadores_path = resource_path('solucionadores.csv')
version_path = resource_path('version.txt')

def check_for_update():
    version_url = "https://raw.githubusercontent.com/Nai-nailinha/MensagemPadrao/master/version.txt"
    try:
        with open(version_path, 'r') as f:
            current_version = f.read().strip()
        response = requests.get(version_url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != current_version:
                return True, latest_version
    except Exception:
        pass
    return False, None

def load_templates():
    return pd.read_csv(message_templates_path)

def load_groups():
    return pd.read_csv(solucionadores_path)
