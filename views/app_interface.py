"""
views/app_interface.py
=======================
Camada de Interface (View) - Interface gráfica com Tkinter.

Contém as telas:
    1. Aba Pacientes  — Formulário de cadastro + Treeview + Atualizar / Deletar
    2. Aba Médicos    — Formulário de cadastro + Treeview + Atualizar / Deletar
    3. Aba Agendamentos — Formulário (selecionar paciente e médico) + Treeview
    4. Aba Relatório  — Filtro por especialidade (Diferencial)

DICA DE ENGENHARIA REVERSA:
    Altere os labels, títulos e colunas do Treeview para o seu tema.
    A lógica de eventos (botões, frames, ttk.Treeview) é reaproveitável.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import controllers.clinica_controller as ctrl


# ==============================================================
#  JANELA PRINCIPAL
# ==============================================================

class AppClinica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clínica Vida+ — Sistema de Agendamentos")
        self.geometry("900x580")
        self.resizable(True, True)
        self.configure(bg="#f0f4f8")

        self._criar_cabecalho()
        self._criar_abas()

    def _criar_cabecalho(self):
        frame = tk.Frame(self, bg="#1a6fa8", pady=10)
        frame.pack(fill="x")
        tk.Label(
            frame,
            text="Clínica Vida+",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1a6fa8",
        ).pack()
        tk.Label(
            frame,
            text="Sistema de Gerenciamento de Agendamentos",
            font=("Arial", 10),
            fg="#cce4f7",
            bg="#1a6fa8",
        ).pack()

    def _criar_abas(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_pacientes    = AbaPacientes(notebook)
        self.aba_medicos      = AbaMedicos(notebook)
        self.aba_agendamentos = AbaAgendamentos(notebook)
        self.aba_relatorio    = AbaRelatorio(notebook)

        notebook.add(self.aba_pacientes,    text="Pacientes")
        notebook.add(self.aba_medicos,      text="Médicos")
        notebook.add(self.aba_agendamentos, text="Agendamentos")
        notebook.add(self.aba_relatorio,    text="Relatório")


# ==============================================================
#  FUNÇÕES AUXILIARES
# ==============================================================

def _criar_treeview(parent, colunas: List[Tuple[str, str, int]]) -> ttk.Treeview:
    """
    Cria um Treeview com scrollbar vertical.
    colunas: lista de (id, título, largura)
    """
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True, pady=5)

    ids = [c[0] for c in colunas]
    tree = ttk.Treeview(frame, columns=ids, show="headings", height=10)

    for col_id, titulo, largura in colunas:
        tree.heading(col_id, text=titulo)
        tree.column(col_id, width=largura, anchor="center")

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    return tree


def _campo(parent, label: str, row: int, col: int = 0) -> ttk.Entry:
    """Cria um label + entry e retorna o entry."""
    tk.Label(parent, text=label, bg="#f0f4f8", font=("Arial", 10)).grid(
        row=row, column=col, sticky="w", padx=5, pady=3
    )
    entry = ttk.Entry(parent, width=28)
    entry.grid(row=row, column=col + 1, sticky="ew", padx=5, pady=3)
    return entry


# ==============================================================
#  ABA PACIENTES
# ==============================================================

class AbaPacientes(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f4f8")
        self._id_selecionado = None
        self._build()
        self.carregar()

    def _build(self):
        # ---- Formulário ----
        frame_form = tk.LabelFrame(
            self, text="Dados do Paciente", bg="#f0f4f8", font=("Arial", 10, "bold")
        )
        frame_form.pack(fill="x", padx=10, pady=8)
        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        self.entry_nome     = _campo(frame_form, "Nome:",     0, 0)
        self.entry_telefone = _campo(frame_form, "Telefone:", 0, 2)

        # ---- Botões ----
        frame_btn = tk.Frame(self, bg="#f0f4f8")
        frame_btn.pack(fill="x", padx=10)

        tk.Button(frame_btn, text="Cadastrar",  bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), command=self.cadastrar).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Atualizar",  bg="#2980b9", fg="white",
                  font=("Arial", 10, "bold"), command=self.atualizar).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Deletar",   bg="#e74c3c", fg="white",
                  font=("Arial", 10, "bold"), command=self.deletar).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Limpar",    bg="#95a5a6", fg="white",
                  font=("Arial", 10, "bold"), command=self.limpar).pack(side="left", padx=4)

        # ---- Treeview ----
        self.tree = _criar_treeview(self, [
            ("id",       "ID",       50),
            ("nome",     "Nome",    250),
            ("telefone", "Telefone",150),
        ])
        self.tree.bind("<<TreeviewSelect>>", self._selecionar)

    def carregar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in ctrl.listar_pacientes():
            self.tree.insert("", "end", values=(p.id, p.nome, p.telefone))

    def cadastrar(self):
        nome     = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        if not nome or not telefone:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        ctrl.cadastrar_paciente(nome, telefone)
        self.limpar()
        self.carregar()
        messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")

    def atualizar(self):
        if not self._id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente na lista.")
            return
        nome     = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        if not nome or not telefone:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        ctrl.atualizar_paciente(self._id_selecionado, nome, telefone)
        self.limpar()
        self.carregar()
        messagebox.showinfo("Sucesso", "Paciente atualizado!")

    def deletar(self):
        if not self._id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente na lista.")
            return
        if not messagebox.askyesno("Confirmar", "Deletar paciente e seus agendamentos?"):
            return
        ctrl.deletar_paciente(self._id_selecionado)
        self.limpar()
        self.carregar()

    def limpar(self):
        self._id_selecionado = None
        self.entry_nome.delete(0, "end")
        self.entry_telefone.delete(0, "end")

    def _selecionar(self, _event):
        selecionado = self.tree.selection()
        if not selecionado:
            return
        valores = self.tree.item(selecionado[0])["values"]
        self._id_selecionado = valores[0]
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, valores[1])
        self.entry_telefone.delete(0, "end")
        self.entry_telefone.insert(0, valores[2])


# ==============================================================
#  ABA MÉDICOS
# ==============================================================

class AbaMedicos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f4f8")
        self._id_selecionado = None
        self._build()
        self.carregar()

    def _build(self):
        frame_form = tk.LabelFrame(
            self, text="Dados do Médico", bg="#f0f4f8", font=("Arial", 10, "bold")
        )
        frame_form.pack(fill="x", padx=10, pady=8)
        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        self.entry_nome         = _campo(frame_form, "Nome:",          0, 0)
        self.entry_especialidade = _campo(frame_form, "Especialidade:", 0, 2)

        frame_btn = tk.Frame(self, bg="#f0f4f8")
        frame_btn.pack(fill="x", padx=10)

        tk.Button(frame_btn, text="Cadastrar",  bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), command=self.cadastrar).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Atualizar",  bg="#2980b9", fg="white",
                  font=("Arial", 10, "bold"), command=self.atualizar).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Deletar",   bg="#e74c3c", fg="white",
                  font=("Arial", 10, "bold"), command=self.deletar).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Limpar",    bg="#95a5a6", fg="white",
                  font=("Arial", 10, "bold"), command=self.limpar).pack(side="left", padx=4)

        self.tree = _criar_treeview(self, [
            ("id",            "ID",            50),
            ("nome",          "Nome",         250),
            ("especialidade", "Especialidade",200),
        ])
        self.tree.bind("<<TreeviewSelect>>", self._selecionar)

    def carregar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for m in ctrl.listar_medicos():
            self.tree.insert("", "end", values=(m.id, m.nome, m.especialidade))

    def cadastrar(self):
        nome          = self.entry_nome.get().strip()
        especialidade = self.entry_especialidade.get().strip()
        if not nome or not especialidade:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        ctrl.cadastrar_medico(nome, especialidade)
        self.limpar()
        self.carregar()
        messagebox.showinfo("Sucesso", "Médico cadastrado com sucesso!")

    def atualizar(self):
        if not self._id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um médico na lista.")
            return
        nome          = self.entry_nome.get().strip()
        especialidade = self.entry_especialidade.get().strip()
        if not nome or not especialidade:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        ctrl.atualizar_medico(self._id_selecionado, nome, especialidade)
        self.limpar()
        self.carregar()
        messagebox.showinfo("Sucesso", "Médico atualizado!")

    def deletar(self):
        if not self._id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um médico na lista.")
            return
        if not messagebox.askyesno("Confirmar", "Deletar médico e seus agendamentos?"):
            return
        ctrl.deletar_medico(self._id_selecionado)
        self.limpar()
        self.carregar()

    def limpar(self):
        self._id_selecionado = None
        self.entry_nome.delete(0, "end")
        self.entry_especialidade.delete(0, "end")

    def _selecionar(self, _event):
        selecionado = self.tree.selection()
        if not selecionado:
            return
        valores = self.tree.item(selecionado[0])["values"]
        self._id_selecionado = valores[0]
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, valores[1])
        self.entry_especialidade.delete(0, "end")
        self.entry_especialidade.insert(0, valores[2])


# ==============================================================
#  ABA AGENDAMENTOS
# ==============================================================

class AbaAgendamentos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f4f8")
        self._pacientes = []
        self._medicos   = []
        self._build()
        self.carregar()

    def _build(self):
        frame_form = tk.LabelFrame(
            self, text="Novo Agendamento", bg="#f0f4f8", font=("Arial", 10, "bold")
        )
        frame_form.pack(fill="x", padx=10, pady=8)

        # Linha 0: Paciente + Médico
        tk.Label(frame_form, text="Paciente:", bg="#f0f4f8").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.combo_paciente = ttk.Combobox(frame_form, width=26, state="readonly")
        self.combo_paciente.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(frame_form, text="Médico:", bg="#f0f4f8").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.combo_medico = ttk.Combobox(frame_form, width=26, state="readonly")
        self.combo_medico.grid(row=0, column=3, sticky="ew", padx=5, pady=3)

        # Linha 1: Data + Hora
        self.entry_data = _campo(frame_form, "Data (AAAA-MM-DD):", 1, 0)
        self.entry_hora = _campo(frame_form, "Hora (HH:MM):",      1, 2)

        frame_btn = tk.Frame(self, bg="#f0f4f8")
        frame_btn.pack(fill="x", padx=10)
        tk.Button(frame_btn, text="Agendar",  bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), command=self.agendar).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Cancelar", bg="#e74c3c", fg="white",
                  font=("Arial", 10, "bold"), command=self.cancelar).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Atualizar Lista", bg="#7f8c8d", fg="white",
                  font=("Arial", 10, "bold"), command=self.carregar).pack(side="left", padx=4)

        self.tree = _criar_treeview(self, [
            ("id",          "ID",          40),
            ("data",        "Data",       100),
            ("hora",        "Hora",        70),
            ("paciente",    "Paciente",   180),
            ("medico",      "Médico",     180),
            ("especialidade","Especialidade",150),
        ])

    def _popular_combos(self):
        self._pacientes = ctrl.listar_pacientes()
        self._medicos   = ctrl.listar_medicos()
        self.combo_paciente["values"] = [f"{p.id} - {p.nome}" for p in self._pacientes]
        self.combo_medico["values"]   = [f"{m.id} - {m.nome} ({m.especialidade})" for m in self._medicos]

    def carregar(self):
        self._popular_combos()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in ctrl.listar_agendamentos():
            self.tree.insert("", "end", values=(
                a.id, a.data, a.hora,
                a.nome_paciente, a.nome_medico, a.especialidade
            ))

    def agendar(self):
        idx_p = self.combo_paciente.current()
        idx_m = self.combo_medico.current()
        data  = self.entry_data.get().strip()
        hora  = self.entry_hora.get().strip()

        if idx_p < 0 or idx_m < 0 or not data or not hora:
            messagebox.showwarning("Atenção", "Selecione paciente, médico, data e hora.")
            return

        ctrl.cadastrar_agendamento(
            self._pacientes[idx_p].id,
            self._medicos[idx_m].id,
            data, hora,
        )
        self.entry_data.delete(0, "end")
        self.entry_hora.delete(0, "end")
        self.combo_paciente.set("")
        self.combo_medico.set("")
        self.carregar()
        messagebox.showinfo("Sucesso", "Agendamento realizado!")

    def cancelar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um agendamento na lista.")
            return
        agendamento_id = self.tree.item(selecionado[0])["values"][0]
        if not messagebox.askyesno("Confirmar", "Cancelar este agendamento?"):
            return
        ctrl.deletar_agendamento(agendamento_id)
        self.carregar()


# ==============================================================
#  ABA RELATÓRIO (DIFERENCIAL)
# ==============================================================

class AbaRelatorio(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f4f8")
        self._build()

    def _build(self):
        frame_filtro = tk.LabelFrame(
            self, text="Filtro por Especialidade (Diferencial)",
            bg="#f0f4f8", font=("Arial", 10, "bold")
        )
        frame_filtro.pack(fill="x", padx=10, pady=8)

        tk.Label(frame_filtro, text="Especialidade:", bg="#f0f4f8").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.combo_esp = ttk.Combobox(frame_filtro, width=30, state="readonly")
        self.combo_esp.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Button(
            frame_filtro, text="Gerar Relatório",
            bg="#8e44ad", fg="white", font=("Arial", 10, "bold"),
            command=self.gerar
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            frame_filtro, text="Carregar Especialidades",
            bg="#7f8c8d", fg="white", font=("Arial", 9),
            command=self._carregar_especialidades
        ).grid(row=0, column=3, padx=4)

        self.lbl_total = tk.Label(self, text="", bg="#f0f4f8",
                                  font=("Arial", 10, "italic"), fg="#555")
        self.lbl_total.pack(pady=2)

        self.tree = _criar_treeview(self, [
            ("id",          "ID",          40),
            ("data",        "Data",       100),
            ("hora",        "Hora",        70),
            ("paciente",    "Paciente",   200),
            ("medico",      "Médico",     180),
            ("especialidade","Especialidade",150),
        ])

        self._carregar_especialidades()

    def _carregar_especialidades(self):
        especialidades = ctrl.listar_especialidades()
        self.combo_esp["values"] = especialidades
        if especialidades:
            self.combo_esp.current(0)

    def gerar(self):
        especialidade = self.combo_esp.get().strip()
        if not especialidade:
            messagebox.showwarning("Atenção", "Selecione uma especialidade.")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        resultados = ctrl.listar_agendamentos_por_especialidade(especialidade)
        for a in resultados:
            self.tree.insert("", "end", values=(
                a.id, a.data, a.hora,
                a.nome_paciente, a.nome_medico, a.especialidade
            ))

        self.lbl_total.config(
            text=f"Total encontrado: {len(resultados)} agendamento(s) para '{especialidade}'"
        )
