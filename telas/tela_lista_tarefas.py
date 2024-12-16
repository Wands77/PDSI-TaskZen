import flet as ft
from data.database import carregar_tarefas, atualizar_status_tarefa
from datetime import datetime
from telas.tela_tarefa_detalhes import tela_tarefa_detalhes

def tela_lista_tarefas(page: ft.Page, user_id: int):
    categorias = ["Todas", "Pessoal", "Profissional", "Estudo"]
    status_opcoes = ["Pendente", "Em Progresso", "Concluído"]

    def abrir_tarefa(tarefa):
        page.clean()
        tela_tarefa_detalhes(page, tarefa, user_id)

    def voltar_tela_inicial(e):
        page.clean()
        from telas.tela_inicial import main
        main(page, user_id)

    def atualizar_status(id_tarefa, novo_status):
        atualizar_status_tarefa(id_tarefa, novo_status)

        tarefas = carregar_tarefas(user_id)

        tarefas_em_progresso = [
            t for t in tarefas if t[6] == "Em Progresso" and datetime.strptime(t[3], "%d/%m/%Y %H:%M") >= datetime.now()
        ]
        tarefas_pendentes = [
            t for t in tarefas if t[6] == "Pendente" and datetime.strptime(t[3], "%d/%m/%Y %H:%M") >= datetime.now()
        ]
        tarefas_vencidas = [
            t for t in tarefas if datetime.strptime(t[3], "%d/%m/%Y %H:%M") < datetime.now() and t[6] != "Concluído"
        ]
        tarefas_concluidas = [t for t in tarefas if t[6] == "Concluído"]

        tarefas_em_progresso.sort(key=lambda t: datetime.strptime(t[3], "%d/%m/%Y %H:%M"))
        tarefas_pendentes.sort(key=lambda t: datetime.strptime(t[3], "%d/%m/%Y %H:%M"))

        tarefas_ordenadas = tarefas_em_progresso + tarefas_pendentes + tarefas_vencidas + tarefas_concluidas

        renderizar_tarefas(tarefas_ordenadas)


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
        page.dialog.open = False
        page.dialog = None
        page.update()

    def abrir_filtro(e):
        atualizar_categorias()
        categoria_dropdown.options = [ft.dropdown.Option(c) for c in categorias]
        page.dialog = filtro_dialog
        page.dialog.open = True
        page.update()

    def fechar_filtro(e):
        page.dialog.open = False
        page.dialog = None
        page.update()

    def abrir_ordenacao(e):
        page.dialog = ordenacao_dialog
        page.dialog.open = True
        page.update()

    def fechar_ordenacao(e):
        page.dialog.open = False
        page.dialog = None
        page.update()

    def aplicar_ordenacao(e):
        opcao = ordenacao_dropdown.value
        tarefas = carregar_tarefas(user_id)

        tarefas_pendentes_em_progresso = [
            t for t in tarefas if t[6] not in ["Concluído"] and datetime.strptime(t[3], "%d/%m/%Y %H:%M") >= datetime.now()
        ]
        tarefas_vencidas = [
            t for t in tarefas if datetime.strptime(t[3], "%d/%m/%Y %H:%M") < datetime.now() and t[6] != "Concluído"
        ]
        tarefas_concluidas = [t for t in tarefas if t[6] == "Concluído"]

        if opcao == "Prioridade":
            prioridade_ordem = {"Alta": 0, "Média": 1, "Baixa": 2}
            tarefas_pendentes_em_progresso.sort(
                key=lambda t: (
                    prioridade_ordem.get(t[4], 3), 
                    datetime.strptime(t[3], "%d/%m/%Y %H:%M"), 
                )
            )
        elif opcao == "Prazo":
            tarefas_pendentes_em_progresso.sort(
                key=lambda t: datetime.strptime(t[3], "%d/%m/%Y %H:%M")
            )

        tarefas_ordenadas = tarefas_pendentes_em_progresso + tarefas_vencidas + tarefas_concluidas

        renderizar_tarefas(tarefas_ordenadas)

        page.dialog.open = False
        page.dialog = None
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
            tabela_tarefas.controls.append(
                ft.Row(
                    [
                        ft.Text("Título", expand=1, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("Categoria", expand=1, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("Prazo", expand=1, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("Prioridade", expand=1, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("Status", expand=1, weight=ft.FontWeight.BOLD, size=14),
                    ],
                    spacing=10,
                )
            )

            for tarefa in tarefas:
                id, titulo, descricao, prazo, prioridade, categoria, status = tarefa

                prazo_exibido = (
                    "Vencida" if datetime.strptime(prazo, "%d/%m/%Y %H:%M") < datetime.now() and status != "Concluído"
                    else "Finalizado" if status == "Concluído"
                    else calcular_tempo_restante(prazo)
                )
                prazo_cor = (
                    "red" if prazo_exibido == "Vencida"
                    else "green" if status == "Concluído"
                    else "black"
                )

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
                            ft.Text(
                                prazo_exibido,
                                expand=1,
                                size=12,
                                color=prazo_cor,
                            ),
                            ft.Text(prioridade, expand=1, size=12),
                            ft.Dropdown(
                                value=status,
                                options=[
                                    ft.dropdown.Option("Pendente", text_style=ft.TextStyle(color="red", size=10)),
                                    ft.dropdown.Option("Em Progresso", text_style=ft.TextStyle(color="orange", size=10)),
                                    ft.dropdown.Option("Concluído", text_style=ft.TextStyle(color="green", size=10)),
                                ],
                                on_change=lambda e, t_id=id: atualizar_status(t_id, e.control.value),
                                expand=1,
                                height=40,
                            ),
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

    ordenacao_dropdown = ft.Dropdown(
        label="Ordenar por",
        options=[
            ft.dropdown.Option("Prioridade"),
            ft.dropdown.Option("Prazo"),
        ],
        width=320,
    )

    filtro_dialog = ft.AlertDialog(
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
        actions=[
            ft.ElevatedButton("Aplicar", on_click=aplicar_filtro, width=150, height=45),
            ft.ElevatedButton("Fechar", on_click=fechar_filtro, width=150, height=45),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    ordenacao_dialog = ft.AlertDialog(
        title=ft.Text("Ordenar Tarefas", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                ordenacao_dropdown,
            ],
            spacing=20,
        ),
        actions=[
            ft.ElevatedButton("Aplicar", on_click=aplicar_ordenacao, width=150, height=45),
            ft.ElevatedButton("Fechar", on_click=fechar_ordenacao, width=150, height=45),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(
        ft.Column(
            [
                ft.Text("Lista de Tarefas", size=20, weight=ft.FontWeight.BOLD, color="black"),
                ft.Row(
                    [
                        ft.ElevatedButton("Filtrar", on_click=abrir_filtro, width=150, height=45),
                        ft.ElevatedButton("Ordenar", on_click=abrir_ordenacao, width=150, height=45),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
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

    tarefas_do_usuario = carregar_tarefas(user_id)
    renderizar_tarefas(tarefas_do_usuario)
