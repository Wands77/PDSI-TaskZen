import os
import json

SESSION_FILE = "session.json"

def salvar_sessao(user_id):
    with open(SESSION_FILE, "w") as f:
        json.dump({"user_id": user_id}, f)

def carregar_sessao():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("user_id")
    return None

def limpar_sessao():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
