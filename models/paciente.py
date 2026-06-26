"""
models/paciente.py
==================
Camada de Entidades (Model) - Entidade Simples A.

DICA DE ENGENHARIA REVERSA:
    Renomeie esta classe e seus atributos para o seu tema:
        Paciente -> Cliente, Aluno, Hóspede...
        nome     -> (mantém)
        telefone -> email, cpf, curso...
"""

from typing import Optional


class Paciente:
    """Representa um paciente cadastrado na clínica."""

    def __init__(self, id: Optional[int], nome: str, telefone: str):
        # TODO: altere os atributos para a sua entidade principal
        self.id = id
        self.nome = nome
        self.telefone = telefone

    def __repr__(self) -> str:
        return f"Paciente(id={self.id}, nome='{self.nome}', telefone='{self.telefone}')"
