import os
import sys
import requests
import pandas as pd
import tkinter as tk
import requests
import tkinter as tk
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
    if relative_path == "version.txt":
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return os.path.join(os.path.abspath("."), relative_path)
    return os.path.join(user_data_dir, relative_path)

message_templates_path = resource_path('message_templates.csv')
solucionadores_path = resource_path('solucionadores.csv')
version_path = resource_path("version.txt")

# Verifica se os arquivos existem no diretório de dados do usuário; caso contrário, copia ou cria
if not os.path.exists(user_templates_path):
    if os.path.exists(message_templates_path):
        shutil.copy(message_templates_path, user_templates_path)
    else:
        pd.DataFrame(columns=["Template", "Message"]).to_csv(user_templates_path, index=False)
else:
    print(f"O arquivo {user_templates_path} já existe. Nenhuma ação de cópia será realizada.")

if not os.path.exists(user_groups_path):
    if os.path.exists(solucionadores_path):
        shutil.copy(solucionadores_path, user_groups_path)
    else:
        pd.DataFrame(columns=["Grupo"]).to_csv(user_groups_path, index=False)
else:
    print(f"O arquivo {user_groups_path} já existe. Nenhuma ação de cópia será realizada.")

def load_templates():
    try:
        return pd.read_csv(user_templates_path)
    except Exception as e:
        print(f"Erro ao carregar templates: {e}")
        return pd.DataFrame(columns=["Template", "Message", "Obrigatório"])  # Retorna um DataFrame vazio

def load_groups():
    try:
        return pd.read_csv(user_groups_path)
    except Exception as e:
        print(f"Erro ao carregar grupos: {e}")
        return pd.DataFrame(columns=["Grupo"])  # Retorna um DataFrame vazio

# Verificar versão e baixar atualização
def check_for_update(root, version_label):
    version_url = "https://raw.githubusercontent.com/Nai-nailinha/MensagemPadrao/master/version.txt"
    download_url = "https://github.com/Nai-nailinha/MensagemPadrao/releases/latest/download/MensagemPadraoSetup.exe"

    version_label.grid(row=20, column=0, padx=10, pady=5)

    try:
        with open(version_path, 'r') as f:
            current_version = f.read().strip()

        response = requests.get(version_url, timeout=30)  # Timeout de 10 segundos
        if response.status_code == 200:
            latest_version = response.text.strip()

            # Função para comparar versões
            def compare_versions(current_version, latest_version):
                current_version_parts = [int(part) for part in current_version.split('.')]
                latest_version_parts = [int(part) for part in latest_version.split('.')]

                # Comparar versões parte por parte (major, minor, patch)
                return latest_version_parts > current_version_parts

            # Verifica se a nova versão é maior
            if compare_versions(current_version, latest_version):
                version_label.config(text=f"Nova versão disponível: {latest_version}.", fg="red")

                # Checar se o botão de download já existe e não duplicá-lo
                if not hasattr(root, 'download_button'):
                    root.download_button = tk.Button(root, text="Baixar Atualização",
                                                     command=lambda: download_update(download_url, version_label))
                    root.download_button.grid(row=21, column=0, padx=10, pady=10)
            else:
                version_label.config(text=f"Versão atual: {current_version}", fg="green")
        else:
            version_label.config(text="Erro ao verificar a versão. Código: " + str(response.status_code), fg="red")

    except requests.exceptions.Timeout:
        version_label.config(text="Erro: Tempo limite esgotado ao tentar verificar atualização.", fg="red")
    except requests.exceptions.RequestException as e:
        version_label.config(text=f"Erro ao verificar atualização: {e}", fg="red")
    except Exception as e:
        version_label.config(text=f"Erro ao verificar atualização: {str(e)}", fg="red")

# Função para baixar a atualização (mantém o rótulo de download como está)
def download_update(download_url, update_label):
    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            setup_path = os.path.join(user_data_dir, 'MensagemPadraoSetup.exe')
            with open(setup_path, 'wb') as f:
                f.write(response.content)

            update_label.config(text="Atualização Baixada. Execute o instalador para concluir.", fg="green")

            if os.name == 'nt':  # Executa apenas no Windows
                os.startfile(setup_path)
        else:
            update_label.config(text="Erro ao baixar a atualização. Código: " + str(response.status_code), fg="red")
    except Exception as e:
        update_label.config(text=f"Erro ao baixar a atualização: {str(e)}", fg="red")

