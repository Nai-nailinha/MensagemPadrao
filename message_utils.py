import unicodedata
from tkinter import messagebox
import tkinter as tk
import pandas as pd

# Função para normalizar strings (remover acentos e tornar minúsculas)
def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

# Função para gerar mensagem personalizada
def generate_message(df_templates, client_name_entry, info_entry, group_combo_box, status_entry, responsavel_entry, combo_box, client_name_label, info_label, group_label, status_label, responsavel_label, result_text):
    # Verifica se algum template foi selecionado
    selected_template = combo_box.get()
    if not selected_template:
        messagebox.showerror("Erro", "Selecione um template para gerar a mensagem.")
        return

    # Verifica se o template selecionado existe no DataFrame
    template_data = df_templates[df_templates['Template'] == selected_template]
    if template_data.empty:
        messagebox.showerror("Erro", "Não foi possível encontrar o template selecionado.")
        return

    # Obtém os campos obrigatórios do template e verifica se o campo não está vazio ou NaN
    obrigatorios = template_data['Obrigatório'].values[0]
    if pd.isna(obrigatorios):  # Verifica se está vazio ou NaN
        obrigatorios = ""  # Define uma string vazia se for o caso

    obrigatorios = obrigatorios.replace(" ", "").split(',')  # Processa os campos obrigatórios
    obrigatorios_normalizados = [campo.upper() for campo in obrigatorios]

    validation_errors = []

    # Campos preenchidos pelo usuário
    campos_usuario = {
        "[CLIENTE]": client_name_entry.get().strip(),
        "[INFORMACAO]": info_entry.get().strip(),
        "[GRUPO]": group_combo_box.get().strip(),
        "[STATUS]": status_entry.get().strip(),
        "[RESPONSAVEL]": responsavel_entry.get().strip()
    }

    # Validação dos campos obrigatórios (com colchetes)
    if "[CLIENTE]" in obrigatorios_normalizados and not campos_usuario["[CLIENTE]"]:
        validation_errors.append("[CLIENTE]")
        client_name_label.config(fg="red")
    else:
        client_name_label.config(fg="black")

    if "[INFORMACAO]" in obrigatorios_normalizados and not campos_usuario["[INFORMACAO]"]:
        validation_errors.append("[INFORMACAO]")
        info_label.config(fg="red")
    else:
        info_label.config(fg="black")

    if "[GRUPO]" in obrigatorios_normalizados and not campos_usuario["[GRUPO]"]:
        validation_errors.append("[GRUPO]")
        group_label.config(fg="red")
    else:
        group_label.config(fg="black")

    if "[STATUS]" in obrigatorios_normalizados and not campos_usuario["[STATUS]"]:
        validation_errors.append("[STATUS]")
        status_label.config(fg="red")
    else:
        status_label.config(fg="black")

    if "[RESPONSAVEL]" in obrigatorios_normalizados and not campos_usuario["[RESPONSAVEL]"]:
        validation_errors.append("[RESPONSAVEL]")
        responsavel_label.config(fg="red")
    else:
        responsavel_label.config(fg="black")

    # Se houver erros de validação, exibe uma mensagem e encerra a função
    if validation_errors:
        messagebox.showerror("Erro", f"Preencha os campos obrigatórios: {', '.join(validation_errors)}.")
        return

    # Geração da mensagem personalizada
    try:
        # Tenta encontrar o template correto no DataFrame
        base_message = template_data['Message'].values[0]

        # Substitui os placeholders no template pelos valores fornecidos
        personalized_message = base_message.replace("[CLIENTE]", campos_usuario["[CLIENTE]"])
        personalized_message = personalized_message.replace("[INFORMACAO]", campos_usuario["[INFORMACAO]"])
        personalized_message = personalized_message.replace("[GRUPO]", campos_usuario["[GRUPO]"])
        personalized_message = personalized_message.replace("[STATUS]", campos_usuario["[STATUS]"])
        personalized_message = personalized_message.replace("[RESPONSAVEL]", campos_usuario["[RESPONSAVEL]"])

        # Exibe a mensagem gerada no campo de resultado
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, personalized_message)

    except KeyError as e:
        messagebox.showerror("Erro", f"O campo obrigatório '{str(e)}' não foi encontrado ou está vazio.")