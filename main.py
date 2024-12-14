import flet as ft
from data.database import inicializar_banco_usuarios, inicializar_banco_tarefas
from data.sessao import carregar_sessao

def main(page: ft.Page):
    # Inicializa os bancos de dados
    inicializar_banco_usuarios()
    inicializar_banco_tarefas()

    # Verifica se há uma sessão ativa
    user_id = carregar_sessao()
    if user_id:
        from telas.tela_inicial import main as tela_inicial
        tela_inicial(page, user_id=user_id)  # Vai direto para a tela inicial
    else:
        # Exibe a tela de login
        from telas.login import tela_login
        tela_login(page)

if __name__ == "__main__":
    ft.app(target=main)
