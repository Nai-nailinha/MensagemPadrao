import tkinter as tk
from tkinter import messagebox
from file_handler import check_for_update, load_templates, load_groups, message_templates_path, solucionadores_path
from message_utils import generate_message
from ui_components import setup_buttons, setup_text_widgets, setup_entry_fields, setup_action_buttons, copy_message
from template_manager import open_management_window, open_group_management_window

# Inicializa a interface principal
root = tk.Tk()
root.title("Gerador de Mensagens")

# Checa atualizações
has_update, latest_version = check_for_update()
if has_update:
    messagebox.showinfo("Atualização Disponível", f"Nova versão disponível: {latest_version}")

# Carrega os dados dos arquivos CSV
df_templates = load_templates()
df_groups = load_groups()

# Lista de valores para o ComboBox de grupos solucionadores
group_values = list(df_groups['Grupo'])

# Configura os botões de gerenciamento
setup_buttons(root, df_templates, df_groups, message_templates_path, solucionadores_path, open_management_window, open_group_management_window)

# Configura os widgets de texto e captura os valores
combo_box = setup_text_widgets(root, list(df_templates['Template']))

# Configura os campos de entrada para gerar a mensagem (passando os valores dos grupos solucionadores)
(client_name_label, client_name_entry, info_label, info_entry,
 status_label, status_entry, responsavel_label, responsavel_entry,
 group_label, group_combo_box) = setup_entry_fields(root, group_values)

# Função para exibir/ocultar o template original
template_visible = False
template_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)


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
        template_visible = False
    else:
        # Tente encontrar o template correto no DataFrame
        try:
            base_message = df_templates.loc[df_templates['Template'] == selected_template, 'Message'].values[0]
            template_text.delete(1.0, tk.END)
            template_text.insert(tk.END, base_message)
            template_text.grid()
            toggle_button.config(text="Ocultar Template Original")
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

# Campo de resultado
result_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
result_text.grid(row=17, column=0, padx=10, pady=10)

# Campo para exibir o template original (inicialmente oculto)
template_text.grid(row=16, column=0, padx=10, pady=5)
template_text.grid_remove()

# Botão para copiar a mensagem gerada
copy_button = tk.Button(root, text="Copiar Mensagem", command=lambda: copy_message(root, result_text))
copy_button.grid(row=18, column=0, padx=10, pady=10)

# Rodar o loop principal da aplicação
root.mainloop()
