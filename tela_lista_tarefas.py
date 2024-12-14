import flet as ft
from data.database import carregar_tarefas
from datetime import datetime
from telas.tela_tarefa_detalhes import tela_tarefa_detalhes

def tela_lista_tarefas(page: ft.Page, user_id: int):
    categorias = ["Todas", "Pessoal", "Profissional", "Estudo"]

    def abrir_tarefa(tarefa):
        page.clean()
        tela_tarefa_detalhes(page, tarefa, user_id)

    def voltar_tela_inicial(e):
        page.clean()
        from telas.tela_inicial import main
        main(page, user_id)

    def atualizar_categorias():
        tarefas = carregar_tarefas(user_id)
        for tarefa in tarefas:
            if tarefa[5] not in categorias:
                categorias.append(tarefa[5])

    def aplicar_filtro(e):
        categoria = categoria_dropdown.value
        prioridade = prioridade_dropdown.value
        data_inicio = data_inicio_input.value.strip()
        data_fim = data_fim_input.value.strip()

        tarefas_filtradas = carregar_tarefas(user_id)

        if categoria and categoria != "Todas":
            tarefas_filtradas = [t for t in tarefas_filtradas if t[5] == categoria]
        if prioridade and prioridade != "Todas":
            tarefas_filtradas = [t for t in tarefas_filtradas if t[4] == prioridade]
        if data_inicio or data_fim:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, "%d/%m/%Y") if data_inicio else None
                data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y") if data_fim else None
                tarefas_filtradas = [
                    t for t in tarefas_filtradas if
                    (not data_inicio_dt or datetime.strptime(t[3].split()[0], "%d/%m/%Y") >= data_inicio_dt) and
                    (not data_fim_dt or datetime.strptime(t[3].split()[0], "%d/%m/%Y") <= data_fim_dt)
                ]
            except ValueError:
                mensagem.value = "Datas inválidas! Use o formato DD/MM/AAAA."
                mensagem.color = "red"
                page.update()
                return

        renderizar_tarefas(tarefas_filtradas)
        dialog.open = False
        page.update()

    def abrir_filtro(e):
        atualizar_categorias()
        categoria_dropdown.options = [ft.dropdown.Option(c) for c in categorias]
        page.update()
        dialog.open = True

    def fechar_filtro(e):
        dialog.open = False
        page.update()

    def calcular_tempo_restante(prazo_str):
        try:
            prazo = datetime.strptime(prazo_str, "%d/%m/%Y %H:%M")
            agora = datetime.now()
            delta = prazo - agora

            if delta.total_seconds() <= 0:
                return "Vencida"
            elif delta.days > 0:
                return f"{delta.days} dias"
            elif delta.seconds // 3600 > 0:
                return f"{delta.seconds // 3600} horas"
            elif delta.seconds // 60 > 0:
                return f"{delta.seconds // 60} minutos"
            else:
                return "Menos de 1 minuto"
        except Exception:
            return "Data inválida"

    def renderizar_tarefas(tarefas):
        tabela_tarefas.controls.clear()

        if not tarefas:
            tabela_tarefas.controls.append(
                ft.Text("Nenhuma tarefa encontrada.", size=16, weight=ft.FontWeight.BOLD, color="gray")
            )
        else:
            # Cabeçalho da tabela
            tabela_tarefas.controls.append(
                ft.Row(
                    [
                        ft.Text("Título", expand=1, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("Categoria", expand=1, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("Prazo", expand=1, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("Prioridade", expand=1, weight=ft.FontWeight.BOLD, size=14),
                    ],
                    spacing=10,
                )
            )

            # Linhas da tabela
            for tarefa in tarefas:
                id, titulo, descricao, prazo, prioridade, categoria = tarefa
                tempo_restante = calcular_tempo_restante(prazo)
                tabela_tarefas.controls.append(
                    ft.Row(
                        [
                            ft.TextButton(
                                text=titulo,
                                on_click=lambda e, t=tarefa: abrir_tarefa(t),
                                expand=1,
                                style=ft.ButtonStyle(
                                    padding=ft.Padding(5, 5, 5, 5),
                                    shape=ft.RoundedRectangleBorder(radius=3),
                                ),
                            ),
                            ft.Text(categoria, expand=1, size=12),
                            ft.Text(tempo_restante, expand=1, size=12),
                            ft.Text(prioridade, expand=1, size=12),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
        page.update()

    tabela_tarefas = ft.Column()

    categoria_dropdown = ft.Dropdown(
        label="Categoria",
        options=[ft.dropdown.Option(c) for c in categorias],
        width=320,
    )
    prioridade_dropdown = ft.Dropdown(
        label="Prioridade",
        options=[ft.dropdown.Option(p) for p in ["Todas", "Alta", "Média", "Baixa"]],
        width=320,
    )
    data_inicio_input = ft.TextField(label="Data Início (DD/MM/AAAA):", width=320)
    data_fim_input = ft.TextField(label="Data Fim (DD/MM/AAAA):", width=320)

    btn_aplicar_filtro = ft.ElevatedButton("Aplicar", on_click=aplicar_filtro, width=150, height=45)
    btn_fechar_filtro = ft.ElevatedButton("Fechar", on_click=fechar_filtro, width=150, height=45)

    dialog = ft.AlertDialog(
        title=ft.Text("Filtrar Tarefas", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                categoria_dropdown,
                prioridade_dropdown,
                data_inicio_input,
                data_fim_input,
            ],
            spacing=20,
        ),
        actions=[btn_aplicar_filtro, btn_fechar_filtro],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    mensagem = ft.Text(value="", size=14)

    # Layout principal
    page.add(
        ft.Column(
            [
                ft.Text("Lista de Tarefas", size=20, weight=ft.FontWeight.BOLD, color="black"),
                ft.ElevatedButton("Filtrar", on_click=abrir_filtro, width=150, height=45),
                ft.Container(
                    content=tabela_tarefas,
                    alignment=ft.alignment.center,
                    padding=10,
                ),
                ft.ElevatedButton("Voltar", on_click=voltar_tela_inicial, width=320, height=45),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

    page.dialog = dialog
    tarefas_do_usuario = carregar_tarefas(user_id)
    renderizar_tarefas(tarefas_do_usuario)
