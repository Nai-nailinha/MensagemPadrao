import tkinter as tk
from tkinter import messagebox, ttk

from numpy.ma.extras import row_stack

from file_handler import check_for_update, load_templates, load_groups, version_path
from message_utils import generate_message
from ui_components import setup_buttons, setup_text_widgets, setup_entry_fields, setup_action_buttons, copy_message
from template_manager import open_management_window, open_group_management_window
from file_handler import user_templates_path, user_groups_path
from PIL import Image, ImageTk

# Inicializa a interface principal
root = tk.Tk()
root.title("Mensagem Padrão")

# Definir estilo e tema
style = ttk.Style()
style.theme_use('clam')

import os
import sys
from PIL import Image


def get_resource_path(relative_path):
    """Obter o caminho correto do arquivo, dependendo se está empacotado ou não."""
    if getattr(sys, 'frozen', False):
        # O aplicativo está empacotado
        base_path = sys._MEIPASS
    else:
        # Modo de desenvolvimento
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Função para usar o ícone no Tkinter
def use_icon_in_app(root, ico_path):
    root.iconbitmap(ico_path)


# Caminho para o arquivo .ico
ico_output = get_resource_path("converted_icon.ico")

# Usar o ícone .ico no aplicativo
use_icon_in_app(root, ico_output)

# Defina a variável para controlar a verificação de atualizações
check_updates = True  # Altere para `True` quando quiser verificar atualizações

# Label para exibir informações de versão
version_label = tk.Label(root, text="Verificando versão...", fg="blue")
#version_label.grid(row=21, column=0, padx=10, pady=10, sticky='w')

# Verificação de atualizações
check_for_update(root, version_label)

# Carrega os dados dos arquivos CSV
df_templates = load_templates()
df_groups = load_groups()

# Lista de valores para o ComboBox de grupos solucionadores
group_values = list(df_groups['Grupo'])

# Configura os widgets de texto e captura os valores
global combo_box
combo_box = setup_text_widgets(root, list(df_templates['Template']))

def reload_main_screen():
    global df_templates, df_groups, group_values  # Certifique-se de que o DataFrame global seja atualizado
    df_templates = load_templates()  # Recarregar os templates do arquivo
    df_groups = load_groups()
    combo_box['values'] = list(df_templates['Template'])
    combo_box.set('')  # Limpar a seleção do ComboBox de templates
    combo_box.set('')


    # Atualizar os valores do ComboBox de grupos e a lista group_values
    group_values = list(df_groups['Grupo'])
    group_combo_box['values'] = group_values
    group_combo_box.set('')  # Limpar a seleção do ComboBox de grupos


# Função para atualizar o template ao selecionar um novo no ComboBox
def update_template_display(*args):
    selected_template = combo_box.get()

    # Verifique se algum template está selecionado
    if not selected_template:
        messagebox.showerror("Erro", "Por favor, selecione um template para visualizar a mensagem padrão.")
        return

    # Tente encontrar o template correto no DataFrame
    try:
        base_message = df_templates.loc[df_templates['Template'] == selected_template, 'Message'].values[0]
        template_text.delete(1.0, tk.END)
        template_text.insert(tk.END, base_message)
    except IndexError:
        messagebox.showerror("Erro", f"Não foi possível encontrar a mensagem padrão para '{selected_template}'.")

# Listener para o ComboBox que aciona quando a seleção mudar
combo_box.bind("<<ComboboxSelected>>", update_template_display)

global group_combo_box

# Configura os campos de entrada para gerar a mensagem (passando os valores dos grupos solucionadores)
(client_name_label, client_name_entry, info_label, info_entry,
 status_label, status_entry, responsavel_label, responsavel_entry,
 group_label, group_combo_box) = setup_entry_fields(root, group_values)

# Função para atualizar o grupo ao selecionar um novo no ComboBox de grupos
def update_group_display(*args):
    selected_group = group_combo_box.get()

    if selected_group:
        print(f"Grupo selecionado: {selected_group}")
        # Aqui você pode adicionar lógica adicional para fazer algo com o grupo selecionado

# Listener para o ComboBox de grupos que aciona quando a seleção mudar
group_combo_box.bind("<<ComboboxSelected>>", update_group_display)

# Agora, `group_combo_box` está definido, e você pode passá-lo para `setup_buttons`.
setup_buttons(root, df_templates, df_groups, user_templates_path, user_groups_path, open_management_window, open_group_management_window, group_combo_box, combo_box, reload_main_screen)

# Função para exibir/ocultar o template original
template_visible = False
template_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)

def get_current_version():
    with open(version_path, 'r') as f:
        return f.read().strip()

def toggle_template():
    global template_visible
    selected_template = combo_box.get()

    # Verifique se algum template está selecionado
    if not selected_template:
        messagebox.showerror("Erro", "Por favor, selecione um template para visualizar a mensagem padrão.")
        return

    if template_visible:
        # Ocultar o campo de texto do template original
        template_text.grid_remove()
        toggle_button.config(text="Exibir Template Original")
        root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")  # Ajusta a geometria da janela
        template_visible = False
    else:
        # Tente encontrar o template correto no DataFrame
        try:
            base_message = df_templates.loc[df_templates['Template'] == selected_template, 'Message'].values[0]
            template_text.delete(1.0, tk.END)
            template_text.insert(tk.END, base_message)
            template_text.grid()
            toggle_button.config(text="Ocultar Template Original")
            root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")  # Ajusta a geometria da janela
        except IndexError:
            # Caso o template não seja encontrado
            messagebox.showerror("Erro", f"Não foi possível encontrar a mensagem padrão para '{selected_template}'.")

        template_visible = True

# Botões para gerar mensagem e exibir/ocultar template
generate_button, toggle_button = setup_action_buttons(
    root,
    lambda: generate_message(df_templates, client_name_entry, info_entry, group_combo_box, status_entry, responsavel_entry, combo_box, client_name_label, info_label, group_label, status_label, responsavel_label, result_text),
    toggle_template
)

#Função pra copiar a mensagem
def copy_menssage():
    mensagem = result_text.get("1.0", tk.END).strip()  # Captura o texto da primeira à última linha

    # Copiar a mensagem para a área de transferência
    root.clipboard_clear()
    root.clipboard_append(mensagem)

    # Exibir o label de confirmação
    copy_label.config(text="Mensagem copiada!", fg="green")
    copy_label.grid()  # Exibe o label

    # Remove o label após 3 segundos
    root.after(3000, clean_copy_label)

# Função para limpar a mensagem de confirmação
def clean_copy_label():
    copy_label.grid_remove()


# Campo de resultado
result_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
result_text.grid(row=17, column=0, padx=10, pady=10)

# Campo para exibir o template original (inicialmente oculto)
template_text.grid(row=16, column=0, padx=10, pady=5)
template_text.grid_remove()

# Botão para copiar a mensagem gerada
copy_button = tk.Button(root, text="Copiar Mensagem", command=copy_menssage)
copy_button.grid(row=18, column=0, pady=10, ipadx=10, ipady=5)

# Label que mostra a confirmação
copy_label = tk.Label(root, text="", font=("Helvetica", 10))
copy_label.grid(row=18, column=0, pady=5)
copy_label.grid_remove()

# Permitir redimensionamento da janela
root.resizable(True, True)

# Atualiza o layout e ajusta o tamanho da janela com base no conteúdo
root.update_idletasks()  # Recalcula o layout
root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")  # Ajusta a geometria da janela

use_icon_in_app(root, ico_output)

# Rodar o loop principal da aplicação
root.mainloop()
