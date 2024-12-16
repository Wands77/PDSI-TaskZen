import flet as ft
import asyncio
from data.database import inicializar_banco_usuarios, inicializar_banco_tarefas
from data.sessao import carregar_sessao
from utils.notificacoes import buscar_tarefas_para_notificacao


async def verificar_notificacoes(page: ft.Page, user_id):
    """
    Loop contínuo para verificar notificações em segundo plano.
    """
    while True:
        print("Verificando notificações...")
        notificacoes = buscar_tarefas_para_notificacao(user_id)
        if notificacoes:
            for notificacao in notificacoes:
                print(f"Exibindo: {notificacao}")  # Log de depuração
                snack_bar = ft.SnackBar(
                    content=ft.Text(notificacao),
                    action="OK",
                    bgcolor=ft.colors.RED_400,
                    duration=10000  # 10 segundos
                )
                page.overlay.append(snack_bar)  # Adiciona ao overlay
                snack_bar.open = True  # Abre o SnackBar
                page.update()  # Atualiza a página para exibição
        await asyncio.sleep(60)  # Aguarda 60 segundos antes de verificar novamente


async def main(page: ft.Page):
    # Inicializa o banco de dados
    inicializar_banco_usuarios()
    inicializar_banco_tarefas()

    # Verifica se há sessão ativa
    user_id = carregar_sessao()
    if user_id:
        # Inicia a verificação de notificações em background
        asyncio.create_task(verificar_notificacoes(page, user_id))

        # Redireciona para a tela inicial
        from telas.tela_inicial import main as tela_inicial
        tela_inicial(page, user_id=user_id)
    else:
        # Redireciona para a tela de login
        from telas.login import tela_login
        tela_login(page)


if __name__ == "__main__":
    ft.app(target=main)
