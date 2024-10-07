import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


# Função para abrir a janela de gerenciamento de templates
def open_management_window(parent_window, df, file_path):
    management_window = tk.Toplevel(parent_window)
    management_window.title("Gerenciamento de Templates")

    # Função para atualizar os campos de um template selecionado para edição
    def update_template_fields(event):
        selected_template = combo_box_manage.get()
        template_data = df[df['Template'] == selected_template]

        if not template_data.empty:
            # Carrega a mensagem e os campos obrigatórios do template
            message = template_data['Message'].values[0]
            required_fields = template_data['Obrigatório'].values[0]

            # Atualiza os campos de texto
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, message)
            required_fields_entry.delete(0, tk.END)
            required_fields_entry.insert(0, required_fields)
        else:
            messagebox.showerror("Erro", "O template selecionado não foi encontrado.")

    # Função para alternar entre as seções de edição e criação
    def show_edit_section():
        # Oculta a seção de criação e mostra a de edição
        create_frame.grid_remove()
        edit_frame.grid()

    def show_create_section():
        # Oculta a seção de edição e mostra a de criação
        edit_frame.grid_remove()
        create_frame.grid()

    # Texto de informações sobre placeholders
    placeholder_info_text = """Use os seguintes placeholders nos seus templates:

    [Nome do Cliente] - Para inserir o nome do cliente
    [Informação] - Para informações adicionais
    [grupo solucionador] - Para o grupo que está resolvendo o problema
    [status] - Para o status atual do chamado
    [responsavel] - Para a pessoa responsável pelo chamado

Copie e cole exatamente como escrito para garantir o funcionamento correto."""

    # Campo de texto para exibir informações sobre os placeholders
    info_text_box = tk.Text(management_window, wrap=tk.WORD, width=60, height=8)
    info_text_box.insert(tk.END, placeholder_info_text)
    info_text_box.config(state="disabled")  # Tornar não editável
    info_text_box.grid(row=0, column=0, padx=10, pady=10)

    # Frame para a seção de edição
    edit_frame = tk.Frame(management_window)

    tk.Label(edit_frame, text="Selecionar Template para Editar ou Excluir").grid(row=0, column=0, padx=10, pady=5)
    combo_box_manage = ttk.Combobox(edit_frame, values=list(df['Template']))
    combo_box_manage.grid(row=1, column=0, padx=10, pady=5)
    combo_box_manage.bind("<<ComboboxSelected>>", update_template_fields)

    tk.Label(edit_frame, text="Conteúdo do Template").grid(row=2, column=0, padx=10, pady=5)
    text_box = tk.Text(edit_frame, wrap=tk.WORD, width=60, height=10)
    text_box.grid(row=3, column=0, padx=10, pady=10)

    tk.Label(edit_frame, text="Campos Obrigatórios (separados por vírgula)").grid(row=4, column=0, padx=10, pady=5)
    required_fields_entry = tk.Entry(edit_frame, width=40)
    required_fields_entry.grid(row=5, column=0, padx=10, pady=5)

    save_button = tk.Button(edit_frame, text="Salvar Alterações",
                            command=lambda: save_edit(combo_box_manage, text_box, required_fields_entry, df, file_path, management_window))
    save_button.grid(row=6, column=0, padx=10, pady=5)

    delete_button = tk.Button(edit_frame, text="Excluir Template",
                              command=lambda: delete_template(combo_box_manage, df, file_path, management_window))
    delete_button.grid(row=7, column=0, padx=10, pady=5)

    # Frame para a seção de criação
    create_frame = tk.Frame(management_window)

    tk.Label(create_frame, text="Adicionar Novo Template").grid(row=0, column=0, padx=10, pady=20)
    tk.Label(create_frame, text="Nome do Novo Template").grid(row=1, column=0, padx=10, pady=5)
    template_entry = tk.Entry(create_frame, width=40)
    template_entry.grid(row=2, column=0, padx=10, pady=5)

    tk.Label(create_frame, text="Conteúdo do Novo Template").grid(row=3, column=0, padx=10, pady=5)
    new_message_text = tk.Text(create_frame, wrap=tk.WORD, width=60, height=10)
    new_message_text.grid(row=4, column=0, padx=10, pady=10)

    tk.Label(create_frame, text="Campos Obrigatórios do Novo Template").grid(row=5, column=0, padx=10, pady=5)
    new_required_fields_entry = tk.Entry(create_frame, width=40)
    new_required_fields_entry.grid(row=6, column=0, padx=10, pady=5)

    add_button = tk.Button(create_frame, text="Adicionar Novo Template",
                           command=lambda: add_new_template(template_entry, new_message_text, new_required_fields_entry, df, file_path, management_window))
    add_button.grid(row=7, column=0, padx=10, pady=10)

    # Botões para alternar entre seções
    toggle_frame = tk.Frame(management_window)
    toggle_frame.grid(row=1, column=0, pady=10)

    edit_section_button = tk.Button(toggle_frame, text="Editar Template", command=show_edit_section)
    edit_section_button.grid(row=0, column=0, padx=10)

    create_section_button = tk.Button(toggle_frame, text="Adicionar Novo Template", command=show_create_section)
    create_section_button.grid(row=0, column=1, padx=10)

    # Inicializa a janela mostrando a seção de edição
    show_edit_section()


