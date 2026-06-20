#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 AGENDA KAWAII (GUI) 🌸
Agenda gráfica em Tkinter com visões diária, mensal e anual,
além de um Pomodoro integrado, no estilo pastel do Memory Game Deluxe.
"""

import calendar
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime, timedelta

try:
    import winsound
    SOM_DISPONIVEL = True
except ImportError:
    SOM_DISPONIVEL = False

# Paleta kawaii (mesma do Memory Game Deluxe)
BG = "#FFF0F6"
PINK = "#FFB6C1"
LILAC = "#D8B4FE"
BLUE = "#BDE0FE"
MINT = "#C7F9CC"
PEACH = "#FFD6A5"
YELLOW = "#FDFFB6"
PURPLE = "#E0C3FC"
CORAL = "#FFB3BA"
LIGHT_PINK = "#FFF5F8"
TITLE_COLOR = "#A4133C"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ARQUIVO_EVENTOS = os.path.join(DATA_DIR, "eventos.json")
ARQUIVO_POMODORO_LOG = os.path.join(DATA_DIR, "pomodoro_log.json")

CATEGORIAS = {
    'trabalho': ('💼', PEACH),
    'estudo': ('📚', BLUE),
    'saude': ('💪', MINT),
    'lazer': ('🎮', LILAC),
    'compras': ('🛍️', YELLOW),
    'comida': ('🍜', CORAL),
    'amigos': ('👯', PURPLE),
    'casa': ('🏠', PINK),
    'outro': ('⭐', LIGHT_PINK),
}

MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
DIAS_SEMANA_ABREV = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
DIAS_SEMANA_COMPLETO = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
                         "Sexta-feira", "Sábado", "Domingo"]

POMO_FOCO_PADRAO = 25
POMO_PAUSA_CURTA_PADRAO = 5
POMO_PAUSA_LONGA_PADRAO = 15
POMO_CICLOS_PARA_PAUSA_LONGA = 4
POMO_CORES_FASE = {'foco': CORAL, 'pausa_curta': MINT, 'pausa_longa': LILAC}
POMO_TEXTOS_FASE = {'foco': '🍅 Foco', 'pausa_curta': '☕ Pausa curta', 'pausa_longa': '🌸 Pausa longa'}


class AgendaKawaiiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Agenda Kawaii 🌸")
        self.root.geometry("860x700")
        self.root.configure(bg=BG)
        self.root.minsize(760, 600)
        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        os.makedirs(DATA_DIR, exist_ok=True)
        self.eventos = self.carregar_eventos()

        self.data_selecionada = date.today()
        self.ano_mes_exibido = [date.today().year, date.today().month]
        self.ano_exibido = date.today().year

        self.pomo_rodando = False
        self.pomo_pausado = False
        self.pomo_fase = None
        self.pomo_ciclo = 0
        self.pomo_segundos_restantes = 0
        self.pomo_after_id = None
        self.pomo_foco_min = POMO_FOCO_PADRAO
        self.pomo_pausa_curta_min = POMO_PAUSA_CURTA_PADRAO
        self.pomo_pausa_longa_min = POMO_PAUSA_LONGA_PADRAO

        self._construir_header()
        self._construir_abas()

        self.atualizar_dia()
        self.atualizar_mes()
        self.atualizar_ano()
        self._pomo_atualizar_stats()

    # ---------- Persistência de eventos ----------
    def carregar_eventos(self):
        if os.path.exists(ARQUIVO_EVENTOS):
            try:
                with open(ARQUIVO_EVENTOS, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def salvar_eventos(self):
        with open(ARQUIVO_EVENTOS, 'w', encoding='utf-8') as f:
            json.dump(self.eventos, f, ensure_ascii=False, indent=2)

    def _atualizar_todas_visoes(self):
        self.atualizar_dia()
        self.atualizar_mes()
        self.atualizar_ano()

    # ---------- Layout geral ----------
    def _construir_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", pady=(14, 4))
        tk.Label(
            header, text="🌸✨ Agenda Kawaii ✨🌸",
            font=("Comic Sans MS", 22, "bold"), bg=BG, fg=TITLE_COLOR
        ).pack()

    def _construir_abas(self):
        style = ttk.Style()
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=(12, 8))

        self.abas = ttk.Notebook(self.root)
        self.abas.pack(fill="both", expand=True, padx=14, pady=10)

        self.aba_dia = tk.Frame(self.abas, bg=BG)
        self.aba_mes = tk.Frame(self.abas, bg=BG)
        self.aba_ano = tk.Frame(self.abas, bg=BG)
        self.aba_adicionar = tk.Frame(self.abas, bg=BG)
        self.aba_pomodoro = tk.Frame(self.abas, bg=BG)

        self.abas.add(self.aba_dia, text="📅 Dia")
        self.abas.add(self.aba_mes, text="🗓️ Mês")
        self.abas.add(self.aba_ano, text="📆 Ano")
        self.abas.add(self.aba_adicionar, text="➕ Adicionar")
        self.abas.add(self.aba_pomodoro, text="🍅 Pomodoro")

        self._construir_aba_dia()
        self._construir_aba_mes()
        self._construir_aba_ano()
        self._construir_aba_adicionar()
        self._construir_aba_pomodoro()

    @staticmethod
    def _bind_clique(widget, callback):
        widget.bind("<Button-1>", callback)
        for filho in widget.winfo_children():
            AgendaKawaiiGUI._bind_clique(filho, callback)

    # ---------- Aba: Dia ----------
    def _construir_aba_dia(self):
        nav = tk.Frame(self.aba_dia, bg=BG)
        nav.pack(fill="x", pady=(12, 4))

        tk.Button(nav, text="◀", command=lambda: self._mudar_dia(-1),
                  font=("Arial", 12, "bold"), bg=BLUE, fg="white", width=3).pack(side="left", padx=6)
        self.label_dia = tk.Label(nav, text="", font=("Arial", 14, "bold"), bg=BG, fg=TITLE_COLOR)
        self.label_dia.pack(side="left", expand=True)
        tk.Button(nav, text="▶", command=lambda: self._mudar_dia(1),
                  font=("Arial", 12, "bold"), bg=BLUE, fg="white", width=3).pack(side="right", padx=6)
        tk.Button(nav, text="Hoje", command=self._ir_hoje_dia,
                  font=("Arial", 10, "bold"), bg=MINT, fg="white").pack(side="right", padx=6)

        self.frame_dia_eventos = tk.Frame(self.aba_dia, bg=BG)
        self.frame_dia_eventos.pack(fill="both", expand=True, padx=12, pady=8)

        tk.Button(
            self.aba_dia, text="➕ Adicionar evento neste dia", command=self.ir_adicionar_neste_dia,
            font=("Arial", 11, "bold"), bg=PINK, fg="white", relief="raised", bd=2
        ).pack(pady=(0, 12))

    def _mudar_dia(self, delta):
        self.data_selecionada += timedelta(days=delta)
        self.atualizar_dia()

    def _ir_hoje_dia(self):
        self.data_selecionada = date.today()
        self.atualizar_dia()

    def atualizar_dia(self):
        for widget in self.frame_dia_eventos.winfo_children():
            widget.destroy()

        d = self.data_selecionada
        self.label_dia.config(
            text=f"{DIAS_SEMANA_COMPLETO[d.weekday()]}, {d.day:02d} de {MESES[d.month - 1]} de {d.year}"
        )

        data_str = d.strftime("%Y-%m-%d")
        eventos_dia = sorted(
            ((chave, ev) for chave, ev in self.eventos.items() if ev['data'] == data_str),
            key=lambda item: item[1].get('hora') or ""
        )

        if not eventos_dia:
            tk.Label(
                self.frame_dia_eventos, text="✨ Dia livre! Nenhum evento marcado.",
                font=("Arial", 11, "italic"), bg=BG, fg="#7B2CBF"
            ).pack(pady=24)
            return

        for chave, evento in eventos_dia:
            emoji, cor = CATEGORIAS.get(evento['categoria'], CATEGORIAS['outro'])
            linha = tk.Frame(self.frame_dia_eventos, bg=cor, relief="raised", bd=2)
            linha.pack(fill="x", pady=4, padx=4)

            tk.Label(
                linha, text=evento.get('hora') or "--:--", font=("Arial", 11, "bold"),
                bg=cor, fg="#7B2CBF", width=7
            ).pack(side="left", padx=(8, 4), pady=8)

            texto_frame = tk.Frame(linha, bg=cor)
            texto_frame.pack(side="left", fill="x", expand=True, pady=8)
            tk.Label(
                texto_frame, text=f"{emoji} {evento['titulo']}", font=("Arial", 11, "bold"),
                bg=cor, fg="#2D3142", anchor="w"
            ).pack(fill="x")
            if evento.get('descricao'):
                tk.Label(
                    texto_frame, text=evento['descricao'], font=("Arial", 9, "italic"),
                    bg=cor, fg="#2D3142", anchor="w", wraplength=440, justify="left"
                ).pack(fill="x")

            tk.Button(
                linha, text="🗑️", command=lambda c=chave: self.deletar_evento(c),
                font=("Arial", 10, "bold"), bg=CORAL, fg="white", relief="raised", bd=1
            ).pack(side="right", padx=8)

    def ir_adicionar_neste_dia(self):
        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, self.data_selecionada.strftime("%Y-%m-%d"))
        self.abas.select(self.aba_adicionar)

    def deletar_evento(self, chave):
        evento = self.eventos.get(chave)
        if not evento:
            return
        if messagebox.askyesno("Confirmar", f"Deletar o evento '{evento['titulo']}'? 🗑️"):
            del self.eventos[chave]
            self.salvar_eventos()
            self._atualizar_todas_visoes()

    # ---------- Aba: Mês ----------
    def _construir_aba_mes(self):
        nav = tk.Frame(self.aba_mes, bg=BG)
        nav.pack(fill="x", pady=(12, 4))

        tk.Button(nav, text="◀", command=lambda: self._mudar_mes(-1),
                  font=("Arial", 12, "bold"), bg=BLUE, fg="white", width=3).pack(side="left", padx=6)
        self.label_mes = tk.Label(nav, text="", font=("Arial", 14, "bold"), bg=BG, fg=TITLE_COLOR)
        self.label_mes.pack(side="left", expand=True)
        tk.Button(nav, text="▶", command=lambda: self._mudar_mes(1),
                  font=("Arial", 12, "bold"), bg=BLUE, fg="white", width=3).pack(side="right", padx=6)
        tk.Button(nav, text="Hoje", command=self._ir_hoje_mes,
                  font=("Arial", 10, "bold"), bg=MINT, fg="white").pack(side="right", padx=6)

        cabecalho = tk.Frame(self.aba_mes, bg=BG)
        cabecalho.pack(fill="x", padx=12)
        for i, nome in enumerate(DIAS_SEMANA_ABREV):
            tk.Label(cabecalho, text=nome, font=("Arial", 10, "bold"), bg=BG, fg=TITLE_COLOR).grid(
                row=0, column=i, sticky="nsew"
            )
            cabecalho.columnconfigure(i, weight=1)

        self.frame_mes_grid = tk.Frame(self.aba_mes, bg=BG)
        self.frame_mes_grid.pack(fill="both", expand=True, padx=12, pady=(2, 12))

    def _mudar_mes(self, delta):
        ano, mes = self.ano_mes_exibido
        mes += delta
        if mes < 1:
            mes, ano = 12, ano - 1
        elif mes > 12:
            mes, ano = 1, ano + 1
        self.ano_mes_exibido = [ano, mes]
        self.atualizar_mes()

    def _ir_hoje_mes(self):
        hoje = date.today()
        self.ano_mes_exibido = [hoje.year, hoje.month]
        self.atualizar_mes()

    def atualizar_mes(self):
        for widget in self.frame_mes_grid.winfo_children():
            widget.destroy()

        ano, mes = self.ano_mes_exibido
        self.label_mes.config(text=f"{MESES[mes - 1]} {ano}")

        contagem = {}
        for evento in self.eventos.values():
            contagem[evento['data']] = contagem.get(evento['data'], 0) + 1

        hoje = date.today()
        semanas = calendar.Calendar(firstweekday=0).monthdayscalendar(ano, mes)

        for linha_idx, semana in enumerate(semanas):
            for coluna_idx, dia in enumerate(semana):
                if dia == 0:
                    celula = tk.Frame(self.frame_mes_grid, bg=BG)
                else:
                    data_str = f"{ano}-{mes:02d}-{dia:02d}"
                    qtd = contagem.get(data_str, 0)
                    eh_hoje = (ano, mes, dia) == (hoje.year, hoje.month, hoje.day)
                    cor = PEACH if eh_hoje else (MINT if qtd else LIGHT_PINK)

                    celula = tk.Frame(self.frame_mes_grid, bg=cor, relief="raised", bd=1, cursor="hand2")
                    tk.Label(celula, text=str(dia), font=("Arial", 10, "bold"), bg=cor, fg="#7B2CBF").pack(
                        pady=(4, 0)
                    )
                    tk.Label(
                        celula, text=(f"🌸{qtd}" if qtd else " "), font=("Arial", 8), bg=cor, fg="#2D3142"
                    ).pack(pady=(0, 4))
                    self._bind_clique(celula, lambda _e, a=ano, m=mes, dd=dia: self.selecionar_dia_do_mes(a, m, dd))

                celula.grid(row=linha_idx, column=coluna_idx, sticky="nsew", padx=2, pady=2)

        for c in range(7):
            self.frame_mes_grid.columnconfigure(c, weight=1)
        for r in range(len(semanas)):
            self.frame_mes_grid.rowconfigure(r, weight=1)

    def selecionar_dia_do_mes(self, ano, mes, dia):
        self.data_selecionada = date(ano, mes, dia)
        self.atualizar_dia()
        self.abas.select(self.aba_dia)

    # ---------- Aba: Ano ----------
    def _construir_aba_ano(self):
        nav = tk.Frame(self.aba_ano, bg=BG)
        nav.pack(fill="x", pady=(12, 4))

        tk.Button(nav, text="◀", command=lambda: self._mudar_ano(-1),
                  font=("Arial", 12, "bold"), bg=BLUE, fg="white", width=3).pack(side="left", padx=6)
        self.label_ano = tk.Label(nav, text="", font=("Arial", 14, "bold"), bg=BG, fg=TITLE_COLOR)
        self.label_ano.pack(side="left", expand=True)
        tk.Button(nav, text="▶", command=lambda: self._mudar_ano(1),
                  font=("Arial", 12, "bold"), bg=BLUE, fg="white", width=3).pack(side="right", padx=6)
        tk.Button(nav, text="Hoje", command=self._ir_hoje_ano,
                  font=("Arial", 10, "bold"), bg=MINT, fg="white").pack(side="right", padx=6)

        self.frame_ano_grid = tk.Frame(self.aba_ano, bg=BG)
        self.frame_ano_grid.pack(fill="both", expand=True, padx=12, pady=(2, 12))

    def _mudar_ano(self, delta):
        self.ano_exibido += delta
        self.atualizar_ano()

    def _ir_hoje_ano(self):
        self.ano_exibido = date.today().year
        self.atualizar_ano()

    def atualizar_ano(self):
        for widget in self.frame_ano_grid.winfo_children():
            widget.destroy()

        self.label_ano.config(text=str(self.ano_exibido))

        contagens = [0] * 13
        for evento in self.eventos.values():
            partes = evento['data'].split('-')
            if len(partes) == 3 and partes[0].isdigit() and int(partes[0]) == self.ano_exibido:
                contagens[int(partes[1])] += 1

        hoje = date.today()
        for indice in range(12):
            mes_num = indice + 1
            linha, coluna = divmod(indice, 3)
            eh_mes_atual = self.ano_exibido == hoje.year and mes_num == hoje.month
            cor = PEACH if eh_mes_atual else (MINT if contagens[mes_num] else LIGHT_PINK)

            celula = tk.Frame(self.frame_ano_grid, bg=cor, relief="raised", bd=2, cursor="hand2")
            celula.grid(row=linha, column=coluna, sticky="nsew", padx=6, pady=6)
            tk.Label(celula, text=MESES[indice], font=("Arial", 12, "bold"), bg=cor, fg="#7B2CBF").pack(
                pady=(10, 2)
            )
            texto = f"🌸 {contagens[mes_num]} evento(s)" if contagens[mes_num] else "✨ livre"
            tk.Label(celula, text=texto, font=("Arial", 10), bg=cor, fg="#2D3142").pack(pady=(0, 10))
            self._bind_clique(celula, lambda _e, m=mes_num: self.selecionar_mes_do_ano(m))

        for c in range(3):
            self.frame_ano_grid.columnconfigure(c, weight=1)
        for r in range(4):
            self.frame_ano_grid.rowconfigure(r, weight=1)

    def selecionar_mes_do_ano(self, mes):
        self.ano_mes_exibido = [self.ano_exibido, mes]
        self.atualizar_mes()
        self.abas.select(self.aba_mes)

    # ---------- Aba: Adicionar ----------
    def _construir_aba_adicionar(self):
        aba = self.aba_adicionar
        form = tk.Frame(aba, bg=BG)
        form.pack(pady=20)

        def campo(label_texto, linha):
            tk.Label(form, text=label_texto, font=("Arial", 11, "bold"), bg=BG, fg="#7B2CBF").grid(
                row=linha, column=0, sticky="e", padx=8, pady=8
            )
            entrada = tk.Entry(form, font=("Arial", 11), width=32)
            entrada.grid(row=linha, column=1, padx=8, pady=8)
            return entrada

        self.entry_data = campo("📅 Data (AAAA-MM-DD):", 0)
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_hora = campo("🕐 Hora (HH:MM) [opcional]:", 1)
        self.entry_titulo = campo("📝 Título:", 2)
        self.entry_descricao = campo("💬 Descrição [opcional]:", 3)

        tk.Label(form, text="🎯 Categoria:", font=("Arial", 11, "bold"), bg=BG, fg="#7B2CBF").grid(
            row=4, column=0, sticky="e", padx=8, pady=8
        )
        self.combo_categoria = ttk.Combobox(
            form, font=("Arial", 11), width=29, state="readonly",
            values=[f"{emoji} {nome}" for nome, (emoji, _) in CATEGORIAS.items()]
        )
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=4, column=1, padx=8, pady=8)

        tk.Button(
            aba, text="✅ Salvar evento", command=self.adicionar_evento,
            font=("Arial", 13, "bold"), bg=PINK, fg="white", relief="raised", bd=3
        ).pack(pady=16)

    def adicionar_evento(self):
        data = self.entry_data.get().strip()
        hora = self.entry_hora.get().strip()
        titulo = self.entry_titulo.get().strip()
        descricao = self.entry_descricao.get().strip()
        categoria_texto = self.combo_categoria.get()

        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Agenda Kawaii", "❌ Data inválida! Use o formato AAAA-MM-DD.")
            return

        if hora:
            try:
                datetime.strptime(hora, "%H:%M")
            except ValueError:
                messagebox.showerror("Agenda Kawaii", "❌ Hora inválida! Use o formato HH:MM.")
                return

        if not titulo:
            messagebox.showerror("Agenda Kawaii", "❌ O título é obrigatório!")
            return

        categoria = categoria_texto.split(" ", 1)[1] if categoria_texto else "outro"
        chave = f"{data}_{hora}_{titulo}" if hora else f"{data}_{titulo}"

        self.eventos[chave] = {
            'data': data,
            'hora': hora,
            'titulo': titulo,
            'descricao': descricao,
            'categoria': categoria,
            'criado_em': datetime.now().isoformat(),
        }
        self.salvar_eventos()

        emoji, _ = CATEGORIAS.get(categoria, CATEGORIAS['outro'])
        messagebox.showinfo("Agenda Kawaii", f"Evento adicionado com sucesso! {emoji}")

        self.entry_titulo.delete(0, "end")
        self.entry_descricao.delete(0, "end")
        self.entry_hora.delete(0, "end")

        self.data_selecionada = datetime.strptime(data, "%Y-%m-%d").date()
        self.ano_mes_exibido = [self.data_selecionada.year, self.data_selecionada.month]
        self.ano_exibido = self.data_selecionada.year
        self._atualizar_todas_visoes()

    # ---------- Aba: Pomodoro ----------
    def _construir_aba_pomodoro(self):
        aba = self.aba_pomodoro

        self.pomo_status_label = tk.Label(
            aba, text="🍅 Pronto para focar!", font=("Arial", 14, "bold"), bg=BG, fg="#7B2CBF"
        )
        self.pomo_status_label.pack(pady=(20, 4))

        self.pomo_timer_label = tk.Label(
            aba, text="--:--", font=("Comic Sans MS", 48, "bold"), bg=BG, fg=TITLE_COLOR
        )
        self.pomo_timer_label.pack(pady=8)

        self.pomo_ciclo_label = tk.Label(aba, text="Ciclo: 0", font=("Arial", 11), bg=BG, fg="#2D3142")
        self.pomo_ciclo_label.pack(pady=(0, 12))

        form = tk.Frame(aba, bg=BG)
        form.pack(pady=4)

        def campo_minutos(texto, linha, padrao):
            tk.Label(form, text=texto, font=("Arial", 10, "bold"), bg=BG, fg="#7B2CBF").grid(
                row=linha, column=0, sticky="e", padx=6, pady=4
            )
            entrada = tk.Entry(form, font=("Arial", 10), width=6, justify="center")
            entrada.insert(0, str(padrao))
            entrada.grid(row=linha, column=1, padx=6, pady=4)
            return entrada

        self.pomo_entry_foco = campo_minutos("⏱️ Foco (min):", 0, POMO_FOCO_PADRAO)
        self.pomo_entry_pausa_curta = campo_minutos("☕ Pausa curta (min):", 1, POMO_PAUSA_CURTA_PADRAO)
        self.pomo_entry_pausa_longa = campo_minutos("🌸 Pausa longa (min):", 2, POMO_PAUSA_LONGA_PADRAO)

        botoes = tk.Frame(aba, bg=BG)
        botoes.pack(pady=14)
        self.pomo_btn_iniciar = tk.Button(
            botoes, text="▶️ Iniciar", command=self._pomo_iniciar,
            font=("Arial", 12, "bold"), bg=PINK, fg="white", relief="raised", bd=2, width=12
        )
        self.pomo_btn_iniciar.pack(side="left", padx=6)
        self.pomo_btn_pausar = tk.Button(
            botoes, text="⏸️ Pausar", command=self._pomo_pausar_retomar,
            font=("Arial", 12, "bold"), bg=BLUE, fg="white", relief="raised", bd=2, width=12
        )
        self.pomo_btn_pausar.pack(side="left", padx=6)
        tk.Button(
            botoes, text="🔁 Reiniciar", command=self._pomo_reiniciar,
            font=("Arial", 12, "bold"), bg=LILAC, fg="white", relief="raised", bd=2, width=12
        ).pack(side="left", padx=6)

        self.pomo_stats_label = tk.Label(
            aba, text="", font=("Arial", 11), bg=BG, fg="#2D3142", justify="center"
        )
        self.pomo_stats_label.pack(pady=(16, 0))

    def _pomo_iniciar(self):
        if self.pomo_rodando:
            return
        try:
            self.pomo_foco_min = float(self.pomo_entry_foco.get())
            self.pomo_pausa_curta_min = float(self.pomo_entry_pausa_curta.get())
            self.pomo_pausa_longa_min = float(self.pomo_entry_pausa_longa.get())
        except ValueError:
            messagebox.showerror("Pomodoro Kawaii", "❌ Use números válidos para os minutos!")
            return

        self.pomo_rodando = True
        self.pomo_pausado = False
        self.pomo_ciclo = 0
        self.pomo_ciclo_label.config(text="Ciclo: 0")
        self._pomo_atualizar_estado_widgets()
        self._pomo_definir_fase('foco')
        self._pomo_tick()

    def _pomo_definir_fase(self, fase):
        self.pomo_fase = fase
        minutos = {
            'foco': self.pomo_foco_min,
            'pausa_curta': self.pomo_pausa_curta_min,
            'pausa_longa': self.pomo_pausa_longa_min,
        }[fase]
        self.pomo_segundos_restantes = int(minutos * 60)
        self.pomo_status_label.config(text=POMO_TEXTOS_FASE[fase], fg="#7B2CBF")
        self.pomo_timer_label.config(fg=TITLE_COLOR if fase == 'foco' else "#2D6A4F")

    def _pomo_tick(self):
        if not self.pomo_rodando or self.pomo_pausado:
            return

        mins, segs = divmod(max(self.pomo_segundos_restantes, 0), 60)
        self.pomo_timer_label.config(text=f"{mins:02d}:{segs:02d}")

        if self.pomo_segundos_restantes <= 0:
            self._pomo_fase_concluida()
            return

        self.pomo_segundos_restantes -= 1
        self.pomo_after_id = self.root.after(1000, self._pomo_tick)

    def _pomo_fase_concluida(self):
        self._pomo_tocar_som()

        if self.pomo_fase == 'foco':
            self.pomo_ciclo += 1
            self.pomo_ciclo_label.config(text=f"Ciclo: {self.pomo_ciclo}")
            self._pomo_registrar_log(self.pomo_foco_min)
            self._pomo_atualizar_stats()
            proxima_fase = (
                'pausa_longa' if self.pomo_ciclo % POMO_CICLOS_PARA_PAUSA_LONGA == 0 else 'pausa_curta'
            )
        else:
            proxima_fase = 'foco'

        self._pomo_definir_fase(proxima_fase)
        self.pomo_after_id = self.root.after(1000, self._pomo_tick)

    def _pomo_pausar_retomar(self):
        if not self.pomo_rodando:
            return
        self.pomo_pausado = not self.pomo_pausado
        self.pomo_btn_pausar.config(text="▶️ Retomar" if self.pomo_pausado else "⏸️ Pausar")
        if not self.pomo_pausado:
            self._pomo_tick()

    def _pomo_reiniciar(self):
        if self.pomo_after_id is not None:
            self.root.after_cancel(self.pomo_after_id)
            self.pomo_after_id = None
        self.pomo_rodando = False
        self.pomo_pausado = False
        self.pomo_ciclo = 0
        self.pomo_fase = None
        self.pomo_timer_label.config(text="--:--", fg=TITLE_COLOR)
        self.pomo_status_label.config(text="🍅 Pronto para focar!")
        self.pomo_ciclo_label.config(text="Ciclo: 0")
        self.pomo_btn_pausar.config(text="⏸️ Pausar")
        self._pomo_atualizar_estado_widgets()

    def _pomo_atualizar_estado_widgets(self):
        estado = "disabled" if self.pomo_rodando else "normal"
        self.pomo_entry_foco.config(state=estado)
        self.pomo_entry_pausa_curta.config(state=estado)
        self.pomo_entry_pausa_longa.config(state=estado)
        self.pomo_btn_iniciar.config(state="disabled" if self.pomo_rodando else "normal")

    @staticmethod
    def _pomo_tocar_som():
        if SOM_DISPONIVEL:
            try:
                winsound.Beep(880, 300)
                return
            except RuntimeError:
                pass
        print("\a", end="")

    @staticmethod
    def _pomo_carregar_log():
        if os.path.exists(ARQUIVO_POMODORO_LOG):
            try:
                with open(ARQUIVO_POMODORO_LOG, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    @staticmethod
    def _pomo_salvar_log(log):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(ARQUIVO_POMODORO_LOG, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

    def _pomo_registrar_log(self, minutos_foco):
        log = self._pomo_carregar_log()
        hoje = datetime.now().strftime("%Y-%m-%d")
        dia = log.setdefault(hoje, {"ciclos": 0, "minutos_foco": 0})
        dia["ciclos"] += 1
        dia["minutos_foco"] += minutos_foco
        self._pomo_salvar_log(log)

    def _pomo_atualizar_stats(self):
        log = self._pomo_carregar_log()
        hoje = datetime.now().strftime("%Y-%m-%d")
        dados_hoje = log.get(hoje, {"ciclos": 0, "minutos_foco": 0})
        total_ciclos = sum(d["ciclos"] for d in log.values())
        total_minutos = sum(d["minutos_foco"] for d in log.values())
        self.pomo_stats_label.config(
            text=(
                f"📊 Hoje: {dados_hoje['ciclos']} ciclo(s) | {dados_hoje['minutos_foco']:.0f} min de foco\n"
                f"🎯 Total: {total_ciclos} ciclo(s) | {total_minutos:.0f} min de foco"
            )
        )

    def _ao_fechar(self):
        if self.pomo_after_id is not None:
            self.root.after_cancel(self.pomo_after_id)
        self.root.destroy()


def main():
    root = tk.Tk()
    AgendaKawaiiGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
