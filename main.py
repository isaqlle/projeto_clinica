"""
main.py
=======
Ponto de entrada do sistema Clínica Vida+.

Responsabilidades:
    1. Inicializar o banco de dados (criar tabelas, se não existirem).
    2. Iniciar a interface gráfica (Tkinter).

DICA DE ENGENHARIA REVERSA:
    Este arquivo raramente muda entre os temas.
    Apenas altere o título e o import da sua interface customizada.
"""

import sys
import os

# Garante que os módulos do projeto sejam encontrados independentemente
# de onde o script é executado
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.conexao import inicializar_banco
from views.app_interface import AppClinica


def main():
    # 1. Cria as tabelas no banco SQLite (caso não existam)
    inicializar_banco()

    # 2. Inicia a interface gráfica
    app = AppClinica()
    app.mainloop()


if __name__ == "__main__":
    main()
