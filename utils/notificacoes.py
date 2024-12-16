import sqlite3
from datetime import datetime, timedelta

def buscar_tarefas_para_notificacao(usuario_id):
    """ Busca tarefas de um usuário específico e verifica se estão em momentos críticos para notificação."""
    # Conecta ao banco de dados
    try:
        conexao = sqlite3.connect("tarefas.db")
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT id, titulo, prazo
            FROM tarefas
            WHERE usuario_id = ? AND status != 'Concluído'
        """, (usuario_id,))
        tarefas = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return []
    finally:
        conexao.close()

    notificacoes = []
    agora = datetime.now()

    # Definir os intervalos de notificação
    intervalos = [
        timedelta(days=60), timedelta(days=30), timedelta(days=15),
        timedelta(days=10), timedelta(days=5), timedelta(days=4),
        timedelta(days=3), timedelta(days=2), timedelta(days=1),
        timedelta(hours=12), timedelta(hours=6), timedelta(hours=3),
        timedelta(hours=2), timedelta(hours=1), timedelta(minutes=30),
        timedelta(minutes=15), timedelta(minutes=10), timedelta(minutes=5),
        timedelta(minutes=3), timedelta(minutes=2), timedelta(minutes=1),
    ]

    for tarefa in tarefas:
        tarefa_id, titulo, prazo = tarefa

        # Converter o prazo para um objeto datetime
        try:
            prazo_datetime = datetime.strptime(prazo, "%d/%m/%Y %H:%M")
        except ValueError:
            print(f"Formato de prazo inválido para a tarefa {tarefa_id}: {prazo}")
            continue

        # Calcular a diferença de tempo
        diferenca = prazo_datetime - agora

        # Verificar se está em um dos intervalos críticos
        if any(diferenca <= intervalo and diferenca > intervalo - timedelta(minutes=5) for intervalo in intervalos):
            prazo_formatado = prazo_datetime.strftime("%d/%m/%Y %H:%M")
            notificacoes.append(f"A tarefa '{titulo}' está próxima do prazo: {prazo_formatado}")

    return notificacoes
