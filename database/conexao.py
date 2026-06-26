"""
database/conexao.py
===================
Camada de Dados - Gerenciamento da conexão com o banco SQLite.

DICA DE ENGENHARIA REVERSA:
    Altere apenas o nome do arquivo .db para o tema do seu projeto
    (ex: academia.db, delivery.db, hotel.db).
    O restante desta camada permanece idêntico.
"""

import sqlite3
import os

# Caminho do arquivo do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(BASE_DIR, "clinica.db")


def obter_conexao() -> sqlite3.Connection:
    """Retorna uma conexão aberta com o banco de dados."""
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    return conn


def inicializar_banco() -> None:
    """
    Lê o arquivo scripts_sql.sql e cria as tabelas caso ainda não existam.
    Deve ser chamado uma única vez na inicialização do sistema (em main.py).
    """
    caminho_sql = os.path.join(BASE_DIR, "scripts_sql.sql")

    with open(caminho_sql, "r", encoding="utf-8") as arquivo:
        ddl = arquivo.read()

    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.executescript(ddl)
    conn.commit()
    conn.close()
    print("[DB] Banco de dados inicializado com sucesso.")
