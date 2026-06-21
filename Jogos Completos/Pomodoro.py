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
# Configurações padrão
# ──────────────────────────────────────────────────────────────
FOCO_MIN_PADRAO = 25
PAUSA_MIN_PADRAO = 5

# Paleta rosa pastel 🌸
CORES = {
    "fundo":     "#FFF0F5",
    "cartao":    "#FFE4EC",
    "acento":    "#FF8FB1",
    "acento2":   "#FFC1CC",
    "texto":     "#6D5D6E",
    "texto_sec": "#A48BA6",
    "pausa":     "#9ED5C5",
    "erro":      "#FF6B6B",
    "input_bd":  "#FFAAC5",
    "input_foc": "#FF8FB1",
}

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_HISTORICO = os.path.join(PASTA, "historico_pomodoro.txt")


class PomodoroKawaii:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Pomodoro Kawaii 🌸")
        self.root.configure(bg=CORES["fundo"])
        self.root.geometry("360x620")
        self.root.resizable(False, False)

        # Valores configuráveis (em minutos)
        self.foco_min = FOCO_MIN_PADRAO
        self.pausa_min = PAUSA_MIN_PADRAO

        # Estado interno
        self.modo = "foco"
        self.segundos = self.foco_min * 60
        self.rodando = False
        self.after_id = None

        # Estatísticas
        self.pomodoros_hoje = 0
        self.minutos_foco_hoje = 0
        self._carregar_stats()

        # Fontes
        self.f_titulo  = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.f_timer   = tkfont.Font(family="Consolas", size=52, weight="bold")
        self.f_normal  = tkfont.Font(family="Segoe UI", size=11)
        self.f_pequena = tkfont.Font(family="Segoe UI", size=9)
        self.f_botao   = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.f_label   = tkfont.Font(family="Segoe UI", size=10)

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
        ).pack(pady=(18, 2))

        self.lbl_patente = tk.Label(
            self.root, text="", font=self.f_normal,
            bg=CORES["fundo"], fg=CORES["texto_sec"]
        )
        self.lbl_patente.pack(pady=(0, 10))

        # ── Painel de configuração de tempo ──────────────────
        cfg = tk.Frame(self.root, bg=CORES["cartao"], bd=0)
        cfg.pack(padx=24, pady=(0, 8), fill="x")

        tk.Label(
            cfg, text="⚙️ Configurar tempos (min)",
            font=self.f_label, bg=CORES["cartao"], fg=CORES["texto"]
        ).grid(row=0, column=0, columnspan=4, pady=(12, 6))

        # Foco
        tk.Label(
            cfg, text="📚 Foco:", font=self.f_label,
            bg=CORES["cartao"], fg=CORES["texto"]
        ).grid(row=1, column=0, padx=(16, 4), pady=(0, 12), sticky="e")

        self.var_foco = tk.StringVar(value=str(self.foco_min))
        self.entry_foco = self._criar_entry(cfg, self.var_foco)
        self.entry_foco.grid(row=1, column=1, padx=(0, 16), pady=(0, 12))

        # Pausa
        tk.Label(
            cfg, text="☕ Pausa:", font=self.f_label,
            bg=CORES["cartao"], fg=CORES["texto"]
        ).grid(row=1, column=2, padx=(8, 4), pady=(0, 12), sticky="e")

        self.var_pausa = tk.StringVar(value=str(self.pausa_min))
        self.entry_pausa = self._criar_entry(cfg, self.var_pausa)
        self.entry_pausa.grid(row=1, column=3, padx=(0, 16), pady=(0, 12))

        # Botão aplicar
        self.btn_aplicar = tk.Button(
            cfg, text="✔ Aplicar", font=self.f_pequena,
            bg=CORES["acento"], fg="white",
            activebackground=CORES["acento2"], activeforeground=CORES["texto"],
            bd=0, padx=12, pady=5, cursor="hand2",
            command=self._aplicar_config
        )
        self.btn_aplicar.grid(row=2, column=0, columnspan=4, pady=(0, 12))

        # Mensagem de erro/confirmação da config
        self.lbl_cfg_msg = tk.Label(
            cfg, text="", font=self.f_pequena,
            bg=CORES["cartao"], fg=CORES["erro"]
        )
        self.lbl_cfg_msg.grid(row=3, column=0, columnspan=4, pady=(0, 6))

        # ── Cartão do timer ───────────────────────────────────
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

        # ── Botões de controle ────────────────────────────────
        botoes = tk.Frame(self.root, bg=CORES["fundo"])
        botoes.pack(pady=14)

        self.btn_iniciar = tk.Button(
            botoes, text="▶ Iniciar", font=self.f_botao,
            bg=CORES["acento"], fg="white", activebackground=CORES["acento2"],
            activeforeground="white", bd=0, padx=20, pady=8,
            cursor="hand2", command=self.alternar_play
        )
        self.btn_iniciar.grid(row=0, column=0, padx=6)

        self.btn_resetar = tk.Button(
            botoes, text="↺ Resetar", font=self.f_botao,
            bg=CORES["acento2"], fg=CORES["texto"],
            activebackground=CORES["cartao"], activeforeground=CORES["texto"],
            bd=0, padx=20, pady=8,
            cursor="hand2", command=self.resetar
        )
        self.btn_resetar.grid(row=0, column=1, padx=6)

        # ── Estatísticas ──────────────────────────────────────
        stats = tk.Frame(self.root, bg=CORES["fundo"])
        stats.pack(pady=(6, 0))

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
        ).pack(side="bottom", pady=10)

    def _criar_entry(self, parent, textvariable):
        """Cria um campo numérico estilizado."""
        e = tk.Entry(
            parent, textvariable=textvariable,
            width=4, justify="center",
            font=self.f_label,
            bg="white", fg=CORES["texto"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=CORES["input_bd"],
            highlightcolor=CORES["input_foc"],
        )
        return e

    # ──────────────────────────────────────────────────────────
    # Aplicar configuração de tempo
    # ──────────────────────────────────────────────────────────
    def _aplicar_config(self):
        """Valida e aplica os novos valores de foco e pausa."""
        if self.rodando:
            self._mostrar_msg_cfg("⚠️ Pause o timer antes de alterar.", erro=True)
            return

        try:
            novo_foco = int(self.var_foco.get())
            nova_pausa = int(self.var_pausa.get())
        except ValueError:
            self._mostrar_msg_cfg("Use apenas números inteiros!", erro=True)
            return

        if not (1 <= novo_foco <= 120):
            self._mostrar_msg_cfg("Foco: entre 1 e 120 min.", erro=True)
            return

        if not (1 <= nova_pausa <= 60):
            self._mostrar_msg_cfg("Pausa: entre 1 e 60 min.", erro=True)
            return

        self.foco_min = novo_foco
        self.pausa_min = nova_pausa

        # Reinicia o timer com os novos valores
        self._iniciar_modo(self.modo)
        self._atualizar_display()
        self._mostrar_msg_cfg(f"✔ Aplicado: {novo_foco}min foco / {nova_pausa}min pausa", erro=False)

    def _mostrar_msg_cfg(self, texto, erro=True):
        cor = CORES["erro"] if erro else "#7CBB8A"
        self.lbl_cfg_msg.config(text=texto, fg=cor)
        # Limpa a mensagem após 3 segundos
        self.root.after(3000, lambda: self.lbl_cfg_msg.config(text=""))

    # ──────────────────────────────────────────────────────────
    # Lógica do timer
    # ──────────────────────────────────────────────────────────
    def alternar_play(self):
        if not self.rodando:
            self.rodando = True
            self.btn_iniciar.config(text="⏸ Pausar")
            # Bloqueia os campos durante a sessão
            self._toggle_config(habilitado=False)
            self._tick()
        else:
            self.rodando = False
            self.btn_iniciar.config(text="▶ Continuar")
            self._toggle_config(habilitado=True)
            if self.after_id:
                self.root.after_cancel(self.after_id)

    def _toggle_config(self, habilitado: bool):
        """Habilita ou desabilita os campos e o botão de configuração."""
        estado = "normal" if habilitado else "disabled"
        self.entry_foco.config(state=estado)
        self.entry_pausa.config(state=estado)
        self.btn_aplicar.config(state=estado)

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
            self.pomodoros_hoje += 1
            self.minutos_foco_hoje += self.foco_min
            self._salvar_historico()
            self._atualizar_stats()
            self._iniciar_modo("pausa")
        else:
            self._iniciar_modo("foco")

        self.rodando = True
        self.btn_iniciar.config(text="⏸ Pausar")
        self._tick()

    def _iniciar_modo(self, modo):
        self.modo = modo
        if modo == "foco":
            self.segundos = self.foco_min * 60
            self.lbl_estado.config(text="📚 Foco")
            self.lbl_timer.config(fg=CORES["acento"])
        else:
            self.segundos = self.pausa_min * 60
            self.lbl_estado.config(text="☕ Pausa")
            self.lbl_timer.config(fg=CORES["pausa"])

    def resetar(self):
        self.rodando = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self._iniciar_modo("foco")
        self.btn_iniciar.config(text="▶ Iniciar")
        self._toggle_config(habilitado=True)
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
        if n >= 10: return "🏆 Arquimaga Python"
        if n >= 5:  return "✨ Maga do Código"
        if n >= 1:  return "🌱 Aprendiz"
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
                self.root.bell()
        except Exception:
            try:
                self.root.bell()
            except Exception:
                pass

    # ──────────────────────────────────────────────────────────
    # Persistência
    # ──────────────────────────────────────────────────────────
    def _salvar_historico(self):
        agora = datetime.datetime.now().isoformat(timespec="seconds")
        linha = f"{agora} - Pomodoro de foco concluído ({self.foco_min} min)\n"
        try:
            with open(ARQUIVO_HISTORICO, "a", encoding="utf-8") as f:
                f.write(linha)
        except Exception as e:
            print(f"Não consegui salvar o histórico: {e}")

    def _carregar_stats(self):
        hoje = datetime.date.today().isoformat()
        if not os.path.exists(ARQUIVO_HISTORICO):
            return
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                for linha in f:
                    if linha.startswith(hoje):
                        self.pomodoros_hoje += 1
                        # Tenta ler os minutos salvos na linha
                        try:
                            mins = int(linha.split("(")[1].split(" min)")[0])
                        except Exception:
                            mins = FOCO_MIN_PADRAO
                        self.minutos_foco_hoje += mins
        except Exception as e:
            print(f"Não consegui ler o histórico: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroKawaii(root)
    root.mainloop()