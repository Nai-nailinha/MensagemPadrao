import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


def open_management_window(parent_window, df, file_path):
    management_window = tk.Toplevel(parent_window)
    management_window.title("Gerenciamento de Templates")

    # Função para salvar edição do template
    def save_edit():
        selected_template = combo_box_manage.get()
        new_message = text_box.get(1.0, tk.END).strip()
        new_required_fields = required_fields_entry.get().strip()
        df.loc[df['Template'] == selected_template, 'Message'] = new_message
        df.loc[df['Template'] == selected_template, 'Obrigatório'] = new_required_fields
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Salvar", "O template foi atualizado com sucesso!")
        management_window.destroy()

    # Função para excluir o template
    def delete_template():
        selected_template = combo_box_manage.get()
        df.drop(df[df['Template'] == selected_template].index, inplace=True)
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Excluir", "O template foi excluído com sucesso!")
        management_window.destroy()

    # Função para adicionar um novo template
    def add_new_template():
        new_template = template_entry.get().strip()
        new_message = new_message_text.get(1.0, tk.END).strip()
        new_required_fields = new_required_fields_entry.get().strip()
        if new_template and new_message:
            new_row = pd.DataFrame(
                {"Template": [new_template], "Message": [new_message], "Obrigatório": [new_required_fields]})
            updated_df = pd.concat([df, new_row], ignore_index=True)
            updated_df.to_csv(file_path, index=False)
            messagebox.showinfo("Adicionar", "Novo template adicionado com sucesso!")
            management_window.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos antes de adicionar um novo template.")

    # Função para atualizar a interface ao selecionar um template
    def update_template_fields(event):
        selected_template = combo_box_manage.get()
        template_data = df[df['Template'] == selected_template]
        message = template_data['Message'].values[0]
        required_fields = template_data['Obrigatório'].values[0]
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, message)
        required_fields_entry.delete(0, tk.END)
        required_fields_entry.insert(0, required_fields)

    # Interface para gerenciamento
    tk.Label(management_window, text="Selecionar Template para Editar ou Excluir").grid(row=0, column=0, padx=10,
                                                                                        pady=5)
    combo_box_manage = ttk.Combobox(management_window, values=list(df['Template']))
    combo_box_manage.grid(row=1, column=0, padx=10, pady=5)
    combo_box_manage.bind("<<ComboboxSelected>>", update_template_fields)

    tk.Label(management_window, text="Conteúdo do Template").grid(row=2, column=0, padx=10, pady=5)
    text_box = tk.Text(management_window, wrap=tk.WORD, width=60, height=10)
    text_box.grid(row=3, column=0, padx=10, pady=10)

    tk.Label(management_window, text="Campos Obrigatórios (separados por vírgula)").grid(row=4, column=0, padx=10,
                                                                                         pady=5)
    required_fields_entry = tk.Entry(management_window, width=40)
    required_fields_entry.grid(row=5, column=0, padx=10, pady=5)

    # Botões de ação para editar, excluir e adicionar
    save_button = tk.Button(management_window, text="Salvar Alterações", command=save_edit)
    save_button.grid(row=6, column=0, padx=10, pady=5)

    delete_button = tk.Button(management_window, text="Excluir Template", command=delete_template)
    delete_button.grid(row=7, column=0, padx=10, pady=5)

    # Adicionar Novo Template
    tk.Label(management_window, text="Adicionar Novo Template").grid(row=8, column=0, padx=10, pady=20)

    tk.Label(management_window, text="Nome do Novo Template").grid(row=9, column=0, padx=10, pady=5)
    template_entry = tk.Entry(management_window, width=40)
    template_entry.grid(row=10, column=0, padx=10, pady=5)

    tk.Label(management_window, text="Conteúdo do Novo Template").grid(row=11, column=0, padx=10, pady=5)
    new_message_text = tk.Text(management_window, wrap=tk.WORD, width=60, height=10)
    new_message_text.grid(row=12, column=0, padx=10, pady=10)

    tk.Label(management_window, text="Campos Obrigatórios do Novo Template").grid(row=13, column=0, padx=10, pady=5)
    new_required_fields_entry = tk.Entry(management_window, width=40)
    new_required_fields_entry.grid(row=14, column=0, padx=10, pady=5)

    add_button = tk.Button(management_window, text="Adicionar Novo Template", command=add_new_template)
    add_button.grid(row=15, column=0, padx=10, pady=10)


def open_group_management_window(parent_window, df_groups, groups_file):
    group_window = tk.Toplevel(parent_window)
    group_window.title("Gerenciamento de Grupos")

    # Função para salvar a edição de um grupo
    def save_group_edit():
        selected_group = group_combo_box.get()
        new_group_name = group_name_entry.get().strip()
        df_groups.loc[df_groups['Grupo'] == selected_group, 'Grupo'] = new_group_name
        df_groups.to_csv(groups_file, index=False)
        messagebox.showinfo("Salvar", "O grupo foi atualizado com sucesso!")
        group_window.destroy()

    # Função para excluir um grupo
    def delete_group():
        selected_group = group_combo_box.get()
        df_groups.drop(df_groups[df_groups['Grupo'] == selected_group].index, inplace=True)
        df_groups.to_csv(groups_file, index=False)
        messagebox.showinfo("Excluir", "O grupo foi excluído com sucesso!")
        group_window.destroy()

    # Função para adicionar um novo grupo
    def add_group():
        new_group = group_name_entry.get().strip()
        if new_group:
            new_row = pd.DataFrame({"Grupo": [new_group]})
            updated_df = pd.concat([df_groups, new_row], ignore_index=True)
            updated_df.to_csv(groups_file, index=False)
            messagebox.showinfo("Adicionar", "Novo grupo adicionado com sucesso!")
            group_window.destroy()
        else:
            messagebox.showerror("Erro", "Preencha o campo de grupo antes de adicionar.")

    # Interface para gerenciamento de grupos
    tk.Label(group_window, text="Selecionar Grupo para Editar ou Excluir").grid(row=0, column=0, padx=10, pady=5)
    group_combo_box = ttk.Combobox(group_window, values=list(df_groups['Grupo']))
    group_combo_box.grid(row=1, column=0, padx=10, pady=5)

    tk.Label(group_window, text="Nome do Grupo").grid(row=2, column=0, padx=10, pady=5)
    group_name_entry = tk.Entry(group_window, width=40)
    group_name_entry.grid(row=3, column=0, padx=10, pady=5)

    save_button = tk.Button(group_window, text="Salvar Alterações", command=save_group_edit)
    save_button.grid(row=4, column=0, padx=10, pady=5)

    delete_button = tk.Button(group_window, text="Excluir Grupo", command=delete_group)
    delete_button.grid(row=5, column=0, padx=10, pady=5)

    # Adicionar Novo Grupo
    tk.Label(group_window, text="Adicionar Novo Grupo").grid(row=6, column=0, padx=10, pady=20)

    tk.Label(group_window, text="Nome do Novo Grupo").grid(row=7, column=0, padx=10, pady=5)
    add_group_entry = tk.Entry(group_window, width=40)
    add_group_entry.grid(row=8, column=0, padx=10, pady=5)

    add_button = tk.Button(group_window, text="Adicionar Grupo", command=add_group)
    add_button.grid(row=9, column=0, padx=10, pady=10)



