"""
models/agendamento.py
=====================
Camada de Entidades (Model) - Entidade Relacional / Transacional.

Esta classe conecta Paciente (Entidade A) com Médico (Entidade B).

DICA DE ENGENHARIA REVERSA:
    Agendamento -> Pedido, Matrícula, Reserva...
    paciente_id -> cliente_id, aluno_id...
    medico_id   -> produto_id, curso_id, quarto_id...
    data / hora -> (mantém, ou troque por status, valor, etc.)
"""

from typing import Optional


class Agendamento:
    """Representa um agendamento de consulta na clínica."""

    def __init__(
        self,
        id: Optional[int],
        paciente_id: int,
        medico_id: int,
        data: str,
        hora: str,
        # Campos extras para exibição (preenchidos por JOIN no controller)
        nome_paciente: str = "",
        nome_medico: str = "",
        especialidade: str = "",
    ):
        # TODO: altere para a sua entidade transacional
        self.id = id
        self.paciente_id = paciente_id
        self.medico_id = medico_id
        self.data = data
        self.hora = hora
        # Campos auxiliares (não persistidos — vêm do JOIN)
        self.nome_paciente = nome_paciente
        self.nome_medico = nome_medico
        self.especialidade = especialidade

    def __repr__(self) -> str:
        return (
            f"Agendamento(id={self.id}, paciente='{self.nome_paciente}', "
            f"medico='{self.nome_medico}', data='{self.data}', hora='{self.hora}')"
        )
