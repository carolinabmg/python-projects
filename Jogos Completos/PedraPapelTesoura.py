import random
import tkinter as tk
from tkinter import font as tkfont

# ── Paleta ──────────────────────────────────────────────────────────────────
BG        = "#1A1A2E"   # fundo principal (azul-noite)
BG2       = "#16213E"   # fundo dos cards
ACCENT    = "#E94560"   # vermelho-rosa (destaque)
WIN_COR   = "#0F6E56"   # verde vitória
LOSS_COR  = "#993C1D"   # laranja derrota
DRAW_COR  = "#185FA5"   # azul empate
TXT       = "#EAE6FF"   # texto claro
TXT_MUT   = "#888080"   # texto secundário
BTN_HO    = "#2C2C54"   # hover dos botões

OPCOES        = ["pedra", "papel", "tesoura"]
EMOJI         = {"pedra": "🪨", "papel": "📄", "tesoura": "✂️"}
VENCE_CONTRA  = {"pedra": "tesoura", "papel": "pedra", "tesoura": "papel"}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pedra · Papel · Tesoura")
        self.resizable(False, False)
        self.configure(bg=BG)

        # placar
        self.placar = {"vitoria": 0, "empate": 0, "derrota": 0}

        # fontes
        self.f_titulo  = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.f_emoji   = tkfont.Font(family="Segoe UI Emoji", size=40)
        self.f_result  = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.f_score   = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.f_label   = tkfont.Font(family="Segoe UI", size=10)
        self.f_btn     = tkfont.Font(family="Segoe UI Emoji", size=28)

        self._build_ui()

    # ── Construção da interface ──────────────────────────────────────────────
    def _build_ui(self):
        pad = {"padx": 20, "pady": 12}

        # título
        tk.Label(self, text="Pedra · Papel · Tesoura",
                 font=self.f_titulo, bg=BG, fg=ACCENT).pack(pady=(20, 4))

        # placar
        self._frame_placar()

        # arena
        self._frame_arena()

        # mensagem de resultado
        self.lbl_result = tk.Label(self, text="Escolha uma opção abaixo",
                                   font=self.f_result, bg=BG, fg=TXT_MUT)
        self.lbl_result.pack(pady=(4, 12))

        # botões de escolha
        self._frame_botoes()

        # botão resetar
        btn_reset = tk.Button(self, text="Resetar placar",
                              font=self.f_label, bg=BG2, fg=TXT_MUT,
                              activebackground=BTN_HO, activeforeground=TXT,
                              relief="flat", bd=0, cursor="hand2",
                              command=self._resetar)
        btn_reset.pack(pady=(0, 20))

    def _frame_placar(self):
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="x", padx=24, pady=(0, 8))

        dados = [("Você", "vitoria", WIN_COR),
                 ("Empates", "empate", DRAW_COR),
                 ("PC", "derrota", LOSS_COR)]

        self.lbl_scores = {}
        for i, (nome, chave, cor) in enumerate(dados):
            card = tk.Frame(frame, bg=BG2, bd=0)
            card.grid(row=0, column=i, padx=5, pady=4, sticky="nsew")
            frame.columnconfigure(i, weight=1)

            tk.Label(card, text=nome, font=self.f_label,
                     bg=BG2, fg=TXT_MUT).pack(pady=(8, 0))
            lbl = tk.Label(card, text="0", font=self.f_score,
                           bg=BG2, fg=cor)
            lbl.pack(pady=(0, 8))
            self.lbl_scores[chave] = lbl

    def _frame_arena(self):
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="x", padx=24, pady=4)

        # lado jogador
        lado_j = tk.Frame(frame, bg=BG)
        lado_j.grid(row=0, column=0, sticky="nsew")
        tk.Label(lado_j, text="VOCÊ", font=self.f_label,
                 bg=BG, fg=TXT_MUT).pack()
        self.lbl_pick_j = tk.Label(lado_j, text="❓",
                                   font=self.f_emoji, bg=BG, fg=TXT)
        self.lbl_pick_j.pack()

        # separador ×
        tk.Label(frame, text="×", font=self.f_result,
                 bg=BG, fg=TXT_MUT).grid(row=0, column=1, padx=16)

        # lado pc
        lado_pc = tk.Frame(frame, bg=BG)
        lado_pc.grid(row=0, column=2, sticky="nsew")
        tk.Label(lado_pc, text="COMPUTADOR", font=self.f_label,
                 bg=BG, fg=TXT_MUT).pack()
        self.lbl_pick_pc = tk.Label(lado_pc, text="❓",
                                    font=self.f_emoji, bg=BG, fg=TXT)
        self.lbl_pick_pc.pack()

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(2, weight=1)

    def _frame_botoes(self):
        frame = tk.Frame(self, bg=BG)
        frame.pack(pady=(0, 16))

        for opcao in OPCOES:
            btn = tk.Button(
                frame,
                text=EMOJI[opcao],
                font=self.f_btn,
                width=3,
                bg=BG2, fg=TXT,
                activebackground=BTN_HO, activeforeground=TXT,
                relief="flat", bd=0, cursor="hand2",
                command=lambda o=opcao: self._jogar(o),
            )
            btn.pack(side="left", padx=8)
            # efeitos hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_HO))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG2))

    # ── Lógica do jogo ───────────────────────────────────────────────────────
    def _jogar(self, jogador: str):
        pc = random.choice(OPCOES)

        self.lbl_pick_j.config(text=EMOJI[jogador])
        self.lbl_pick_pc.config(text=EMOJI[pc])

        if jogador == pc:
            resultado, msg, cor = "empate", "🤝 Empate!", DRAW_COR
        elif VENCE_CONTRA[jogador] == pc:
            resultado, msg, cor = "vitoria", "🏆 Você ganhou!", WIN_COR
        else:
            resultado, msg, cor = "derrota", "💻 Computador ganhou!", LOSS_COR

        self.placar[resultado] += 1
        self.lbl_scores[resultado].config(
            text=str(self.placar[resultado])
        )
        self.lbl_result.config(text=msg, fg=cor)

    def _resetar(self):
        self.placar = {"vitoria": 0, "empate": 0, "derrota": 0}
        for chave, lbl in self.lbl_scores.items():
            lbl.config(text="0")
        self.lbl_pick_j.config(text="❓")
        self.lbl_pick_pc.config(text="❓")
        self.lbl_result.config(text="Escolha uma opção abaixo", fg=TXT_MUT)


if __name__ == "__main__":
    app = App()
    app.mainloop()