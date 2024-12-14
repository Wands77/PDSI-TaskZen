import flet as ft
from data.database import adicionar_tarefa
from datetime import datetime

def tela_cadastrar_tarefa(page: ft.Page, user_id: int):
    categorias = ["Pessoal", "Profissional", "Estudo"]

    def salvar_tarefa(e):
        titulo = titulo_input.value.strip()
        descricao = descricao_input.value.strip()
        vencimento = vencimento_input.value.strip()
        prioridade = prioridade_dropdown.value
        categoria = categoria_dropdown.value

        if categoria == "Outra?":
            nova_categoria = nova_categoria_input.value.strip()
            if not nova_categoria:
                mensagem.value = "Digite uma nova categoria!"
                mensagem.color = "red"
                page.update()
                return
            categoria = nova_categoria
            if categoria not in categorias:
                categorias.append(categoria)  # Adiciona a nova categoria na lista
                categoria_dropdown.options = [ft.dropdown.Option(c) for c in categorias + ["Outra?"]]
                categoria_dropdown.value = categoria
                nova_categoria_input.value = ""
                nova_categoria_input.visible = False

        if not (titulo and descricao and vencimento and prioridade and categoria):
            mensagem.value = "Todos os campos são obrigatórios!"
            mensagem.color = "red"
            page.update()
            return

        try:
            data_vencimento = datetime.strptime(vencimento, "%d/%m/%Y %H:%M")
            if data_vencimento <= datetime.now():
                mensagem.value = "A data e hora de vencimento devem ser futuras!"
                mensagem.color = "red"
                page.update()
                return
        except ValueError:
            mensagem.value = "Data inválida! Use o formato DD/MM/AAAA HH:MM."
            mensagem.color = "red"
            page.update()
            return

        # Salva a tarefa no banco de dados
        adicionar_tarefa(user_id, titulo, descricao, vencimento, prioridade, categoria)
        mensagem.value = "Tarefa salva com sucesso!"
        mensagem.color = "green"
        page.update()

        # Retorna à tela inicial, passando o `user_id`
        page.clean()
        from telas.tela_inicial import main
        main(page, user_id)  # Passa o ID do usuário

    def voltar_tela_inicial(e):
        page.clean()
        from telas.tela_inicial import main
        main(page, user_id)  # Passa o ID do usuário
    
    def mostrar_nova_categoria(e):
        if categoria_dropdown.value == "Outra?":
            nova_categoria_input.visible = True
        else:
            nova_categoria_input.visible = False
        page.update()

    # Campos de entrada
    titulo_input = ft.TextField(label="Título:", width=320)
    descricao_input = ft.TextField(label="Descrição:", multiline=True, height=120, width=320)
    vencimento_input = ft.TextField(label="Vencimento (DD/MM/AAAA HH:MM):", width=320)
    prioridade_dropdown = ft.Dropdown(
        label="Prioridade:", options=[ft.dropdown.Option(p) for p in ["Alta", "Média", "Baixa"]], width=320
    )
    categoria_dropdown = ft.Dropdown(
        label="Categoria:",
        options=[ft.dropdown.Option(c) for c in categorias + ["Outra?"]],
        width=320,
        on_change=mostrar_nova_categoria,  # Detecta mudança no valor do dropdown
    )
    nova_categoria_input = ft.TextField(label="Nova Categoria:", width=320, visible=False)
    mensagem = ft.Text(value="", size=14)

    # Layout da página
    page.add(
        ft.Column(
            [
                ft.Text("Nova Tarefa", size=20, weight=ft.FontWeight.BOLD, color="black"),
                titulo_input,
                descricao_input,
                vencimento_input,
                prioridade_dropdown,
                categoria_dropdown,
                nova_categoria_input,
                mensagem,
                ft.Row(
                    [
                        ft.ElevatedButton("Voltar", on_click=voltar_tela_inicial, width=150, height=45),
                        ft.ElevatedButton("Salvar", on_click=salvar_tarefa, width=150, height=45),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
    )
