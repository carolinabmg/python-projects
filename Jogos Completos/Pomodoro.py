"""
🌸 Pomodoro Kawaii 🌸
Um timer Pomodoro com interface gráfica, tema rosa pastel e estatísticas do dia.

Como rodar:
    python pomodoro_kawaii.py

Requisitos: apenas Python 3 (tkinter já vem incluso na maioria das instalações).
Se der "ModuleNotFoundError: tkinter" no Linux, instale com:
    sudo apt install python3-tk
"""

import os
import sys
import datetime
import tkinter as tk
from tkinter import font as tkfont

# ──────────────────────────────────────────────────────────────
# Configurações (mexa aqui se quiser tempos diferentes)
# ──────────────────────────────────────────────────────────────
FOCO_MIN = 25       # minutos de foco
PAUSA_MIN = 5       # minutos de pausa

# Paleta rosa pastel 🌸
CORES = {
    "fundo":     "#FFF0F5",  # lavender blush (fundo geral)
    "cartao":    "#FFE4EC",  # rosa um pouco mais saturado
    "acento":    "#FF8FB1",  # rosa principal (botões, destaques)
    "acento2":   "#FFC1CC",  # rosa claro (botão secundário)
    "texto":     "#6D5D6E",  # cinza-roxeado suave
    "texto_sec": "#A48BA6",  # texto secundário, mais clarinho
    "pausa":     "#9ED5C5",  # verdinho pastel pro modo pausa
}

# Caminho do arquivo de histórico (fica na mesma pasta do script)
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_HISTORICO = os.path.join(PASTA, "historico_pomodoro.txt")


