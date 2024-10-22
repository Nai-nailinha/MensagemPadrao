import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from file_handler import solucionadores_path


# Função para limpar a mensagem de status após um tempo (em segundos)
def clear_status_after_delay(status_label, delay_seconds):
    status_label.after(int(delay_seconds * 1000), lambda: clear_status(status_label))

def clear_status(status_label):
    if status_label.winfo_exists():  # Verifica se o label ainda existe
        status_label.config(text="")

# Função para abrir a janela de gerenciamento de templates
def open_management_window(parent_window, df_templates, file_path, combo_box, reload_main_screen):
    # Fecha a janela principal ao abrir a janela de gerenciamento
    parent_window.withdraw()

    management_window = tk.Toplevel(parent_window)
    management_window.title("Gerenciamento de Templates")

    def on_close():
        # Reabre a janela principal quando a janela de gerenciamento for fechada
        parent_window.deiconify()
        management_window.destroy()
        reload_main_screen()
        # Recarregar a tela principal para garantir que os templates mais recentes estão carregados
        try:
            reload_main_screen()  # Isso garante que o ComboBox da tela principal seja atualizado corretamente
        except Exception as e:
            print(f"Erro ao recarregar a tela principal: {e}")

    # Função para atualizar os campos de um template selecionado para edição
    def update_template_fields(event, combo_box_manage, text_box, required_fields_entry, file_path):
        global df_templates  # Certifica-se de que o df_templates é global

        # Recarregar o CSV para garantir que o DataFrame esteja atualizado
        df_templates = reload_templates(file_path)

        selected_template = combo_box_manage.get()

        if selected_template:
            # Verifique se o template foi corretamente selecionado
            if selected_template not in df_templates['Template'].values:
                messagebox.showerror("Erro", "O template selecionado não foi encontrado no DataFrame.")
                return

            template_data = df_templates[df_templates['Template'] == selected_template]

            if not template_data.empty:
                message = template_data['Message'].values[0]
                required_fields = template_data['Obrigatório'].values[0]

                text_box.delete(1.0, tk.END)
                text_box.insert(tk.END, message)
                required_fields_entry.delete(0, tk.END)
                required_fields_entry.insert(0, required_fields)
            else:
                messagebox.showerror("Erro", "O template selecionado não foi encontrado.")
        else:
            messagebox.showerror("Erro", "Nenhum template foi selecionado.")

    management_window.protocol("WM_DELETE_WINDOW", on_close)

    # Label para exibir o status (mensagem de sucesso ao salvar)
    status_label = tk.Label(management_window, text="", fg="red")
    status_label.grid(row=8, column=0, padx=10, pady=5)

    # Frame para a seção de criação
    create_frame = tk.Frame(management_window)
    create_frame.grid(row=2, column=0, padx=10, pady=5)

    # Frame para edição de templates
    edit_frame = tk.Frame(management_window)
    edit_frame.grid(row=1, column=0, padx=10, pady=5)

    # Label para exibir as placeholders que o cliente pode usar
    placeholder_info_text = """Use os seguintes placeholders nos seus templates:

    [CLIENTE] - Para inserir o nome do cliente
    [INFORMACAO] - Para informações adicionais
    [GRUPO] - Para o grupo que está resolvendo o problema
    [STATUS] - Para o status atual do chamado
    [RESPONSAVEL] - Para a pessoa responsável pelo chamado

    Copie e cole exatamente como escrito para garantir o funcionamento correto."""

    # Campo de texto para exibir as informações sobre os placeholders
    info_text_box = tk.Text(management_window, wrap=tk.WORD, width=60, height=8)
    info_text_box.insert(tk.END, placeholder_info_text)
    info_text_box.config(state="disabled")  # Tornar o campo não editável
    info_text_box.grid(row=0, column=0, padx=10, pady=10)

    # Campo de texto para o conteúdo do template
    tk.Label(edit_frame, text="Conteúdo do Template").grid(row=2, column=0, padx=10, pady=5)
    text_box = tk.Text(edit_frame, wrap=tk.WORD, width=60, height=10)
    text_box.grid(row=3, column=0, padx=10, pady=10)

    # Campo de entrada para os campos obrigatórios
    tk.Label(edit_frame, text="Campos Obrigatórios (separados por vírgula)").grid(row=4, column=0, padx=10, pady=5)
    required_fields_entry = tk.Entry(edit_frame, width=40)
    required_fields_entry.grid(row=5, column=0, padx=10, pady=5)

    # Função para salvar o template
    def save_edit(df_templates, file_path, status_label, combo_box_manage):

        selected_template = combo_box_manage.get()
        new_message = text_box.get(1.0, tk.END).strip()
        new_required_fields = required_fields_entry.get().strip()

        if selected_template:
            df_templates.loc[df_templates['Template'] == selected_template, 'Message'] = new_message
            df_templates.loc[df_templates['Template'] == selected_template, 'Obrigatório'] = new_required_fields

            try:
                df_templates.to_csv(file_path, index=False)
                status_label.config(text="Template atualizado com sucesso!", fg="green")
                clear_status_after_delay(status_label, 3)
                reload_main_screen()

                # Recarrega o CSV atualizado e atualiza o ComboBox
                df_templates = reload_templates(file_path)
                combo_box_manage['values'] = list(df_templates['Template'])

            except Exception as e:
                status_label.config(text=f"Erro ao salvar: {e}", fg="red")
        else:
            status_label.config(text="Selecione um template válido!", fg="red")

    #Função para excluir template
    def delete_template(combo_box_manage, file_path, status_label, text_box, required_fields_entry):
        # Recarregar o CSV antes de excluir
        df_templates = reload_templates(file_path)

        selected_template = combo_box_manage.get()
        if selected_template:
            # Remover o template selecionado
            df_templates_updated = df_templates[df_templates['Template'] != selected_template]

            try:
                # Salvar o arquivo atualizado
                df_templates_updated.to_csv(file_path, index=False)
                status_label.config(text=f"Template '{selected_template}' excluído com sucesso!", fg="green")
                clear_status_after_delay(status_label, 3)

                # Recarregar as telas relevantes
                reload_management_screen(combo_box_manage, file_path)  # Atualizar a tela de gerenciamento
                reload_main_screen()

                # Limpar campos
                text_box.delete(1.0, tk.END)
                required_fields_entry.delete(0, tk.END)

            except Exception as e:
                status_label.config(text=f"Erro ao excluir template: {e}", fg="red")
        else:
            status_label.config(text="Selecione um template para excluir!", fg="red")

    #Função para incluir novo template
    def add_new_template(template_entry, new_message_text, new_required_fields_entry, file_path, status_label,
                         combo_box_manage):
        # Recarregar o CSV antes de adicionar
        df_templates = reload_templates(file_path)

        new_template = template_entry.get().strip()
        new_message = new_message_text.get(1.0, tk.END).strip()
        new_required_fields = new_required_fields_entry.get().strip()

        if not new_template or not new_message:
            status_label.config(text="Erro: Preencha os campos obrigatórios.", fg="red")
            return

        if new_template in df_templates['Template'].values:
            status_label.config(text="Template já existe!", fg="red")
            return

        new_row = pd.DataFrame(
            {"Template": [new_template], "Message": [new_message], "Obrigatório": [new_required_fields]})
        df_templates = pd.concat([df_templates, new_row], ignore_index=True)

        try:
            # Salvar o novo template no arquivo
            df_templates.to_csv(file_path, index=False)
            status_label.config(text="Novo template adicionado com sucesso!", fg="green")
            clear_status_after_delay(status_label, 3)

            # Recarregar as telas relevantes
            reload_management_screen(combo_box_manage, file_path)  # Atualizar a tela de gerenciamento
            reload_main_screen()

            # Limpar campos
            clear_template_fields(template_entry, new_message_text, new_required_fields_entry)

        except Exception as e:
            status_label.config(text=f"Erro ao salvar: {e}", fg="red")

    # Limpa os campos de template
    def clear_template_fields(template_entry, message_text, required_fields_entry):
        template_entry.delete(0, tk.END)  # Limpa o campo do nome do template
        message_text.delete(1.0, tk.END)  # Limpa o campo de conteúdo do template
        required_fields_entry.delete(0, tk.END)  # Limpa o campo de campos obrigatórios

    def show_section(frame_to_hide, frame_to_show):
        frame_to_hide.grid_remove()  # Oculta o frame passado como primeiro argumento
        frame_to_show.grid(row=2, column=0, padx=10, pady=5)  # Exibe o frame passado como segundo argumento

    def reload_management_screen(combo_box_manage, file_path):
        global df_templates  # Certifique-se de que o DataFrame global seja atualizado
        df_templates = reload_templates(file_path)

        # Atualizar o ComboBox na tela de gerenciamento
        combo_box_manage['values'] = list(df_templates['Template'])

    def reload_templates(file_path):
        try:
            df_templates = pd.read_csv(file_path)
            return df_templates
        except Exception as e:
            print(f"Erro ao carregar templates do CSV: {e}")
            return pd.DataFrame(columns=["Template", "Message", "Obrigatório"])

    # Função para alternar entre as seções de edição e criação
    def show_edit_section():
        create_frame.grid_remove()
        edit_frame.grid(row=2, column=0, padx=10, pady=5)

    def show_create_section():
        edit_frame.grid_remove()
        create_frame.grid(row=2, column=0, padx=10, pady=5)

    # Inicializando ComboBox de edição
    combo_box_manage = ttk.Combobox(edit_frame, values=list(df_templates['Template']))
    combo_box_manage.grid(row=1, column=0, padx=10, pady=5)


    save_button = tk.Button(edit_frame, text="Salvar Alterações",
                            command=lambda: save_edit(df_templates, file_path, status_label, combo_box_manage))
    save_button.grid(row=6, column=0, padx=10, pady=5)

    delete_button = tk.Button(edit_frame, text="Excluir Template",
                              command=lambda: delete_template(combo_box_manage, file_path, status_label,
                                                              text_box, required_fields_entry))
    delete_button.grid(row=7, column=0, padx=10, pady=5)

    tk.Label(create_frame, text="Nome do Novo Template").grid(row=1, column=0, padx=10, pady=5)
    template_entry = tk.Entry(create_frame, width=40)
    template_entry.grid(row=2, column=0, padx=10, pady=5)

    tk.Label(create_frame, text="Conteúdo do Novo Template").grid(row=3, column=0, padx=10, pady=5)
    new_message_text = tk.Text(create_frame, wrap=tk.WORD, width=60, height=10)
    new_message_text.grid(row=4, column=0, padx=10, pady=10)

    tk.Label(create_frame, text="Campos Obrigatórios").grid(row=5, column=0, padx=10, pady=5)
    new_required_fields_entry = tk.Entry(create_frame, width=40)
    new_required_fields_entry.grid(row=6, column=0, padx=10, pady=5)

    # Faz o bind do evento de seleção no ComboBox
    combo_box_manage.bind("<<ComboboxSelected>>",
                          lambda event: update_template_fields(event, combo_box_manage, text_box, required_fields_entry,
                                                               file_path))

    add_button = tk.Button(create_frame, text="Adicionar Novo Template",
                           command=lambda: add_new_template(template_entry, new_message_text,
                                                            new_required_fields_entry,
                                                            file_path, status_label, combo_box_manage))
    add_button.grid(row=7, column=0, padx=10, pady=10)

    toggle_frame = tk.Frame(management_window)
    toggle_frame.grid(row=1, column=0, pady=10)

    edit_section_button = tk.Button(toggle_frame, text="Editar Template", command=lambda: show_section(create_frame, edit_frame))
    edit_section_button.grid(row=0, column=0, padx=10)

    create_section_button = tk.Button(toggle_frame, text="Adicionar Novo Template",
                                      command=lambda: show_section(edit_frame, create_frame))
    create_section_button.grid(row=0, column=1, padx=10)

    # Permitir redimensionamento
    management_window.resizable(True, True)

    # Ajustar o tamanho com base no conteúdo
    management_window.update_idletasks()
    management_window.update_idletasks()
    management_window.geometry(f"{management_window.winfo_width()}x{management_window.winfo_height()}")

    show_section(edit_frame, create_frame)

