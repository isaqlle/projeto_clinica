"""
models/medico.py
================
Camada de Entidades (Model) - Entidade Simples B.

DICA DE ENGENHARIA REVERSA:
    Renomeie esta classe e seus atributos para o seu tema:
        Medico        -> Produto, Professor, Entregador...
        especialidade -> categoria, disciplina, veiculo...
"""

from typing import Optional


class Medico:
    """Representa um médico cadastrado na clínica."""

    def __init__(self, id: Optional[int], nome: str, especialidade: str):
        # TODO: altere os atributos para a sua entidade secundária
        self.id = id
        self.nome = nome
        self.especialidade = especialidade

    def __repr__(self) -> str:
        return (
            f"Medico(id={self.id}, nome='{self.nome}', "
            f"especialidade='{self.especialidade}')"
        )
