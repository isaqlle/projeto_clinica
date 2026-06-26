# Clínica Vida+ — Projeto Modelo (Padrão Ouro)

Sistema de Agendamentos para a Clínica Vida+, desenvolvido em Python com
SQLite e Tkinter. Este projeto é o **código-modelo** que serve de base para
engenharia reversa por outros grupos.

---

## ▶️ Como Executar

```bash
# Não precisa instalar nada além do Python padrão!
python main.py
```

> Requisito: **Python 3.10+** (usa `int | None` como type hint nativo)

---

## 📁 Estrutura de Arquivos

```
projeto_clinica/
│
├── database/
│   ├── conexao.py          # Abre/fecha conexão com o SQLite
│   └── scripts_sql.sql     # DDL: criação das tabelas
│
├── models/
│   ├── paciente.py         # Entidade A (simples)
│   ├── medico.py           # Entidade B (simples)
│   └── agendamento.py      # Entidade relacional (JOIN entre A e B)
│
├── controllers/
│   └── clinica_controller.py  # Todo o CRUD + consulta diferencial
│
├── views/
│   └── app_interface.py    # Interface Tkinter (4 abas)
│
└── main.py                 # Ponto de entrada
```

---

## 🔄 Guia de Engenharia Reversa (Para os Outros Grupos)

| Este projeto (Clínica) | Delivery         | Academia          | Hotel             |
|------------------------|------------------|-------------------|-------------------|
| `pacientes`            | `clientes`       | `alunos`          | `hospedes`        |
| `medicos`              | `produtos`       | `modalidades`     | `quartos`         |
| `agendamentos`         | `pedidos`        | `matriculas`      | `reservas`        |
| `especialidade`        | `categoria`      | `tipo`            | `tipo_quarto`     |
| `data/hora`            | `data/status`    | `data_inicio`     | `check_in/out`    |

### Passo a Passo para Adaptar

1. **Banco de Dados** — Abra `database/scripts_sql.sql` e renomeie as tabelas/colunas
2. **Models** — Renomeie as classes e atributos em `models/`
3. **Controller** — Altere as queries SQL e os nomes de funções
4. **View** — Mude os labels, colunas do Treeview e títulos das abas
5. **main.py** — Altere apenas o título da janela e o import

---

## 🗄️ Banco de Dados

O banco `clinica.db` é criado automaticamente na pasta `database/`
na primeira execução. Use o **DB Browser for SQLite** para visualizá-lo.

### Diagrama ER

```
pacientes           agendamentos          medicos
─────────           ────────────          ───────
id (PK)  ◄──┐  ┌── id (PK)           ┌── id (PK)
nome         └── paciente_id (FK)     │   nome
telefone         medico_id (FK)   ────┘   especialidade
                 data
                 hora
```

---

## ✅ Funcionalidades

- [x] CRUD completo de Pacientes
- [x] CRUD completo de Médicos
- [x] Cadastro e cancelamento de Agendamentos
- [x] Consulta com JOIN (Agendamentos exibe nome do paciente e médico)
- [x] Relatório diferencial: filtrar agendamentos por especialidade
- [x] Interface gráfica com 4 abas (Tkinter nativo, sem dependências externas)

---

## 📝 Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.10+ | Linguagem principal |
| `sqlite3` | Banco de dados (nativo, sem instalação) |
| `tkinter` | Interface gráfica (nativo, sem instalação) |

> **Nenhuma instalação de pacote externo é necessária.**
