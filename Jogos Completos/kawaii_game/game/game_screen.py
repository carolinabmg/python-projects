"""
game_screen.py — Tela e lógica de uma partida ativa.

Responsabilidade única: montar o tabuleiro, controlar a partida
e acionar os callbacks do app ao terminar.
"""

import tkinter as tk
from tkinter import messagebox
import random
import time

from .constants import (
    BG, LILAC, MINT, PEACH, YELLOW, BLUE, PINK, CORAL,
    DARK_TEXT, VIOLET, DEEP_RED,
    CORES_BOTOES,
    Dificuldade, GRADE_DIFICULDADE, TEMAS,
    XP_ACERTO, XP_STREAK, STREAK_TRIGGER,
    MOEDAS_POR_DIFICULDADE, MOEDAS_STREAK_BONUS,
    FALAS_ACERTO, FALAS_STREAK, FALAS_ERRO,
)
from .models import Carta
from . import sound
from . import widgets as W


class GameScreen:
    """
    Gerencia uma partida completa.

    Parâmetros
    ----------
    app          : instância de KawaiiMemoryApp (dono da janela)
    estado_salvo : dict carregado do arquivo de save (ou None para nova partida)
    """

    def __init__(self, app, estado_salvo: dict | None = None):
        self.app    = app
        self.root   = app.root
        self.jog    = app.jogadora

        self.primeira: Carta | None = None
        self.segunda:  Carta | None = None
        self.streak     = 0
        self.start_time = None
        self.tempo_acumulado = 0

        self._preparar_estado(estado_salvo)
        self._montar_ui()

        if estado_salvo is None:
            self._show_cards_memory()
        else:
            self._restaurar_tabuleiro()

    # ── preparar estado ──────────────────────────────────────
    def _preparar_estado(self, estado_salvo: dict | None):
        if estado_salvo is None:
            self.jog.stats["games_played"] += 1
            self.app.gerenciador.salvar_jogadora(self.jog)

            diff          = self.app._dificuldade_atual()
            rows, cols    = GRADE_DIFICULDADE[diff]
            pairs         = (rows * cols) // 2
            tema          = self.app.tema_atual.get()
            icons         = TEMAS[tema][:pairs]
            valores       = icons * 2
            random.shuffle(valores)

            self.cartas   = [Carta(i, v) for i, v in enumerate(valores)]
            self.rows, self.cols, self.pairs = rows, cols, pairs
            self.tempo_acumulado = 0
            self.streak   = 0
        else:
            self.rows     = estado_salvo["linhas"]
            self.cols     = estado_salvo["colunas"]
            self.pairs    = estado_salvo["pares"]
            self.app.diff.set(estado_salvo["dificuldade"])
            self.app.tema_atual.set(estado_salvo.get("tema", "Kawaii 🎀"))
            combinadas    = set(estado_salvo["combinadas"])
            self.cartas   = [Carta(i, v) for i, v in enumerate(estado_salvo["valores"])]
            for c in self.cartas:
                if c.indice in combinadas:
                    c.marcar_combinada()
            self.tempo_acumulado = estado_salvo["tempo"]
            self.streak          = estado_salvo.get("streak", 0)

    # ── montar UI ────────────────────────────────────────────
    def _montar_ui(self):
        self.app.clear()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)
        self._main = main

        found_ini = sum(1 for c in self.cartas if c.combinada) // 2

        # status
        status = tk.Frame(main, bg=LILAC, relief="raised", bd=2)
        status.pack(padx=16, pady=8, fill="x")
        tk.Label(
            status,
            text=(f"👤 {self.jog.nome}  |  👑 Nível {self.jog.level}  |  "
                  f"📊 {self.app.diff.get()}  |  {self.app.tema_atual.get()}  |  "
                  f"💰 {self.jog.moedas}"),
            font=("Arial", 10, "bold"), bg=LILAC, fg="#4C0080",
        ).pack(side="left", padx=8, pady=6)

        self.lbl_timer = tk.Label(status, text="⏱️ 00:00",
                                  font=("Arial", 10, "bold"), bg=LILAC, fg=VIOLET)
        self.lbl_timer.pack(side="right", padx=8)

        self.lbl_pares = tk.Label(
            status, text=f"🎁 Pares: {found_ini}/{self.pairs}",
            font=("Arial", 10, "bold"), bg=LILAC, fg=DEEP_RED,
        )
        self.lbl_pares.pack(side="right", padx=8)

        # barra XP + streak
        xp_f = tk.Frame(main, bg=BG)
        xp_f.pack(fill="x", padx=16, pady=(0, 2))

        xp_atual = self.jog.xp_no_nivel_atual()
        xp_max   = self.jog.xp_para_proximo()
        pct      = xp_atual / xp_max
        self.xp_canvas = tk.Canvas(xp_f, width=480, height=16,
                                   bg="#E8D5F5", highlightthickness=1,
                                   highlightbackground=LILAC)
        self.xp_canvas.pack(side="left", padx=6)
        self._redesenhar_xp(xp_atual, xp_max, pct)

        self.lbl_streak = tk.Label(xp_f, text=f"🔥 Streak: {self.streak}",
                                   font=("Arial", 10, "bold"), bg=BG, fg=DEEP_RED)
        self.lbl_streak.pack(side="left", padx=10)

        # dica
        tk.Label(main, text="💡 Vire duas cartas e tente formar pares iguais!",
                 font=("Arial", 10, "italic"), bg=BG, fg=VIOLET).pack(pady=(3, 0))

        # mascote
        self.lbl_mascote = tk.Label(
            main, text="🦋 Cirilla: boa sorte! 💖",
            font=("Arial", 12, "bold"), bg=PEACH, fg=DARK_TEXT,
            relief="raised", bd=2, width=54,
        )
        self.lbl_mascote.pack(pady=(4, 5), ipady=3)

        # tabuleiro
        board = tk.Frame(main, bg=BG)
        board.pack(padx=14, pady=4)
        total    = self.rows * self.cols
        self.btns: list[tk.Button] = []
        for i in range(total):
            btn = tk.Button(
                board, text="", width=5, height=2,
                font=("Arial", 20, "bold"),
                bg=CORES_BOTOES[i % len(CORES_BOTOES)],
                activebackground="#FFFFFF", relief="raised", bd=2,
                command=lambda x=i: self.flip(x),
            )
            btn.grid(row=i // self.cols, column=i % self.cols, padx=5, pady=5)
            self.btns.append(btn)

        # controles
        ctrl = tk.Frame(main, bg=BG)
        ctrl.pack(pady=8)
        for texto, cor, cmd in [
            ("🔙 Voltar",        BLUE,  self.app.voltar_da_partida),
            ("🔄 Novo Jogo",     PINK,  self.app.reiniciar_partida),
            ("💾 Salvar e Sair", MINT,  self._salvar_e_sair),
            ("🚪 Sair",          CORAL, self.app.sair_do_jogo),
        ]:
            tk.Button(ctrl, text=texto, font=("Arial", 10, "bold"),
                      bg=cor, width=14, command=cmd).pack(side="left", padx=5)

    # ── memorização ──────────────────────────────────────────
    def _show_cards_memory(self):
        for i, carta in enumerate(self.cartas):
            self.btns[i].config(text=carta.valor, state="disabled")
        self._segundos_memo = 5
        self._contar_memo()

    def _contar_memo(self):
        if not self.lbl_mascote.winfo_exists():
            return
        if self._segundos_memo > 0:
            self.lbl_mascote.config(
                text=f"🧠 Memorize! Escondendo em {self._segundos_memo}…", bg=YELLOW)
            self._segundos_memo -= 1
            self.root.after(1000, self._contar_memo)
        else:
            self.lbl_mascote.config(text="🎮 Valendo! Encontre os pares! 💪", bg=PEACH)
            self._iniciar_jogo()

    def _iniciar_jogo(self):
        for i, btn in enumerate(self.btns):
            if not self.cartas[i].combinada:
                btn.config(text="", state="normal")
        self.start_time = time.time()
        self._update_timer()

    # ── restaurar jogo salvo ──────────────────────────────
    def _restaurar_tabuleiro(self):
        for carta in self.cartas:
            if carta.combinada:
                self.btns[carta.indice].config(
                    text=carta.valor, state="disabled", bg="#FDE2E4")
        self.lbl_mascote.config(text="🦋 Cirilla: bem-vinda de volta! 🌙", bg=PEACH)
        self.start_time = time.time()
        self._update_timer()

    # ── cronômetro ───────────────────────────────────────
    def _update_timer(self):
        if not self.lbl_timer.winfo_exists():
            return
        combinados = sum(1 for c in self.cartas if c.combinada)
        if self.start_time and combinados < self.pairs * 2:
            elapsed = self.tempo_acumulado + int(time.time() - self.start_time)
            self.lbl_timer.config(text=f"⏱️ {elapsed//60:02d}:{elapsed%60:02d}")
            self.root.after(1000, self._update_timer)

    # ── animação de virar carta ───────────────────────────
    def _animar_carta(self, idx: int, valor: str):
        btn = self.btns[idx]
        flashes = ["#FFFFFF", "#FFE0F0", "#FFB6C1"]

        def passo(n):
            if n < len(flashes):
                btn.config(bg=flashes[n])
                self.root.after(50, lambda: passo(n + 1))
            else:
                btn.config(text=valor)

        passo(0)

    # ── flip ─────────────────────────────────────────────
    def flip(self, i: int):
        carta = self.cartas[i]
        if carta.combinada or carta.virada:
            return
        if self.primeira and self.segunda:
            return
        carta.virar()
        self._animar_carta(i, carta.valor)

        if self.primeira is None:
            self.primeira = carta
        else:
            self.segunda = carta
            for btn in self.btns:
                btn.config(state="disabled")
            self.root.after(700, self._check_match)

    # ── conferir par ─────────────────────────────────────
    def _check_match(self):
        a, b = self.primeira, self.segunda

        if a.valor == b.valor:
            a.marcar_combinada()
            b.marcar_combinada()
            self.btns[a.indice].config(state="disabled", bg="#FDE2E4")
            self.btns[b.indice].config(state="disabled", bg="#FDE2E4")

            self.streak += 1
            self.lbl_streak.config(text=f"🔥 Streak: {self.streak}")

            if self.streak % STREAK_TRIGGER == 0:
                self.lbl_mascote.config(
                    text=f"🦋 Cirilla: {random.choice(FALAS_STREAK)}", bg=YELLOW)
                self._dar_xp(XP_STREAK)
                self.jog.ganhar_moedas(MOEDAS_STREAK_BONUS)
                sound.streak()
                self.app._desbloquear("Streak Master 🔥🔥🔥")
            else:
                self.lbl_mascote.config(
                    text=f"🦋 Cirilla: {random.choice(FALAS_ACERTO)}", bg=MINT)
                sound.acerto()

            self._dar_xp(XP_ACERTO)
            self._redesenhar_xp_atual()

        else:
            self.btns[a.indice].config(text="", bg=CORES_BOTOES[a.indice % len(CORES_BOTOES)])
            self.btns[b.indice].config(text="", bg=CORES_BOTOES[b.indice % len(CORES_BOTOES)])
            a.esconder()
            b.esconder()
            self.lbl_mascote.config(
                text=f"🦋 Cirilla: {random.choice(FALAS_ERRO)}", bg=PEACH)
            sound.erro()
            self.streak = 0
            self.lbl_streak.config(text=f"🔥 Streak: {self.streak}")

        self.primeira = None
        self.segunda  = None

        for carta in self.cartas:
            if not carta.combinada:
                self.btns[carta.indice].config(state="normal")

        combinados = sum(1 for c in self.cartas if c.combinada)
        self.lbl_pares.config(text=f"🎁 Pares: {combinados//2}/{self.pairs}")

        if combinados == self.pairs * 2:
            self._vitoria()

    # ── helpers XP ───────────────────────────────────────
    def _dar_xp(self, qtd: int):
        subiu = self.jog.ganhar_xp(qtd)
        self.app.gerenciador.salvar_jogadora(self.jog)
        if subiu:
            messagebox.showinfo(
                "✨ LEVEL UP!",
                f"Parabéns, {self.jog.nome}!\n"
                f"Você chegou ao nível {self.jog.level}!\n"
                f"Agora você é: {self.jog.titulo()} 🎉",
            )

    def _redesenhar_xp_atual(self):
        if not self.xp_canvas.winfo_exists():
            return
        xp_atual = self.jog.xp_no_nivel_atual()
        xp_max   = self.jog.xp_para_proximo()
        self._redesenhar_xp(xp_atual, xp_max, xp_atual / xp_max)

    def _redesenhar_xp(self, xp_atual: int, xp_max: int, pct: float):
        self.xp_canvas.delete("all")
        self.xp_canvas.create_rectangle(0, 0, int(480 * pct), 16, fill=LILAC, outline="")
        self.xp_canvas.create_text(
            240, 8,
            text=f"XP Nível {self.jog.level}: {xp_atual}/{xp_max}",
            font=("Arial", 9, "bold"), fill="#2D3142",
        )

    # ── salvar ───────────────────────────────────────────
    def _salvar_e_sair(self):
        elapsed = (self.tempo_acumulado + int(time.time() - self.start_time)
                   if self.start_time else self.tempo_acumulado)
        estado = {
            "valores":     [c.valor for c in self.cartas],
            "combinadas":  [c.indice for c in self.cartas if c.combinada],
            "linhas":      self.rows,
            "colunas":     self.cols,
            "pares":       self.pairs,
            "dificuldade": self.app.diff.get(),
            "tema":        self.app.tema_atual.get(),
            "nome":        self.jog.nome,
            "tempo":       elapsed,
            "streak":      self.streak,
        }
        from .file_manager import FileManager
        from .constants import SAVE_GAME_FILE
        FileManager.gravar(SAVE_GAME_FILE, estado)
        self.start_time = None
        messagebox.showinfo("💾 Jogo salvo!",
                            "Partida guardada! ✨\nClique em '▶️ Continuar' quando voltar. 🌸")
        self.app.home()

    # ── vitória ──────────────────────────────────────────
    def _vitoria(self):
        elapsed     = self.tempo_acumulado + int(time.time() - self.start_time)
        self.start_time = None

        self.jog.stats["games_won"]  += 1
        self.jog.stats["total_time"] += elapsed
        if self.jog.stats["best_time"] is None or elapsed < self.jog.stats["best_time"]:
            self.jog.stats["best_time"] = elapsed

        diff_str = self.app.diff.get()
        self.jog.registrar_partida(elapsed, diff_str, vitoria=True)

        # moedas
        moedas_ganhas = MOEDAS_POR_DIFICULDADE.get(diff_str, 10)
        self.jog.ganhar_moedas(moedas_ganhas)

        self.app.gerenciador.salvar_jogadora(self.jog)

        # XP vitória
        self._dar_xp(50)

        # conquistas
        self.app._desbloquear("Primeira Vitória 🏆")
        if elapsed <= 60:
            self.app._desbloquear("Velocista ⚡")
        if self.app._dificuldade_atual() == Dificuldade.DIFICIL:
            self.app._desbloquear("Mestre da Memória 🧙‍♀️")
        if self.jog.stats["games_won"] == 10:
            self.app._desbloquear("10 Vitórias 🎉")
        if self.jog.level >= 10:
            self.app._desbloquear("Nivel 10 👑")
        if self.jog.moedas >= 1000:
            self.app._desbloquear("Milionária 💰")

        from .file_manager import FileManager
        from .constants import SAVE_GAME_FILE
        FileManager.apagar(SAVE_GAME_FILE)
        self.app.ranking.adicionar(
            self.jog.nome, self.jog.xp, elapsed, self.jog.level)

        sound.vitoria()
        messagebox.showinfo(
            "🎉 VITÓRIA!",
            f"PARABÉNS! 🎉\n\n"
            f"👤 {self.jog.nome}\n"
            f"👑 {self.jog.titulo()}\n"
            f"⏱️ Tempo: {elapsed}s\n"
            f"💰 +{moedas_ganhas} moedas!\n"
            f"⭐ Nível: {self.jog.level}\n"
            f"💜 XP Total: {self.jog.xp}\n\n"
            f"Você é incrível! ✨",
        )
        self.app.home()
