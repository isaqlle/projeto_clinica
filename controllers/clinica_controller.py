"""
controllers/clinica_controller.py
==================================
Camada de Negócio (Controller) - CRUD completo + regras de negócio.

Aqui ficam todas as funções que interagem com o banco de dados.
A View (interface) chama estas funções e nunca acessa o banco diretamente.

DICA DE ENGENHARIA REVERSA:
    Altere os nomes das funções e das queries SQL para o seu tema.
    A ESTRUTURA (abrir conexão -> executar query -> fechar conexão) é sempre a mesma.
"""

import sys
import os
from typing import List, Optional

# Garante que o Python encontre o pacote 'database' na raiz do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.conexao import obter_conexao
from models.paciente import Paciente
from models.medico import Medico
from models.agendamento import Agendamento


# ==============================================================
#  PACIENTES — Entidade Simples A
# ==============================================================

def cadastrar_paciente(nome: str, telefone: str) -> None:
    """Insere um novo paciente no banco de dados."""
    # TODO: adapte a tabela e colunas para o seu tema
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pacientes (nome, telefone) VALUES (?, ?)",
        (nome, telefone),
    )
    conn.commit()
    conn.close()


def listar_pacientes() -> List[Paciente]:
    """Retorna todos os pacientes cadastrados."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone FROM pacientes ORDER BY nome")
    linhas = cursor.fetchall()
    conn.close()
    return [Paciente(l["id"], l["nome"], l["telefone"]) for l in linhas]


def buscar_paciente_por_id(paciente_id: int) -> Optional[Paciente]:
    """Busca um único paciente pelo ID."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, telefone FROM pacientes WHERE id = ?", (paciente_id,)
    )
    linha = cursor.fetchone()
    conn.close()
    if linha:
        return Paciente(linha["id"], linha["nome"], linha["telefone"])
    return None


def atualizar_paciente(paciente_id: int, nome: str, telefone: str) -> None:
    """Atualiza os dados de um paciente existente."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pacientes SET nome = ?, telefone = ? WHERE id = ?",
        (nome, telefone, paciente_id),
    )
    conn.commit()
    conn.close()


def deletar_paciente(paciente_id: int) -> None:
    """Remove um paciente e seus agendamentos vinculados."""
    conn = obter_conexao()
    cursor = conn.cursor()
    # Remove agendamentos vinculados primeiro (integridade referencial manual)
    cursor.execute(
        "DELETE FROM agendamentos WHERE paciente_id = ?", (paciente_id,)
    )
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    conn.commit()
    conn.close()


# ==============================================================
#  MÉDICOS — Entidade Simples B
# ==============================================================

def cadastrar_medico(nome: str, especialidade: str) -> None:
    """Insere um novo médico no banco de dados."""
    # TODO: adapte a tabela e colunas para o seu tema
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicos (nome, especialidade) VALUES (?, ?)",
        (nome, especialidade),
    )
    conn.commit()
    conn.close()


def listar_medicos() -> List[Medico]:
    """Retorna todos os médicos cadastrados."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, especialidade FROM medicos ORDER BY nome"
    )
    linhas = cursor.fetchall()
    conn.close()
    return [Medico(l["id"], l["nome"], l["especialidade"]) for l in linhas]


def buscar_medico_por_id(medico_id: int) -> Optional[Medico]:
    """Busca um único médico pelo ID."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, especialidade FROM medicos WHERE id = ?", (medico_id,)
    )
    linha = cursor.fetchone()
    conn.close()
    if linha:
        return Medico(linha["id"], linha["nome"], linha["especialidade"])
    return None


def atualizar_medico(medico_id: int, nome: str, especialidade: str) -> None:
    """Atualiza os dados de um médico existente."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE medicos SET nome = ?, especialidade = ? WHERE id = ?",
        (nome, especialidade, medico_id),
    )
    conn.commit()
    conn.close()


