import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import unicodedata
from template_manager import open_management_window, open_group_management_window

# Caminhos para os arquivos CSV
template_file = 'message_templates.csv'
groups_file = 'solucionadores.csv'


# Função para carregar o CSV de templates
def load_templates():
    return pd.read_csv(template_file)


# Função para carregar o CSV de grupos de solucionadores
def load_groups():
    return pd.read_csv(groups_file)


# Variáveis globais para os dados
df_templates = load_templates()
df_groups = load_groups()


# Função para normalizar strings (remover acentos e tornar minúsculas)
def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()


# Função para gerar mensagem personalizada
def generate_message():
    selected_template = combo_box.get()
    if not selected_template:
        messagebox.showerror("Erro", "Selecione um template para gerar a mensagem.")
        return

    # Extrair os campos obrigatórios para validação
    obrigatorios = df_templates[df_templates['Template'] == selected_template]['Obrigatório'].values[0].split(', ')
    obrigatorios_normalizados = [normalize_string(campo) for campo in obrigatorios]

    # Verificar se todos os campos obrigatórios estão preenchidos
    validation_errors = []

    # Normalizar campos fornecidos pelo usuário para comparação
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

    # Extrair a mensagem base e substituir os placeholders
    base_message = df_templates[df_templates['Template'] == selected_template]['Message'].values[0]
    personalized_message = base_message.replace("[Nome do Cliente]", client_name_entry.get())
    personalized_message = personalized_message.replace("[Informação]", info_entry.get())
    personalized_message = personalized_message.replace("[grupo solucionador]", group_combo_box.get())
    personalized_message = personalized_message.replace("[responsavel]", responsavel_entry.get())
    personalized_message = personalized_message.replace("[status]", status_entry.get())

    # Atualizar o conteúdo do Text widget
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, personalized_message)


# Função para exibir/ocultar o template original
template_visible = False


def toggle_template():
    global template_visible
    if template_visible:
        template_text.grid_remove()
        toggle_button.config(text="Exibir Template Original")
        template_visible = False
    else:
        selected_template = combo_box.get()
        if selected_template:
            # Mostrar o template original
            base_message = df_templates[df_templates['Template'] == selected_template]['Message'].values[0]
            template_text.delete(1.0, tk.END)
            template_text.insert(tk.END, base_message)
            template_text.grid()
        toggle_button.config(text="Ocultar Template Original")
        template_visible = True


# Função para copiar a mensagem gerada para a área de transferência
def copy_message():
    message = result_text.get(1.0, tk.END).strip()
    if message:
        root.clipboard_clear()
        root.clipboard_append(message)
        messagebox.showinfo("Copiar", "Mensagem copiada para a área de transferência!")


# Criar a janela principal
root = tk.Tk()
root.title("Gerador de Mensagens")

# Frame para os botões de gerenciamento centralizados
manage_frame = tk.Frame(root)
manage_frame.grid(row=0, column=0, columnspan=2, pady=10)

# Botão para gerenciar templates (centralizado na parte superior)
manage_button = tk.Button(manage_frame, text="Gerenciar Templates",
                          command=lambda: open_management_window(root, df_templates, template_file))
manage_button.grid(row=0, column=0, padx=10)

# Botão para gerenciar grupos (centralizado na parte superior)
manage_groups_button = tk.Button(manage_frame, text="Gerenciar Grupos",
                                 command=lambda: open_group_management_window(root, df_groups, groups_file))
manage_groups_button.grid(row=0, column=1, padx=10)

# ComboBox para seleção de templates
tk.Label(root, text="Selecione uma Mensagem:").grid(row=2, column=0, sticky='w', padx=10)
combo_box = ttk.Combobox(root, values=list(df_templates['Template']))
combo_box.grid(row=2, column=0, padx=10, pady=5)

# Campo para inserir o nome do cliente
client_name_label = tk.Label(root, text="Nome do Cliente:")
client_name_label.grid(row=4, column=0, sticky='w', padx=10)
client_name_entry = tk.Entry(root, width=30)
client_name_entry.grid(row=4, column=0, padx=10, pady=5)

# Campo para inserir a informação
info_label = tk.Label(root, text="Informação:")
info_label.grid(row=6, column=0, sticky='w', padx=10)
info_entry = tk.Entry(root, width=30)
info_entry.grid(row=6, column=0, padx=10, pady=5)

# Campo para inserir o status
status_label = tk.Label(root, text="Status:")
status_label.grid(row=8, column=0, sticky='w', padx=10)
status_entry = tk.Entry(root, width=30)
status_entry.grid(row=8, column=0, padx=10, pady=5)

# Campo para inserir o responsável
responsavel_label = tk.Label(root, text="Responsável:")
responsavel_label.grid(row=10, column=0, sticky='w', padx=10)
responsavel_entry = tk.Entry(root, width=30)
responsavel_entry.grid(row=10, column=0, padx=10, pady=5)

# ComboBox para selecionar grupos de solucionadores
group_label = tk.Label(root, text="Grupo Solucionador:")
group_label.grid(row=12, column=0, sticky='w', padx=10)
group_combo_box = ttk.Combobox(root, values=list(df_groups['Grupo']))
group_combo_box.grid(row=12, column=0, padx=10, pady=5)

# Botão para gerar a mensagem
generate_button = tk.Button(root, text="Gerar Mensagem", command=generate_message)
generate_button.grid(row=13, column=0, padx=10, pady=10)

# Botão para exibir/ocultar o template original
toggle_button = tk.Button(root, text="Exibir Template Original", command=toggle_template)
toggle_button.grid(row=14, column=0, padx=10, pady=10)

# Campo para exibir o template original (inicialmente oculto)
template_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
template_text.grid(row=15, column=0, padx=10, pady=5)
template_text.grid_remove()

# Text widget para exibir a mensagem gerada
result_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
result_text.grid(row=16, column=0, padx=10, pady=10)

# Botão para copiar a mensagem gerada
copy_button = tk.Button(root, text="Copiar Mensagem", command=copy_message)
copy_button.grid(row=17, column=0, padx=10, pady=10)

# Rodar o loop principal da aplicação
root.mainloop()





