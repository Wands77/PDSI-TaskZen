import sqlite3
import bcrypt
import re

# Função para inicializar o banco de dados de tarefas
def inicializar_banco_tarefas():
    conexao = sqlite3.connect("tarefas.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT,
            descricao TEXT,
            prazo TEXT,
            prioridade TEXT,
            categoria TEXT
        )
    """)
    conexao.commit()
    conexao.close()

# Função para inicializar o banco de dados de usuários
def inicializar_banco_usuarios():
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

# Funções relacionadas ao gerenciamento de usuários
def email_existe(email):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario is not None

def validar_login(email, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, senha FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conexao.close()
    if usuario:
        user_id, senha_armazenada = usuario
        if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
            return user_id  # Retorna o ID do usuário se o login for bem-sucedido
    return None  # Retorna None se o login falhar

def adicionar_usuario(nome, email, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
    conexao.commit()
    conexao.close()

def validar_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email)

# Funções relacionadas ao gerenciamento de tarefas
def adicionar_tarefa(usuario_id, titulo, descricao, prazo, prioridade, categoria):
    conexao = sqlite3.connect("tarefas.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO tarefas (usuario_id, titulo, descricao, prazo, prioridade, categoria)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (usuario_id, titulo, descricao, prazo, prioridade, categoria))
    conexao.commit()
    conexao.close()

def carregar_tarefas(usuario_id):
    conexao = sqlite3.connect("tarefas.db")
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, titulo, descricao, prazo, prioridade, categoria FROM tarefas WHERE usuario_id = ?
    """, (usuario_id,))
    tarefas = cursor.fetchall()
    conexao.close()
    return tarefas

def excluir_tarefa(tarefa_id):
    conexao = sqlite3.connect("tarefas.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conexao.commit()
    conexao.close()

def atualizar_tarefa(tarefa_id, titulo, descricao, prazo, prioridade, categoria):
    conexao = sqlite3.connect("tarefas.db")
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE tarefas
        SET titulo = ?, descricao = ?, prazo = ?, prioridade = ?, categoria = ?
        WHERE id = ?
    """, (titulo, descricao, prazo, prioridade, categoria, tarefa_id))
    conexao.commit()
    conexao.close()