def deletar_medico(medico_id: int) -> None:
    """Remove um médico e seus agendamentos vinculados."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM agendamentos WHERE medico_id = ?", (medico_id,)
    )
    cursor.execute("DELETE FROM medicos WHERE id = ?", (medico_id,))
    conn.commit()
    conn.close()


# ==============================================================
#  AGENDAMENTOS — Entidade Transacional (JOIN)
# ==============================================================

def cadastrar_agendamento(
    paciente_id: int, medico_id: int, data: str, hora: str
) -> None:
    """Insere um novo agendamento no banco de dados."""
    # TODO: adapte para o seu tema (ex: pedido, matrícula, reserva)
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO agendamentos (paciente_id, medico_id, data, hora) VALUES (?, ?, ?, ?)",
        (paciente_id, medico_id, data, hora),
    )
    conn.commit()
    conn.close()


def listar_agendamentos() -> List[Agendamento]:
    """
    Retorna todos os agendamentos com dados completos (JOIN).
    Este é o exemplo central de consulta com múltiplas tabelas.
    """
    conn = obter_conexao()
    cursor = conn.cursor()
    query = """
        SELECT
            a.id,
            a.paciente_id,
            a.medico_id,
            a.data,
            a.hora,
            p.nome   AS nome_paciente,
            m.nome   AS nome_medico,
            m.especialidade
        FROM agendamentos a
        JOIN pacientes p ON a.paciente_id = p.id
        JOIN medicos   m ON a.medico_id   = m.id
        ORDER BY a.data, a.hora
    """
    cursor.execute(query)
    linhas = cursor.fetchall()
    conn.close()

    return [
        Agendamento(
            id=l["id"],
            paciente_id=l["paciente_id"],
            medico_id=l["medico_id"],
            data=l["data"],
            hora=l["hora"],
            nome_paciente=l["nome_paciente"],
            nome_medico=l["nome_medico"],
            especialidade=l["especialidade"],
        )
        for l in linhas
    ]


def deletar_agendamento(agendamento_id: int) -> None:
    """Remove um agendamento pelo ID."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
    conn.commit()
    conn.close()


# ==============================================================
#  RELATÓRIO DIFERENCIAL — Consulta avançada com filtro
# ==============================================================

def listar_agendamentos_por_especialidade(especialidade: str) -> List[Agendamento]:
    """
    DIFERENCIAL: Retorna agendamentos filtrados por especialidade médica.

    DICA DE ENGENHARIA REVERSA:
        - Delivery: filtrar pedidos por bairro ou status
        - Academia: filtrar matrículas por modalidade
        - Hotel: filtrar reservas por tipo de quarto
    """
    conn = obter_conexao()
    cursor = conn.cursor()
    query = """
        SELECT
            a.id,
            a.paciente_id,
            a.medico_id,
            a.data,
            a.hora,
            p.nome   AS nome_paciente,
            m.nome   AS nome_medico,
            m.especialidade
        FROM agendamentos a
        JOIN pacientes p ON a.paciente_id = p.id
        JOIN medicos   m ON a.medico_id   = m.id
        WHERE m.especialidade = ?
        ORDER BY a.data, a.hora
    """
    cursor.execute(query, (especialidade,))
    linhas = cursor.fetchall()
    conn.close()

    return [
        Agendamento(
            id=l["id"],
            paciente_id=l["paciente_id"],
            medico_id=l["medico_id"],
            data=l["data"],
            hora=l["hora"],
            nome_paciente=l["nome_paciente"],
            nome_medico=l["nome_medico"],
            especialidade=l["especialidade"],
        )
        for l in linhas
    ]


def listar_especialidades() -> List[str]:
    """Retorna todas as especialidades cadastradas (para popular o filtro)."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT especialidade FROM medicos ORDER BY especialidade"
    )
    linhas = cursor.fetchall()
    conn.close()
    return [l["especialidade"] for l in linhas]