# Função para abrir a janela de gerenciamento de grupos solucionadores
def open_group_management_window(parent_window, df_groups, groups_file, main_group_combo_box, reload_main_screen):
    # Fecha a janela principal ao abrir a janela de gerenciamento
    parent_window.withdraw()

    group_window = tk.Toplevel(parent_window)
    group_window.title("Gerenciamento de Grupos")

    def on_close():
        # Reabre a janela principal quando a janela de gerenciamento for fechada
        parent_window.deiconify()
        group_window.destroy()
        reload_main_screen()

    group_window.protocol("WM_DELETE_WINDOW", on_close)

    # Label para exibir o status
    status_label = tk.Label(group_window, text="", fg="red")
    status_label.grid(row=10, column=0, padx=10, pady=5)

    # Função para salvar a edição de um grupo
    def save_group_edit(group_combo_box, group_name_entry, df_groups, groups_file, status_label):
        selected_group = group_combo_box.get()
        new_group_name = group_name_entry.get().strip()

        if not selected_group:
            # Exibe mensagem de erro se nenhum grupo for selecionado
            status_label.config(text="Selecione um grupo para editar.", fg="red")
            return

        if not new_group_name:
            # Exibe mensagem de erro se o novo nome do grupo estiver vazio
            status_label.config(text="O nome do grupo não pode estar vazio.", fg="red")
            return

        # Verifica se o grupo selecionado existe e atualiza o nome do grupo
        df_groups.loc[df_groups['Grupo'] == selected_group, 'Grupo'] = new_group_name
        try:
            # Salva o DataFrame atualizado no CSV
            df_groups.to_csv(groups_file, index=False)

            # Atualiza o ComboBox e exibe mensagem de sucesso
            update_group_combobox(group_combo_box, df_groups)  # Atualiza o ComboBox com novos valores
            group_combo_box.set('')  # Limpa a seleção do ComboBox
            group_name_entry.delete(0, tk.END)  # Limpa o campo de entrada de nome

            # Mensagem de sucesso
            status_label.config(text="Grupo atualizado com sucesso!", fg="green")

            # Limpa a mensagem de status após 3 segundos
            clear_status_after_delay(status_label, 3)

            # Atualizar o ComboBox de grupos na tela principal
            reload_group_screen(group_combo_box, solucionadores_path)
        except Exception as e:
            # Exibe mensagem de erro caso haja problemas ao salvar
            status_label.config(text=f"Erro ao salvar: {e}", fg="red")

    # Função para excluir um grupo
    def delete_group(group_combo_box, df_groups, groups_file, status_label):
        selected_group = group_combo_box.get()

        if selected_group:
            # Remover o grupo selecionado do DataFrame
            df_groups.drop(df_groups[df_groups['Grupo'] == selected_group].index, inplace=True)

            try:
                # Salvar o DataFrame atualizado no CSV
                df_groups.to_csv(groups_file, index=False)

                # Atualizar a mensagem de status
                status_label.config(text=f"Grupo '{selected_group}' excluído com sucesso!", fg="green")

                # Limpa a mensagem de status após 3 segundos
                clear_status_after_delay(status_label, 3)

                # Atualizar o ComboBox após exclusão
                update_group_combobox(group_combo_box, df_groups)
                # Atualizar o ComboBox de grupos na tela principal
                reload_group_screen(group_combo_box, solucionadores_path)

                # Limpar a seleção do ComboBox após a exclusão
                group_combo_box.set('')
            except Exception as e:
                # Exibir mensagem de erro, caso haja falha ao salvar
                status_label.config(text=f"Erro ao excluir grupo: {e}", fg="red")
        else:
            # Exibir mensagem de erro se nenhum grupo for selecionado
            status_label.config(text="Selecione um grupo para excluir.", fg="red")

    def add_group(group_entry, df_groups, file_path, status_label, combo_box_groups):
        # Recarregar o CSV antes de adicionar
        df_groups = reload_groups(file_path)

        new_group = group_entry.get().strip()

        if not new_group:
            status_label.config(text="Erro: Preencha o nome do grupo.", fg="red")
            return

        if new_group in df_groups['Grupo'].values:
            status_label.config(text="Grupo já existe!", fg="red")
            return

        # Adicionar o novo grupo ao DataFrame
        new_row = pd.DataFrame({"Grupo": [new_group]})
        df_groups = pd.concat([df_groups, new_row], ignore_index=True)

        try:
            # Salvar o novo grupo no arquivo CSV
            df_groups.to_csv(file_path, index=False)
            status_label.config(text="Novo grupo adicionado com sucesso!", fg="green")
            clear_status_after_delay(status_label, 3)

            # Recarregar os grupos atualizados no ComboBox
            reload_group_screen(combo_box_groups, solucionadores_path)

            # Limpar campos
            group_entry.delete(0, tk.END)

        except Exception as e:
            status_label.config(text=f"Erro ao salvar: {e}", fg="red")

    # Função para recarregar os grupos a partir do arquivo CSV
    def reload_groups(file_path):
        try:
            df_groups = pd.read_csv(file_path)
            return df_groups
        except Exception as e:
            print(f"Erro ao carregar grupos do CSV: {e}")
            return pd.DataFrame(columns=["Grupo"])

    # Função para atualizar o ComboBox com os grupos
    def update_group_combobox(group_combo_box, df_groups):
        group_combo_box['values'] = list(df_groups['Grupo'])
        group_combo_box.set('')  # Limpa a seleção do ComboBox após a atualização

    def reload_group_screen(combo_box_groups, file_path):
        global df_groups  # Certifique-se de que o DataFrame global seja atualizado
        df_groups = reload_groups(file_path)

        # Atualizar o ComboBox de grupos
        combo_box_groups['values'] = list(df_groups['Grupo'])
        combo_box_groups.set('')  # Limpar a seleção atual

    def update_group_display(*args):
        selected_group = group_combo_box.get()  # group_combo_box é o widget ComboBox
        if selected_group:
            print(f"Grupo selecionado: {selected_group}")
            # Adicione aqui o que você deseja fazer com o grupo selecionado


    # Interface para gerenciamento de grupos
    tk.Label(group_window, text="Selecionar Grupo para Editar ou Excluir").grid(row=0, column=0, padx=10, pady=5)

    # ComboBox para selecionar o grupo a ser editado ou excluído
    group_combo_box = ttk.Combobox(group_window, values=list(df_groups['Grupo']), width=40)
    group_combo_box.grid(row=1, column=0, padx=10, pady=5)
    # Ligar o listener
    group_combo_box.bind("<<ComboboxSelected>>", update_group_display)

    # Entrada para editar o nome do grupo selecionado
    tk.Label(group_window, text="Nome do Grupo").grid(row=2, column=0, padx=10, pady=5)
    group_name_entry = tk.Entry(group_window, width=40)
    group_name_entry.grid(row=3, column=0, padx=10, pady=5)

    # Botão para salvar as alterações no grupo
    save_button = tk.Button(group_window, text="Salvar Alterações",
                            command=lambda: save_group_edit(group_combo_box, group_name_entry, df_groups, groups_file,
                                                            status_label))
    save_button.grid(row=4, column=0, padx=10, pady=5)

    # Botão para excluir o grupo selecionado
    delete_button = tk.Button(group_window, text="Excluir Grupo",
                              command=lambda: delete_group(group_combo_box, df_groups, groups_file, status_label))
    delete_button.grid(row=5, column=0, padx=10, pady=5)

    # Adicionar Novo Grupo
    tk.Label(group_window, text="Adicionar Novo Grupo").grid(row=6, column=0, padx=10, pady=20)

    # Entrada para adicionar um novo grupo
    tk.Label(group_window, text="Nome do Novo Grupo").grid(row=7, column=0, padx=10, pady=5)
    add_group_entry = tk.Entry(group_window, width=40)
    add_group_entry.grid(row=8, column=0, padx=10, pady=5)

    # Botão para adicionar o novo grupo
    add_button = tk.Button(group_window, text="Adicionar Grupo",
                           command=lambda: add_group(add_group_entry, df_groups, groups_file, status_label,
                                                     group_combo_box))
    add_button.grid(row=9, column=0, padx=10, pady=10)

    # Permitir redimensionamento
    group_window.resizable(True, True)

    # Ajustar o tamanho com base no conteúdo
    group_window.update_idletasks()
    group_window.geometry(f"{group_window.winfo_width()}x{group_window.winfo_height()}")


