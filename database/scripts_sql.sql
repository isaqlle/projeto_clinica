-- =============================================================
-- CLÍNICA VIDA+ - Scripts de Criação do Banco de Dados (DDL)
-- =============================================================
-- DICA DE ENGENHARIA REVERSA:
--   Tabela A (pacientes)    -> adapte para: Clientes, Alunos, Hóspedes...
--   Tabela B (medicos)      -> adapte para: Produtos, Professores, Quartos...
--   Tabela C (agendamentos) -> adapte para: Pedidos, Matrículas, Reservas...
-- =============================================================

-- Tabela Entidade A: Pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome     TEXT    NOT NULL,
    telefone TEXT    NOT NULL
);

-- Tabela Entidade B: Médicos
CREATE TABLE IF NOT EXISTS medicos (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT    NOT NULL,
    especialidade TEXT   NOT NULL
);

-- Tabela Transacional: Agendamentos (relaciona A <-> B + data/hora)
CREATE TABLE IF NOT EXISTS agendamentos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    medico_id   INTEGER NOT NULL,
    data        TEXT    NOT NULL,   -- formato: YYYY-MM-DD
    hora        TEXT    NOT NULL,   -- formato: HH:MM
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (medico_id)   REFERENCES medicos(id)
);
