import unicodedata
from tkinter import messagebox
import tkinter as tk  # Adicione esta linha para importar `tkinter` corretamente


# Função para normalizar strings (remover acentos e tornar minúsculas)
def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

# Função para gerar mensagem personalizada
def generate_message(df_templates, client_name_entry, info_entry, group_combo_box, status_entry, responsavel_entry, combo_box, client_name_label, info_label, group_label, status_label, responsavel_label, result_text):
    selected_template = combo_box.get()
    if not selected_template:
        messagebox.showerror("Erro", "Selecione um template para gerar a mensagem.")
        return

    obrigatorios = df_templates[df_templates['Template'] == selected_template]['Obrigatório'].values[0].split(', ')
    obrigatorios_normalizados = [normalize_string(campo) for campo in obrigatorios]

    validation_errors = []

    campos_usuario = {
        "nome do cliente": normalize_string(client_name_entry.get()),
        "informacao": normalize_string(info_entry.get()),
        "grupo solucionador": normalize_string(group_combo_box.get()),
        "status": normalize_string(status_entry.get()),
        "responsavel": normalize_string(responsavel_entry.get())
    }

    if "nome do cliente" in obrigatorios_normalizados and not campos_usuario["nome do cliente"]:
        validation_errors.append("Nome do Cliente")
        client_name_label.config(fg="red")
    else:
        client_name_label.config(fg="black")

    if "informacao" in obrigatorios_normalizados and not campos_usuario["informacao"]:
        validation_errors.append("Informação")
        info_label.config(fg="red")
    else:
        info_label.config(fg="black")

    if "grupo solucionador" in obrigatorios_normalizados and not campos_usuario["grupo solucionador"]:
        validation_errors.append("Grupo Solucionador")
        group_label.config(fg="red")
    else:
        group_label.config(fg="black")

    if "status" in obrigatorios_normalizados and not campos_usuario["status"]:
        validation_errors.append("Status")
        status_label.config(fg="red")
    else:
        status_label.config(fg="black")

    if "responsavel" in obrigatorios_normalizados and not campos_usuario["responsavel"]:
        validation_errors.append("Responsável")
        responsavel_label.config(fg="red")
    else:
        responsavel_label.config(fg="black")

    if validation_errors:
        messagebox.showerror("Erro", f"Preencha os campos obrigatórios: {', '.join(validation_errors)}.")
        return

    base_message = df_templates[df_templates['Template'] == selected_template]['Message'].values[0]
    personalized_message = base_message.replace("[Nome do Cliente]", client_name_entry.get())
    personalized_message = personalized_message.replace("[Informação]", info_entry.get())
    personalized_message = personalized_message.replace("[grupo solucionador]", group_combo_box.get())
    personalized_message = personalized_message.replace("[responsavel]", responsavel_entry.get())
    personalized_message = personalized_message.replace("[status]", status_entry.get())

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, personalized_message)