# Funções para manipular templates
def save_edit(combo_box, text_box, required_fields_entry, df, file_path, management_window):
    selected_template = combo_box.get()
    new_message = text_box.get(1.0, tk.END).strip()
    new_required_fields = required_fields_entry.get().strip()
    df.loc[df['Template'] == selected_template, 'Message'] = new_message
    df.loc[df['Template'] == selected_template, 'Obrigatório'] = new_required_fields
    df.to_csv(file_path, index=False)
    messagebox.showinfo("Salvar", "O template foi atualizado com sucesso!")
    management_window.destroy()

def delete_template(combo_box, df, file_path, management_window):
    selected_template = combo_box.get()
    df.drop(df[df['Template'] == selected_template].index, inplace=True)
    df.to_csv(file_path, index=False)
    messagebox.showinfo("Excluir", "O template foi excluído com sucesso!")
    management_window.destroy()

def add_new_template(template_entry, message_text, required_fields_entry, df, file_path, management_window):
    new_template = template_entry.get().strip()
    new_message = message_text.get(1.0, tk.END).strip()
    new_required_fields = required_fields_entry.get().strip()
    if new_template and new_message:
        new_row = pd.DataFrame({"Template": [new_template], "Message": [new_message], "Obrigatório": [new_required_fields]})
        updated_df = pd.concat([df, new_row], ignore_index=True)
        updated_df.to_csv(file_path, index=False)
        messagebox.showinfo("Adicionar", "Novo template adicionado com sucesso!")
        management_window.destroy()
    else:
        messagebox.showerror("Erro", "Preencha todos os campos antes de adicionar um novo template.")


# Função para abrir a janela de gerenciamento de grupos solucionadores
def open_group_management_window(parent_window, df_groups, groups_file, main_group_combo_box):
    group_window = tk.Toplevel(parent_window)
    group_window.title("Gerenciamento de Grupos")

    # Função para salvar a edição de um grupo
    def save_group_edit():
        selected_group = group_combo_box.get()
        new_group_name = group_name_entry.get().strip()
        if new_group_name:
            df_groups.loc[df_groups['Grupo'] == selected_group, 'Grupo'] = new_group_name
            df_groups.to_csv(groups_file, index=False)
            messagebox.showinfo("Salvar", "O grupo foi atualizado com sucesso!")
            update_main_group_combo_box()
            group_window.destroy()
        else:
            messagebox.showerror("Erro", "O nome do grupo não pode estar vazio.")

    # Função para excluir um grupo
    def delete_group():
        selected_group = group_combo_box.get()
        df_groups.drop(df_groups[df_groups['Grupo'] == selected_group].index, inplace=True)
        df_groups.to_csv(groups_file, index=False)
        messagebox.showinfo("Excluir", "O grupo foi excluído com sucesso!")
        update_main_group_combo_box()
        group_window.destroy()

    # Função para adicionar um novo grupo
    def add_group():
        new_group = add_group_entry.get().strip()
        if new_group and new_group not in df_groups['Grupo'].values:
            df_groups.loc[len(df_groups)] = [new_group]
            df_groups.to_csv(groups_file, index=False)
            messagebox.showinfo("Adicionar", "Novo grupo adicionado com sucesso!")
            update_main_group_combo_box()
            group_window.destroy()
        else:
            messagebox.showerror("Erro", "O nome do grupo não pode estar vazio ou já existente.")

    # Atualiza o ComboBox principal de grupos na tela principal
    def update_main_group_combo_box():
        main_group_combo_box['values'] = list(df_groups['Grupo'])

    # Interface para gerenciamento de grupos
    tk.Label(group_window, text="Selecionar Grupo para Editar ou Excluir").grid(row=0, column=0, padx=10, pady=5)

    # ComboBox para selecionar o grupo a ser editado ou excluído
    group_combo_box = ttk.Combobox(group_window, values=list(df_groups['Grupo']), width=40)
    group_combo_box.grid(row=1, column=0, padx=10, pady=5)

    # Entrada para editar o nome do grupo selecionado
    tk.Label(group_window, text="Nome do Grupo").grid(row=2, column=0, padx=10, pady=5)
    group_name_entry = tk.Entry(group_window, width=40)
    group_name_entry.grid(row=3, column=0, padx=10, pady=5)

    # Botão para salvar as alterações no grupo
    save_button = tk.Button(group_window, text="Salvar Alterações", command=save_group_edit)
    save_button.grid(row=4, column=0, padx=10, pady=5)

    # Botão para excluir o grupo selecionado
    delete_button = tk.Button(group_window, text="Excluir Grupo", command=delete_group)
    delete_button.grid(row=5, column=0, padx=10, pady=5)

    # Adicionar Novo Grupo
    tk.Label(group_window, text="Adicionar Novo Grupo").grid(row=6, column=0, padx=10, pady=20)

    # Entrada para adicionar um novo grupo
    tk.Label(group_window, text="Nome do Novo Grupo").grid(row=7, column=0, padx=10, pady=5)
    add_group_entry = tk.Entry(group_window, width=40)
    add_group_entry.grid(row=8, column=0, padx=10, pady=5)

    # Botão para adicionar o novo grupo
    add_button = tk.Button(group_window, text="Adicionar Grupo", command=add_group)
    add_button.grid(row=9, column=0, padx=10, pady=10)
