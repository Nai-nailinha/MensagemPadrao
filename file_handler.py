import os
import sys
import requests
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import shutil

# Definir o diretório para os arquivos de dados do usuário
if os.name == 'nt':  # Windows
    user_data_dir = os.path.join(os.getenv('APPDATA'), 'mensagemPadrao_data')
else:  # Linux/macOS
    user_data_dir = os.path.expanduser('~/.mensagemPadrao_data')

# Criar o diretório caso ele não exista
os.makedirs(user_data_dir, exist_ok=True)

# Caminho correto dos arquivos CSV no diretório de dados do usuário
user_templates_path = os.path.join(user_data_dir, 'message_templates.csv')
user_groups_path = os.path.join(user_data_dir, 'solucionadores.csv')

# Caminhos originais dos arquivos CSV no diretório de projeto

def resource_path(relative_path):
    # Quando o programa estiver empacotado com o PyInstaller, ele usa o atributo _MEIPASS
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # Quando estiver em desenvolvimento
    return os.path.join(os.path.abspath("."), relative_path)


message_templates_path = resource_path('message_templates.csv')
solucionadores_path = resource_path('solucionadores.csv')
# Caminho para os arquivos de versão e dados
version_path = resource_path("version.txt")

# Verifica se os arquivos existem no diretório de dados do usuário; caso contrário, copia ou cria
if not os.path.exists(user_templates_path):
    if os.path.exists(default_templates_path):
        shutil.copy(default_templates_path, user_templates_path)
    else:
        # Se o arquivo original não existir, crie um arquivo CSV vazio ou com dados padrão
        pd.DataFrame(columns=["Template", "Message"]).to_csv(user_templates_path, index=False)

if not os.path.exists(user_groups_path):
    if os.path.exists(default_groups_path):
        shutil.copy(default_groups_path, user_groups_path)
    else:
        # Se o arquivo original não existir, crie um arquivo CSV vazio ou com dados padrão
        pd.DataFrame(columns=["Grupo"]).to_csv(user_groups_path, index=False)

def load_templates():
    # Carrega o arquivo de templates do diretório de dados do usuário
    return pd.read_csv(user_templates_path)

def load_groups():
    # Carrega o arquivo de grupos do diretório de dados do usuário
    return pd.read_csv(user_groups_path)


def check_for_update(root):
    # URL para verificar a versão no GitHub
    version_url = "https://raw.githubusercontent.com/Nai-nailinha/MensagemPadrao/master/version.txt"
    download_url = "https://github.com/Nai-nailinha/MensagemPadrao/releases/latest/download/MensagemPadrao.exe"

    with open(version_path, 'r') as f:
        current_version = f.read().strip()

    try:
        response = requests.get(version_url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != current_version:
                # Oculta temporariamente a janela principal
                root.withdraw()

                update = messagebox.askyesno(
                    "Atualização Disponível",
                    f"Nova versão disponível: {latest_version}\nDeseja baixar e atualizar agora?"
                )

                # Restaura a janela principal após a verificação
                root.deiconify()

                if update:
                    new_exe_path = os.path.join(user_data_dir, "MensagemPadrao_new.exe")
                    response = requests.get(download_url)
                    with open(new_exe_path, 'wb') as f:
                        f.write(response.content)

                    messagebox.showinfo(
                        "Atualização Baixada",
                        "A nova versão foi baixada.\nPor favor, feche a aplicação atual e renomeie o arquivo 'MensagemPadrao_new.exe' para 'MensagemPadrao.exe'."
                    )
    except Exception as e:
        pass  # Ignore qualquer erro durante a verificação de atualização
