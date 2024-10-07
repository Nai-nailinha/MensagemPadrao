import tkinter as tk
from tkinter import ttk, messagebox  # Adicione `ttk` aqui

def setup_buttons(root, df_templates, df_groups, message_templates_path, solucionadores_path, open_management_window, open_group_management_window, group_combo_box):
    manage_frame = tk.Frame(root)
    manage_frame.grid(row=0, column=0, columnspan=2, pady=10)

    manage_button = tk.Button(manage_frame, text="Gerenciar Templates",
                              command=lambda: open_management_window(root, df_templates, message_templates_path))
    manage_button.grid(row=0, column=0, padx=10)

    manage_groups_button = tk.Button(manage_frame, text="Gerenciar Grupos",
                                     command=lambda: open_group_management_window(root, df_groups, solucionadores_path, group_combo_box))
    manage_groups_button.grid(row=0, column=1, padx=10)

def setup_text_widgets(root, combo_values):
    combo_box = ttk.Combobox(root, values=combo_values)  # Agora `ttk` está definido
    combo_box.grid(row=2, column=0, padx=10, pady=5)
    return combo_box

def copy_message(root, result_text):
    message = result_text.get(1.0, tk.END).strip()
    if message:
        root.clipboard_clear()
        root.clipboard_append(message)
        messagebox.showinfo("Copiar", "Mensagem copiada para a área de transferência!")


def setup_action_buttons(root, generate_message_func, toggle_template_func):
    # Botão para gerar a mensagem
    generate_button = tk.Button(root, text="Gerar Mensagem", command=generate_message_func)
    generate_button.grid(row=15, column=0, padx=10, pady=10)

    # Botão para exibir/ocultar o template original
    toggle_button = tk.Button(root, text="Exibir Template Original", command=toggle_template_func)
    toggle_button.grid(row=14, column=0, padx=10, pady=10)

    return generate_button, toggle_button

def setup_entry_fields(root, group_values):
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
    group_combo_box = ttk.Combobox(root, values=group_values, width=60)  # Adiciona os valores ao ComboBox
    group_combo_box.grid(row=13, column=0, padx=10, pady=5)

    return client_name_label, client_name_entry, info_label, info_entry, status_label, status_entry, responsavel_label, responsavel_entry, group_label, group_combo_box
