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

# Caminhos completos para os arquivos CSV no diretório de dados do usuário
user_templates_path = os.path.join(user_data_dir, 'message_templates.csv')
user_groups_path = os.path.join(user_data_dir, 'solucionadores.csv')


# Caminhos dos arquivos originais no diretório do projeto
def resource_path(relative_path):
    # Se o arquivo for "version.txt", use o diretório do executável empacotado
    if relative_path == "version.txt":
        # Quando o programa estiver empacotado com o PyInstaller, use o diretório temporário (_MEIPASS)
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        # Quando estiver em desenvolvimento, use o diretório do projeto
        else:
            return os.path.join(os.path.abspath("."), relative_path)

    # Para todos os outros arquivos (como CSVs), use o diretório de dados do usuário
    return os.path.join(user_data_dir, relative_path)

message_templates_path = resource_path('message_templates.csv')
solucionadores_path = resource_path('solucionadores.csv')
version_path = resource_path("version.txt")

# Verifica se os arquivos existem no diretório de dados do usuário; caso contrário, copia ou cria
if not os.path.exists(user_templates_path):
    if os.path.exists(message_templates_path):
        # Só copia se o arquivo não existir
        shutil.copy(message_templates_path, user_templates_path)
else:
    # Se o arquivo já existir, carregue-o e certifique-se de que não seja sobrescrito
    print(f"O arquivo {user_templates_path} já existe. Nenhuma ação de cópia será realizada.")

if not os.path.exists(user_groups_path):
    print("O arquivo message_templates.csv não existe em APPDATA. Copiando o original.")
    if os.path.exists(solucionadores_path):
        shutil.copy(solucionadores_path, user_groups_path)
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
                # Abre janela de diálogo para confirmar a atualização
                update = messagebox.askyesno(
                    "Atualização Disponível",
                    f"Nova versão disponível: {latest_version}\nDeseja baixar e atualizar agora?"
                )

                if update:
                    # Código para baixar e atualizar a aplicação
                    new_exe_path = os.path.join(user_data_dir, "MensagemPadrao_new.exe")
                    response = requests.get(download_url)
                    with open(new_exe_path, 'wb') as f:
                        f.write(response.content)

                    messagebox.showinfo(
                        "Atualização Baixada",
                        "A nova versão foi baixada.\nPor favor, feche a aplicação atual e renomeie o arquivo 'MensagemPadrao_new.exe' para 'MensagemPadrao.exe'."
                    )
                    # Feche a aplicação após baixar
                    root.quit()
                else:
                    # Se o usuário clicar em "Não", apenas continua usando a versão atual
                    messagebox.showinfo("Continuar", "Você está usando a versão atual do aplicativo.")
                    return
    except Exception as e:
        pass  # Ignore qualquer erro durante a verificação da atualização

