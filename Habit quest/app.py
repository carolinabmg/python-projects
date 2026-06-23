# habit_quest/app.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from models import (Habito, Personagem, Frequencia,
                    NivelPersonagem, SistemaDeRecompensas, SaveManager)

# ── PALETA PASTEL KAWAII ───────────────────────────────
COR = {
    "bg":        "#fdf6ff",   # fundo lilás bem clarinho
    "surface":   "#ffffff",   # cards brancos
    "surface2":  "#f3eaff",   # fundo de campos
    "border":    "#e8d5f5",   # bordas roxo pastel
    "accent":    "#c084fc",   # roxo pastel principal
    "accent2":   "#f9a8d4",   # rosa pastel
    "accent3":   "#86efac",   # verde menta
    "accent4":   "#fde68a",   # amarelo pastel
    "text":      "#4a3560",   # texto roxo escuro
    "muted":     "#9d7fc0",   # texto secundário
    "done":      "#86efac",   # verde hábito completo
    "done_bg":   "#f0fdf4",   # fundo hábito completo
    "streak":    "#fb923c",   # laranja streak
}

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_SUB    = ("Segoe UI", 11)
FONT_MONO   = ("Consolas", 10)
FONT_CARD   = ("Segoe UI", 13, "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_EMOJI  = ("Segoe UI Emoji", 48)
FONT_EMOJI_SM = ("Segoe UI Emoji", 18)

RAIO = 16  # border radius simulado com padding


# ── WIDGET AUXILIAR: CARD ARREDONDADO ─────────────────
class Card(tk.Frame):
    def __init__(self, master, bg=None, **kw):
        super().__init__(master, bg=bg or COR["surface"],
                         bd=0, highlightthickness=1,
                         highlightbackground=COR["border"], **kw)


# ── TELA PRINCIPAL ─────────────────────────────────────
class HabitQuestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌸 Habit Quest")
        self.geometry("480x720")
        self.resizable(False, False)
        self.configure(bg=COR["bg"])

        self.save = SaveManager()
        self.personagem, self.habitos = self.save.carregar()
        self.recompensas = SistemaDeRecompensas()

        self._build_ui()
        self._atualizar_tudo()

    # ── CONSTRUÇÃO DA UI ──────────────────────────────
    def _build_ui(self):
        # ── HEADER ──
        header = tk.Frame(self, bg=COR["bg"], pady=8)
        header.pack(fill="x", padx=20)

        tk.Label(header, text="🌸 habit quest",
                 font=("Segoe UI", 14, "bold"),
                 bg=COR["bg"], fg=COR["accent"]).pack(side="left")

        tk.Button(header, text="+ hábito",
                  font=FONT_SMALL, bg=COR["accent"], fg="white",
                  relief="flat", cursor="hand2", padx=10, pady=4,
                  command=self._adicionar_habito).pack(side="right")

        # ── CARD DA PERSONAGEM ──
        self.card_personagem = Card(self, pady=16, padx=16)
        self.card_personagem.pack(fill="x", padx=20, pady=(0, 12))

        # emoji do nível
        self.lbl_emoji = tk.Label(self.card_personagem, text="😴",
                                   font=FONT_EMOJI,
                                   bg=COR["surface"])
        self.lbl_emoji.pack()

        # nome e nível
        self.lbl_nivel = tk.Label(self.card_personagem, text="",
                                   font=("Segoe UI", 12, "bold"),
                                   bg=COR["surface"], fg=COR["accent"])
        self.lbl_nivel.pack(pady=(4, 0))

        self.lbl_sub = tk.Label(self.card_personagem, text="",
                                 font=FONT_SMALL,
                                 bg=COR["surface"], fg=COR["muted"])
        self.lbl_sub.pack()

        # barra de XP
        xp_frame = tk.Frame(self.card_personagem, bg=COR["surface"])
        xp_frame.pack(fill="x", pady=(10, 0))

        self.lbl_xp = tk.Label(xp_frame, text="",
                                font=FONT_MONO,
                                bg=COR["surface"], fg=COR["muted"])
        self.lbl_xp.pack()

        barra_bg = tk.Frame(xp_frame, bg=COR["border"],
                             height=8, bd=0)
        barra_bg.pack(fill="x", pady=(4, 0))
        barra_bg.pack_propagate(False)

        self.barra_xp = tk.Frame(barra_bg, bg=COR["accent"],
                                  height=8, width=0)
        self.barra_xp.place(x=0, y=0, relheight=1)

        # moedas
        self.lbl_moedas = tk.Label(self.card_personagem, text="",
                                    font=FONT_SMALL,
                                    bg=COR["surface"], fg=COR["streak"])
        self.lbl_moedas.pack(pady=(6, 0))

        # ── TÍTULO SEÇÃO HÁBITOS ──
        sec = tk.Frame(self, bg=COR["bg"])
        sec.pack(fill="x", padx=20, pady=(0, 8))
        tk.Label(sec, text="// hoje",
                 font=FONT_MONO,
                 bg=COR["bg"], fg=COR["muted"]).pack(side="left")
        self.lbl_progresso_dia = tk.Label(sec, text="",
                                           font=FONT_MONO,
                                           bg=COR["bg"], fg=COR["accent3"])
        self.lbl_progresso_dia.pack(side="right")

        # ── LISTA DE HÁBITOS (scrollável) ──
        container = tk.Frame(self, bg=COR["bg"])
        container.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(container, bg=COR["bg"],
                            highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical",
                                  command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.frame_habitos = tk.Frame(canvas, bg=COR["bg"])
        self.frame_habitos_id = canvas.create_window(
            (0, 0), window=self.frame_habitos, anchor="nw")

        self.frame_habitos.bind("<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(
                self.frame_habitos_id, width=e.width))

        # scroll com mouse
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        self._canvas = canvas

    # ── ATUALIZAR UI ──────────────────────────────────
    def _atualizar_tudo(self):
        self._atualizar_personagem()
        self._atualizar_habitos()

    def _atualizar_personagem(self):
        p = self.personagem
        nivel = p.nivel_atual

        # emoji muda por nível
        emojis = {
            "DORMINHOCA": "😴",
            "ACORDANDO":  "🥱",
            "ANIMADA":    "😊",
            "FOCADA":     "🎯",
            "BRILHANTE":  "✨",
            "LENDARIA":   "🌟",
        }
        self.lbl_emoji.config(text=emojis.get(nivel.name, "😴"))
        self.lbl_nivel.config(text=nivel.descricao)
        self.lbl_sub.config(text=f"Olá, {p.nome}!")
        self.lbl_moedas.config(text=f"🪙 {p.moedas} moedas")

        # barra de XP
        proximo = p.xp_para_proximo_nivel()
        niveis = list(NivelPersonagem)
        idx = niveis.index(nivel)
        if proximo is not None:
            xp_nivel_atual = niveis[idx].xp_necessario
            xp_proximo = niveis[idx + 1].xp_necessario
            xp_no_nivel = p.xp_total - xp_nivel_atual
            faixa = xp_proximo - xp_nivel_atual
            pct = min(xp_no_nivel / faixa, 1.0) if faixa > 0 else 1.0
            self.lbl_xp.config(text=f"XP {p.xp_total} · faltam {proximo} para o próximo nível")
        else:
            pct = 1.0
            self.lbl_xp.config(text=f"XP {p.xp_total} · nível máximo! 🌟")

        # atualiza barra após render
        self.after(50, lambda: self._animar_barra(pct))

    def _animar_barra(self, pct):
        largura = self._canvas.winfo_width() or 400
        largura_card = largura - 32
        self.barra_xp.config(width=int(largura_card * pct))

    def _atualizar_habitos(self):
        # limpa frame
        for w in self.frame_habitos.winfo_children():
            w.destroy()

        if not self.habitos:
            tk.Label(self.frame_habitos,
                     text="nenhum hábito ainda.\nclique em '+ hábito' para começar! 🌱",
                     font=FONT_SUB, bg=COR["bg"], fg=COR["muted"],
                     justify="center").pack(pady=40)
            self.lbl_progresso_dia.config(text="")
            return

        completos = sum(1 for h in self.habitos if h.foi_completado_hoje())
        total = len(self.habitos)
        self.lbl_progresso_dia.config(
            text=f"{completos}/{total} ✓")

        for h in self.habitos:
            self._criar_card_habito(h)

    def _criar_card_habito(self, habito: Habito):
        feito = habito.foi_completado_hoje()
        bg_card = COR["done_bg"] if feito else COR["surface"]
        cor_borda = COR["done"] if feito else COR["border"]

        card = tk.Frame(self.frame_habitos,
                        bg=bg_card, bd=0,
                        highlightthickness=1,
                        highlightbackground=cor_borda)
        card.pack(fill="x", pady=5)

        inner = tk.Frame(card, bg=bg_card, padx=14, pady=12)
        inner.pack(fill="x")

        # linha superior: emoji + nome + streak
        top = tk.Frame(inner, bg=bg_card)
        top.pack(fill="x")

        tk.Label(top, text=habito.icone,
                 font=FONT_EMOJI_SM,
                 bg=bg_card).pack(side="left")

        info = tk.Frame(top, bg=bg_card)
        info.pack(side="left", padx=10, fill="x", expand=True)

        tk.Label(info, text=habito.nome,
                 font=FONT_CARD,
                 bg=bg_card, fg=COR["text"],
                 anchor="w").pack(fill="x")

        meta = f"{habito.frequencia.value}"
        if habito.streak_atual > 0:
            meta += f"  🔥 {habito.streak_atual} dias"
        tk.Label(info, text=meta,
                 font=FONT_SMALL,
                 bg=bg_card, fg=COR["muted"],
                 anchor="w").pack(fill="x")

        # botão ou check
        if feito:
            tk.Label(top, text="✅",
                     font=FONT_EMOJI_SM,
                     bg=bg_card).pack(side="right")
        else:
            btn = tk.Button(top, text="completar",
                            font=FONT_SMALL,
                            bg=COR["accent"], fg="white",
                            relief="flat", cursor="hand2",
                            padx=10, pady=4,
                            command=lambda h=habito: self._completar(h))
            btn.pack(side="right")

        # recompensas
        bottom = tk.Frame(inner, bg=bg_card)
        bottom.pack(fill="x", pady=(6, 0))
        tk.Label(bottom,
                 text=f"+{habito.xp_recompensa} XP  🪙 +{habito.moedas_recompensa}",
                 font=FONT_MONO,
                 bg=bg_card, fg=COR["muted"]).pack(side="left")

        # botão apagar
        tk.Button(bottom, text="✕",
                  font=FONT_SMALL,
                  bg=bg_card, fg=COR["muted"],
                  relief="flat", cursor="hand2",
                  command=lambda h=habito: self._apagar_habito(h)
                  ).pack(side="right")

    # ── AÇÕES ─────────────────────────────────────────
    def _completar(self, habito: Habito):
        xp, moedas = habito.completar_hoje()
        if xp == 0:
            return  # já completado

        subiu = self.personagem.ganhar_xp(xp)
        self.personagem.ganhar_moedas(moedas)

        # verifica conquistas
        novas = self.recompensas.verificar(self.personagem, self.habitos)

        self.save.salvar(self.personagem, self.habitos)
        self._atualizar_tudo()

        # feedback
        msg = f"{habito.icone} {habito.nome} completo!\n+{xp} XP  🪙 +{moedas}"
        if subiu:
            msg += f"\n\n🎉 Subiu de nível!\n{self.personagem.nivel_atual.descricao}"
        if novas:
            nomes = [self.recompensas.CONQUISTAS[c][0] for c in novas]
            msg += f"\n\n🏆 Nova conquista!\n" + "\n".join(nomes)

        messagebox.showinfo("✨ hábito completo!", msg)

    def _adicionar_habito(self):
        nome = simpledialog.askstring("novo hábito",
                                       "nome do hábito:",
                                       parent=self)
        if not nome or not nome.strip():
            return

        icone = simpledialog.askstring("ícone",
                                        "escolha um emoji:",
                                        initialvalue="⭐",
                                        parent=self) or "⭐"

        h = Habito(nome.strip(), icone.strip())
        self.habitos.append(h)
        self.save.salvar(self.personagem, self.habitos)
        self._atualizar_habitos()

    def _apagar_habito(self, habito: Habito):
        if messagebox.askyesno("apagar",
                                f"Apagar '{habito.nome}'?",
                                parent=self):
            self.habitos.remove(habito)
            self.save.salvar(self.personagem, self.habitos)
            self._atualizar_habitos()


# ── MAIN ───────────────────────────────────────────────
if __name__ == "__main__":
    app = HabitQuestApp()
    app.mainloop()