class PomodoroKawaii:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Pomodoro Kawaii 🌸")
        self.root.configure(bg=CORES["fundo"])
        self.root.geometry("360x520")
        self.root.resizable(False, False)

        # Estado interno
        self.modo = "foco"          # "foco" ou "pausa"
        self.segundos = FOCO_MIN * 60
        self.rodando = False
        self.after_id = None        # id do agendamento do tkinter (pra cancelar)

        # Estatísticas do dia
        self.pomodoros_hoje = 0
        self.minutos_foco_hoje = 0
        self._carregar_stats()      # lê o histórico e conta os de hoje

        # Fontes
        self.f_titulo = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.f_timer = tkfont.Font(family="Consolas", size=52, weight="bold")
        self.f_normal = tkfont.Font(family="Segoe UI", size=11)
        self.f_pequena = tkfont.Font(family="Segoe UI", size=9)
        self.f_botao = tkfont.Font(family="Segoe UI", size=12, weight="bold")

        self._montar_interface()
        self._atualizar_display()
        self._atualizar_stats()

    # ──────────────────────────────────────────────────────────
    # Montagem da interface
    # ──────────────────────────────────────────────────────────
    def _montar_interface(self):
        # Cabeçalho
        tk.Label(
            self.root, text="🌸 Pomodoro Kawaii 🌸",
            font=self.f_titulo, bg=CORES["fundo"], fg=CORES["acento"]
        ).pack(pady=(22, 4))

        # Patente (sistema de conquistas, versão leve)
        self.lbl_patente = tk.Label(
            self.root, text="", font=self.f_normal,
            bg=CORES["fundo"], fg=CORES["texto_sec"]
        )
        self.lbl_patente.pack(pady=(0, 14))

        # Cartão central com o timer
        cartao = tk.Frame(self.root, bg=CORES["cartao"], bd=0)
        cartao.pack(padx=24, pady=4, fill="x")

        self.lbl_estado = tk.Label(
            cartao, text="📚 Foco", font=self.f_normal,
            bg=CORES["cartao"], fg=CORES["texto"]
        )
        self.lbl_estado.pack(pady=(18, 0))

        self.lbl_timer = tk.Label(
            cartao, text="25:00", font=self.f_timer,
            bg=CORES["cartao"], fg=CORES["acento"]
        )
        self.lbl_timer.pack(pady=(0, 18))

        # Botões
        botoes = tk.Frame(self.root, bg=CORES["fundo"])
        botoes.pack(pady=18)

        self.btn_iniciar = tk.Button(
            botoes, text="▶ Iniciar", font=self.f_botao,
            bg=CORES["acento"], fg="white", activebackground=CORES["acento2"],
            activeforeground="white", bd=0, padx=20, pady=8,
            cursor="hand2", command=self.alternar_play
        )
        self.btn_iniciar.grid(row=0, column=0, padx=6)

        self.btn_resetar = tk.Button(
            botoes, text="↺ Resetar", font=self.f_botao,
            bg=CORES["acento2"], fg=CORES["texto"], activebackground=CORES["cartao"],
            activeforeground=CORES["texto"], bd=0, padx=20, pady=8,
            cursor="hand2", command=self.resetar
        )
        self.btn_resetar.grid(row=0, column=1, padx=6)

        # Painel de estatísticas
        stats = tk.Frame(self.root, bg=CORES["fundo"])
        stats.pack(pady=(8, 0))

        tk.Label(
            stats, text="📊 Estatísticas de hoje", font=self.f_normal,
            bg=CORES["fundo"], fg=CORES["texto"]
        ).pack()

        self.lbl_pomodoros = tk.Label(
            stats, text="", font=self.f_normal,
            bg=CORES["fundo"], fg=CORES["texto_sec"]
        )
        self.lbl_pomodoros.pack(pady=(6, 0))

        self.lbl_foco_total = tk.Label(
            stats, text="", font=self.f_normal,
            bg=CORES["fundo"], fg=CORES["texto_sec"]
        )
        self.lbl_foco_total.pack()

        # Rodapé
        tk.Label(
            self.root, text="feito com 🩷 pela feiticeira do código",
            font=self.f_pequena, bg=CORES["fundo"], fg=CORES["texto_sec"]
        ).pack(side="bottom", pady=12)

    # ──────────────────────────────────────────────────────────
    # Lógica do timer
    #   Importante: em GUI NÃO se usa while + time.sleep(), porque
    #   isso trava a janela. Usamos root.after(), que agenda a
    #   próxima execução sem bloquear o loop de eventos do tkinter.
    # ──────────────────────────────────────────────────────────
    def alternar_play(self):
        if not self.rodando:
            self.rodando = True
            self.btn_iniciar.config(text="⏸ Pausar")
            self._tick()
        else:
            self.rodando = False
            self.btn_iniciar.config(text="▶ Continuar")
            if self.after_id:
                self.root.after_cancel(self.after_id)

    def _tick(self):
        if not self.rodando:
            return

        self._atualizar_display()

        if self.segundos <= 0:
            self._fim_de_sessao()
            return

        self.segundos -= 1
        self.after_id = self.root.after(1000, self._tick)

    def _fim_de_sessao(self):
        self.rodando = False
        self._tocar_som()

        if self.modo == "foco":
            # Concluiu um Pomodoro de foco!
            self.pomodoros_hoje += 1
            self.minutos_foco_hoje += FOCO_MIN
            self._salvar_historico()
            self._atualizar_stats()
            self._iniciar_modo("pausa")
        else:
            # Concluiu a pausa, volta pro foco
            self._iniciar_modo("foco")

        # Fluxo automático: já emenda a próxima sessão (como num Pomodoro de verdade)
        self.rodando = True
        self.btn_iniciar.config(text="⏸ Pausar")
        self._tick()

    def _iniciar_modo(self, modo):
        self.modo = modo
        if modo == "foco":
            self.segundos = FOCO_MIN * 60
            self.lbl_estado.config(text="📚 Foco")
            self.lbl_timer.config(fg=CORES["acento"])
        else:
            self.segundos = PAUSA_MIN * 60
            self.lbl_estado.config(text="☕ Pausa")
            self.lbl_timer.config(fg=CORES["pausa"])

    def resetar(self):
        self.rodando = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self._iniciar_modo("foco")
        self.btn_iniciar.config(text="▶ Iniciar")
        self._atualizar_display()

    # ──────────────────────────────────────────────────────────
    # Atualização visual
    # ──────────────────────────────────────────────────────────
    def _atualizar_display(self):
        minutos, seg = divmod(self.segundos, 60)
        self.lbl_timer.config(text=f"{minutos:02d}:{seg:02d}")

    def _atualizar_stats(self):
        self.lbl_pomodoros.config(text=f"🍓 Pomodoros concluídos: {self.pomodoros_hoje}")
        self.lbl_foco_total.config(text=f"⏱️ Foco total: {self.minutos_foco_hoje} min")
        self.lbl_patente.config(text=self._patente())

    def _patente(self):
        n = self.pomodoros_hoje
        if n >= 10:
            return "🏆 Arquimaga Python"
        if n >= 5:
            return "✨ Maga do Código"
        if n >= 1:
            return "🌱 Aprendiz"
        return "🌸 Pronta para começar"

    # ──────────────────────────────────────────────────────────
    # Som
    # ──────────────────────────────────────────────────────────
    def _tocar_som(self):
        try:
            if sys.platform.startswith("win"):
                import winsound
                winsound.Beep(880, 250)
                winsound.Beep(1100, 250)
            else:
                # bell() funciona em Mac/Linux usando o som do sistema
                self.root.bell()
        except Exception:
            try:
                self.root.bell()
            except Exception:
                pass  # se não rolar som, segue a vida sem travar

    # ──────────────────────────────────────────────────────────
    # Persistência (histórico em .txt)
    # ──────────────────────────────────────────────────────────
    def _salvar_historico(self):
        agora = datetime.datetime.now().isoformat(timespec="seconds")
        linha = f"{agora} - Pomodoro de foco concluído ({FOCO_MIN} min)\n"
        try:
            with open(ARQUIVO_HISTORICO, "a", encoding="utf-8") as f:
                f.write(linha)
        except Exception as e:
            print(f"Não consegui salvar o histórico: {e}")

    def _carregar_stats(self):
        """Lê o histórico e conta quantos Pomodoros foram feitos HOJE."""
        hoje = datetime.date.today().isoformat()  # ex: "2026-06-17"
        if not os.path.exists(ARQUIVO_HISTORICO):
            return
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                for linha in f:
                    if linha.startswith(hoje):
                        self.pomodoros_hoje += 1
                        self.minutos_foco_hoje += FOCO_MIN
        except Exception as e:
            print(f"Não consegui ler o histórico: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroKawaii(root)
    root.mainloop()