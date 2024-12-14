import flet as ft
from data.database import excluir_tarefa, atualizar_tarefa

def tela_tarefa_detalhes(page: ft.Page, tarefa, usuario_id: int):
    tarefa_id, titulo, descricao, prazo, prioridade, categoria = tarefa

    def excluir(e):
        excluir_tarefa(tarefa_id)
        page.clean()
        from telas.tela_lista_tarefas import tela_lista_tarefas
        tela_lista_tarefas(page, usuario_id)

    def salvar(e):
        categoria_final = categoria_dropdown.value
        if categoria_final == "Outra?":
            categoria_final = nova_categoria_input.value.strip()
            if not categoria_final:
                mensagem.value = "Digite uma nova categoria!"
                mensagem.color = "red"
                page.update()
                return
            if categoria_final not in categorias:
                categorias.append(categoria_final)
                categoria_dropdown.options = [ft.dropdown.Option(c) for c in categorias + ["Outra?"]]
                categoria_dropdown.value = categoria_final

        atualizar_tarefa(
            tarefa_id,
            titulo_input.value,
            descricao_input.value,
            prazo_input.value,
            prioridade_dropdown.value,
            categoria_final,
        )
        page.clean()
        from telas.tela_lista_tarefas import tela_lista_tarefas
        tela_lista_tarefas(page, usuario_id)

    def voltar_tela_inicial(e):
        page.clean()
        from telas.tela_lista_tarefas import tela_lista_tarefas
        tela_lista_tarefas(page, usuario_id)

    def mostrar_nova_categoria(e):
        if categoria_dropdown.value == "Outra?":
            nova_categoria_input.visible = True
        else:
            nova_categoria_input.visible = False
        page.update()

    categorias = ["Pessoal", "Profissional", "Estudo"]
    if categoria not in categorias:
        categorias.append(categoria)

    prioridades = ["Alta", "Média", "Baixa"]

    titulo_input = ft.TextField(value=titulo, label="Título:", width=320)
    descricao_input = ft.TextField(value=descricao, label="Descrição:", multiline=True, height=120, width=320)
    prazo_input = ft.TextField(value=prazo, label="Prazo (DD/MM/AAAA HH:MM):", width=320)
    prioridade_dropdown = ft.Dropdown(
        value=prioridade,
        options=[ft.dropdown.Option(p) for p in prioridades],
        label="Prioridade",
        width=320,
    )
    categoria_dropdown = ft.Dropdown(
        value=categoria,
        options=[ft.dropdown.Option(c) for c in categorias + ["Outra?"]],
        label="Categoria",
        width=320,
        on_change=mostrar_nova_categoria,
    )
    nova_categoria_input = ft.TextField(label="Nova Categoria:", width=320, visible=False)
    mensagem = ft.Text(value="", size=14)

    # Ajuste do layout principal para caber na tela
    page.add(
        ft.Column(
            [
                ft.Text("Editar Tarefa", size=20, weight=ft.FontWeight.BOLD, color="black"),
                titulo_input,
                descricao_input,
                prazo_input,
                prioridade_dropdown,
                categoria_dropdown,
                nova_categoria_input,
                mensagem,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Voltar", 
                            on_click=voltar_tela_inicial, 
                            expand=1, 
                            height=45,
                        ),
                        ft.ElevatedButton(
                            "Excluir", 
                            on_click=excluir, 
                            expand=1, 
                            height=45,
                        ),
                        ft.ElevatedButton(
                            "Salvar", 
                            on_click=salvar, 
                            expand=1, 
                            height=45,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
    )
