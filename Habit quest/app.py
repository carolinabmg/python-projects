# habit_quest/app.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from models import (Habito, Missao, Personagem, Frequencia,
                    NivelPersonagem, SistemaDeRecompensas, SaveManager)

# ── PALETA PASTEL KAWAII ───────────────────────────────
COR = {
    "bg":        "#fdf6ff",
    "surface":   "#ffffff",
    "surface2":  "#f3eaff",
    "border":    "#e8d5f5",
    "accent":    "#c084fc",
    "accent2":   "#f9a8d4",
    "accent3":   "#86efac",
    "accent4":   "#fde68a",
    "text":      "#4a3560",
    "muted":     "#9d7fc0",
    "done":      "#86efac",
    "done_bg":   "#f0fdf4",
    "streak":    "#fb923c",
    "missao":    "#f9a8d4",   # rosa para missões
    "missao_bg": "#fff0f7",   # fundo missão ativa
    "expirou":   "#fca5a5",   # vermelho suave para expirado
}

FONT_TITLE    = ("Segoe UI", 20, "bold")
FONT_SUB      = ("Segoe UI", 11)
FONT_MONO     = ("Consolas", 10)
FONT_CARD     = ("Segoe UI", 13, "bold")
FONT_SMALL    = ("Segoe UI", 9)
FONT_EMOJI    = ("Segoe UI Emoji", 48)
FONT_EMOJI_SM = ("Segoe UI Emoji", 18)


# ── WIDGET AUXILIAR: CARD ─────────────────────────────
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
        self.geometry("480x780")
        self.resizable(False, False)
        self.configure(bg=COR["bg"])

        self.save = SaveManager()
        self.personagem, self.habitos, self.missoes = self.save.carregar()
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

        # ── CARD DA PERSONAGEM ──
        self.card_personagem = Card(self, pady=16, padx=16)
        self.card_personagem.pack(fill="x", padx=20, pady=(0, 12))

        self.lbl_emoji = tk.Label(self.card_personagem, text="😴",
                                   font=FONT_EMOJI, bg=COR["surface"])
        self.lbl_emoji.pack()

        self.lbl_nivel = tk.Label(self.card_personagem, text="",
                                   font=("Segoe UI", 12, "bold"),
                                   bg=COR["surface"], fg=COR["accent"])
        self.lbl_nivel.pack(pady=(4, 0))

        self.lbl_sub = tk.Label(self.card_personagem, text="",
                                 font=FONT_SMALL,
                                 bg=COR["surface"], fg=COR["muted"])
        self.lbl_sub.pack()

        xp_frame = tk.Frame(self.card_personagem, bg=COR["surface"])
        xp_frame.pack(fill="x", pady=(10, 0))

        self.lbl_xp = tk.Label(xp_frame, text="", font=FONT_MONO,
                                bg=COR["surface"], fg=COR["muted"])
        self.lbl_xp.pack()

        barra_bg = tk.Frame(xp_frame, bg=COR["border"], height=8, bd=0)
        barra_bg.pack(fill="x", pady=(4, 0))
        barra_bg.pack_propagate(False)

        self.barra_xp = tk.Frame(barra_bg, bg=COR["accent"], height=8, width=0)
        self.barra_xp.place(x=0, y=0, relheight=1)

        self.lbl_moedas = tk.Label(self.card_personagem, text="",
                                    font=FONT_SMALL,
                                    bg=COR["surface"], fg=COR["streak"])
        self.lbl_moedas.pack(pady=(6, 0))

        # ── ABAS: hábitos / missões ──
        abas_frame = tk.Frame(self, bg=COR["bg"])
        abas_frame.pack(fill="x", padx=20, pady=(0, 6))

        self.aba_atual = tk.StringVar(value="habitos")

        self.btn_aba_habitos = tk.Button(
            abas_frame, text="📋 hábitos",
            font=FONT_MONO, relief="flat", cursor="hand2",
            padx=12, pady=5,
            command=lambda: self._trocar_aba("habitos"))
        self.btn_aba_habitos.pack(side="left")

        self.btn_aba_missoes = tk.Button(
            abas_frame, text="⚔️ missões",
            font=FONT_MONO, relief="flat", cursor="hand2",
            padx=12, pady=5,
            command=lambda: self._trocar_aba("missoes"))
        self.btn_aba_missoes.pack(side="left", padx=(6, 0))

        # botão de adicionar — muda dependendo da aba
        self.btn_adicionar = tk.Button(
            abas_frame, text="+ hábito",
            font=FONT_SMALL, bg=COR["accent"], fg="white",
            relief="flat", cursor="hand2", padx=10, pady=4,
            command=self._adicionar_item)
        self.btn_adicionar.pack(side="right")

        # ── SUBTÍTULO DA SEÇÃO ──
        sec = tk.Frame(self, bg=COR["bg"])
        sec.pack(fill="x", padx=20, pady=(0, 8))
        tk.Label(sec, text="// hoje",
                 font=FONT_MONO, bg=COR["bg"], fg=COR["muted"]).pack(side="left")
        self.lbl_progresso_dia = tk.Label(sec, text="",
                                           font=FONT_MONO,
                                           bg=COR["bg"], fg=COR["accent3"])
        self.lbl_progresso_dia.pack(side="right")

        # ── LISTA SCROLLÁVEL ──
        container = tk.Frame(self, bg=COR["bg"])
        container.pack(fill="both", expand=True, padx=20)

        self._canvas = tk.Canvas(container, bg=COR["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical",
                                  command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self.frame_lista = tk.Frame(self._canvas, bg=COR["bg"])
        self._frame_lista_id = self._canvas.create_window(
            (0, 0), window=self.frame_lista, anchor="nw")

        self.frame_lista.bind("<Configure>",
            lambda e: self._canvas.configure(
                scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
            lambda e: self._canvas.itemconfig(
                self._frame_lista_id, width=e.width))

        self._canvas.bind_all("<MouseWheel>",
            lambda e: self._canvas.yview_scroll(-1*(e.delta//120), "units"))

        self._atualizar_abas_visual()

    # ── TROCA DE ABA ──────────────────────────────────
    def _trocar_aba(self, aba: str):
        self.aba_atual.set(aba)
        self._atualizar_abas_visual()
        self._atualizar_lista()

    def _atualizar_abas_visual(self):
        aba = self.aba_atual.get()
        if aba == "habitos":
            self.btn_aba_habitos.config(bg=COR["accent"], fg="white")
            self.btn_aba_missoes.config(bg=COR["surface2"], fg=COR["text"])
            self.btn_adicionar.config(text="+ hábito")
        else:
            self.btn_aba_habitos.config(bg=COR["surface2"], fg=COR["text"])
            self.btn_aba_missoes.config(bg=COR["missao"], fg="white")
            self.btn_adicionar.config(text="+ missão")

    # ── ATUALIZAR TUDO ────────────────────────────────
    def _atualizar_tudo(self):
        self._atualizar_personagem()
        self._atualizar_lista()

    def _atualizar_personagem(self):
        p = self.personagem
        nivel = p.nivel_atual

        emojis = {
            "DORMINHOCA": "😴", "ACORDANDO": "🥱",
            "ANIMADA": "😊",    "FOCADA": "🎯",
            "BRILHANTE": "✨",  "LENDARIA": "🌟",
        }
        self.lbl_emoji.config(text=emojis.get(nivel.name, "😴"))
        self.lbl_nivel.config(text=nivel.descricao)
        self.lbl_sub.config(text=f"Olá, {p.nome}!")
        self.lbl_moedas.config(text=f"🪙 {p.moedas} moedas")

        proximo = p.xp_para_proximo_nivel()
        niveis = list(NivelPersonagem)
        idx = niveis.index(nivel)

        if proximo is not None:
            xp_nivel_atual = niveis[idx].xp_necessario
            xp_proximo = niveis[idx + 1].xp_necessario
            xp_no_nivel = p.xp_total - xp_nivel_atual
            faixa = xp_proximo - xp_nivel_atual
            pct = min(xp_no_nivel / faixa, 1.0) if faixa > 0 else 1.0
            self.lbl_xp.config(
                text=f"XP {p.xp_total} · faltam {proximo} para o próximo nível")
        else:
            pct = 1.0
            self.lbl_xp.config(text=f"XP {p.xp_total} · nível máximo! 🌟")

        self.after(50, lambda: self._animar_barra(pct))

    def _animar_barra(self, pct):
        largura = self._canvas.winfo_width() or 400
        largura_card = largura - 32
        self.barra_xp.config(width=int(largura_card * pct))

    # ── LISTA DINÂMICA (hábitos ou missões) ──────────
    def _atualizar_lista(self):
        for w in self.frame_lista.winfo_children():
            w.destroy()

        if self.aba_atual.get() == "habitos":
            self._renderizar_habitos()
        else:
            self._renderizar_missoes()

    # ── HÁBITOS ───────────────────────────────────────
    def _renderizar_habitos(self):
        if not self.habitos:
            tk.Label(self.frame_lista,
                     text="nenhum hábito ainda.\nclique em '+ hábito' para começar! 🌱",
                     font=FONT_SUB, bg=COR["bg"], fg=COR["muted"],
                     justify="center").pack(pady=40)
            self.lbl_progresso_dia.config(text="")
            return

        completos = sum(1 for h in self.habitos if h.foi_completado_hoje())
        total = len(self.habitos)
        self.lbl_progresso_dia.config(text=f"{completos}/{total} ✓")

        for h in self.habitos:
            self._criar_card_habito(h)

    def _criar_card_habito(self, habito: Habito):
        feito = habito.foi_completado_hoje()
        bg_card = COR["done_bg"] if feito else COR["surface"]
        cor_borda = COR["done"] if feito else COR["border"]

        card = tk.Frame(self.frame_lista, bg=bg_card, bd=0,
                        highlightthickness=1,
                        highlightbackground=cor_borda)
        card.pack(fill="x", pady=5)

        inner = tk.Frame(card, bg=bg_card, padx=14, pady=12)
        inner.pack(fill="x")

        top = tk.Frame(inner, bg=bg_card)
        top.pack(fill="x")

        tk.Label(top, text=habito.icone, font=FONT_EMOJI_SM,
                 bg=bg_card).pack(side="left")

        info = tk.Frame(top, bg=bg_card)
        info.pack(side="left", padx=10, fill="x", expand=True)

        tk.Label(info, text=habito.nome, font=FONT_CARD,
                 bg=bg_card, fg=COR["text"], anchor="w").pack(fill="x")

        meta = f"{habito.frequencia.value}"
        if habito.streak_atual > 0:
            meta += f"  🔥 {habito.streak_atual} dias"
        tk.Label(info, text=meta, font=FONT_SMALL,
                 bg=bg_card, fg=COR["muted"], anchor="w").pack(fill="x")

        if feito:
            tk.Label(top, text="✅", font=FONT_EMOJI_SM,
                     bg=bg_card).pack(side="right")
        else:
            tk.Button(top, text="completar", font=FONT_SMALL,
                      bg=COR["accent"], fg="white", relief="flat",
                      cursor="hand2", padx=10, pady=4,
                      command=lambda h=habito: self._completar_habito(h)
                      ).pack(side="right")

        bottom = tk.Frame(inner, bg=bg_card)
        bottom.pack(fill="x", pady=(6, 0))
        tk.Label(bottom,
                 text=f"+{habito.xp_recompensa} XP  🪙 +{habito.moedas_recompensa}",
                 font=FONT_MONO, bg=bg_card, fg=COR["muted"]).pack(side="left")

        tk.Button(bottom, text="✕", font=FONT_SMALL,
                  bg=bg_card, fg=COR["muted"], relief="flat", cursor="hand2",
                  command=lambda h=habito: self._apagar_habito(h)
                  ).pack(side="right")

    # ── MISSÕES ───────────────────────────────────────
    def _renderizar_missoes(self):
        # separa missões ativas das concluídas
        ativas = [m for m in self.missoes if not m.concluida]
        concluidas = [m for m in self.missoes if m.concluida]

        pendentes = len(ativas)
        total = len(self.missoes)
        self.lbl_progresso_dia.config(
            text=f"{total - pendentes}/{total} ✓" if total else "")

        if not self.missoes:
            tk.Label(self.frame_lista,
                     text="nenhuma missão ainda.\nclique em '+ missão' para criar! ⚔️",
                     font=FONT_SUB, bg=COR["bg"], fg=COR["muted"],
                     justify="center").pack(pady=40)
            return

        # ── missões ativas ──
        if ativas:
            tk.Label(self.frame_lista, text="// em andamento",
                     font=FONT_MONO, bg=COR["bg"], fg=COR["muted"]
                     ).pack(anchor="w", pady=(0, 4))
            for m in ativas:
                self._criar_card_missao(m)

        # ── missões concluídas (colapsado) ──
        if concluidas:
            tk.Label(self.frame_lista, text=f"// concluídas ({len(concluidas)})",
                     font=FONT_MONO, bg=COR["bg"], fg=COR["accent3"]
                     ).pack(anchor="w", pady=(12, 4))
            for m in concluidas:
                self._criar_card_missao(m)

    def _criar_card_missao(self, missao: Missao):
        concluida = missao.concluida
        expirada = missao.esta_expirada()

        if concluida:
            bg_card = COR["done_bg"]
            cor_borda = COR["done"]
        elif expirada:
            bg_card = "#fff5f5"
            cor_borda = COR["expirou"]
        else:
            bg_card = COR["missao_bg"]
            cor_borda = COR["missao"]

        card = tk.Frame(self.frame_lista, bg=bg_card, bd=0,
                        highlightthickness=1,
                        highlightbackground=cor_borda)
        card.pack(fill="x", pady=5)

        inner = tk.Frame(card, bg=bg_card, padx=14, pady=12)
        inner.pack(fill="x")

        top = tk.Frame(inner, bg=bg_card)
        top.pack(fill="x")

        tk.Label(top, text=missao.icone, font=FONT_EMOJI_SM,
                 bg=bg_card).pack(side="left")

        info = tk.Frame(top, bg=bg_card)
        info.pack(side="left", padx=10, fill="x", expand=True)

        tk.Label(info, text=missao.nome, font=FONT_CARD,
                 bg=bg_card, fg=COR["text"], anchor="w").pack(fill="x")

        tk.Label(info, text=f"📅 {missao.prazo_texto()}",
                 font=FONT_SMALL, bg=bg_card, fg=COR["muted"],
                 anchor="w").pack(fill="x")

        # botão direito: concluir / check / expirou
        if concluida:
            tk.Label(top, text="✅", font=FONT_EMOJI_SM,
                     bg=bg_card).pack(side="right")
        elif expirada:
            tk.Label(top, text="⌛", font=FONT_EMOJI_SM,
                     bg=bg_card).pack(side="right")
        else:
            tk.Button(top, text="concluir", font=FONT_SMALL,
                      bg=COR["missao"], fg="white", relief="flat",
                      cursor="hand2", padx=10, pady=4,
                      command=lambda m=missao: self._concluir_missao(m)
                      ).pack(side="right")

        # rodapé: recompensa + apagar
        bottom = tk.Frame(inner, bg=bg_card)
        bottom.pack(fill="x", pady=(6, 0))
        tk.Label(bottom,
                 text=f"+{missao.xp_recompensa} XP  🪙 +{missao.moedas_recompensa}",
                 font=FONT_MONO, bg=bg_card, fg=COR["muted"]).pack(side="left")

        tk.Button(bottom, text="✕", font=FONT_SMALL,
                  bg=bg_card, fg=COR["muted"], relief="flat", cursor="hand2",
                  command=lambda m=missao: self._apagar_missao(m)
                  ).pack(side="right")

    # ── AÇÕES: HÁBITOS ────────────────────────────────
    def _completar_habito(self, habito: Habito):
        xp, moedas = habito.completar_hoje()
        if xp == 0:
            return

        subiu = self.personagem.ganhar_xp(xp)
        self.personagem.ganhar_moedas(moedas)
        novas = self.recompensas.verificar(
            self.personagem, self.habitos, self.missoes)

        self.save.salvar(self.personagem, self.habitos, self.missoes)
        self._atualizar_tudo()

        msg = f"{habito.icone} {habito.nome} completo!\n+{xp} XP  🪙 +{moedas}"
        if subiu:
            msg += f"\n\n🎉 Subiu de nível!\n{self.personagem.nivel_atual.descricao}"
        if novas:
            nomes = [self.recompensas.CONQUISTAS[c][0] for c in novas]
            msg += "\n\n🏆 Nova conquista!\n" + "\n".join(nomes)

        messagebox.showinfo("✨ hábito completo!", msg)

    def _adicionar_habito(self):
        nome = simpledialog.askstring("novo hábito", "nome do hábito:", parent=self)
        if not nome or not nome.strip():
            return
        icone = simpledialog.askstring("ícone", "escolha um emoji:",
                                        initialvalue="⭐", parent=self) or "⭐"
        self.habitos.append(Habito(nome.strip(), icone.strip()))
        self.save.salvar(self.personagem, self.habitos, self.missoes)
        self._atualizar_lista()

    def _apagar_habito(self, habito: Habito):
        if messagebox.askyesno("apagar", f"Apagar '{habito.nome}'?", parent=self):
            self.habitos.remove(habito)
            self.save.salvar(self.personagem, self.habitos, self.missoes)
            self._atualizar_lista()

    # ── AÇÕES: MISSÕES ────────────────────────────────
    def _concluir_missao(self, missao: Missao):
        xp, moedas = missao.concluir()
        if xp == 0:
            return

        subiu = self.personagem.ganhar_xp(xp)
        self.personagem.ganhar_moedas(moedas)
        novas = self.recompensas.verificar(
            self.personagem, self.habitos, self.missoes)

        self.save.salvar(self.personagem, self.habitos, self.missoes)
        self._atualizar_tudo()

        msg = f"{missao.icone} {missao.nome} concluída!\n+{xp} XP  🪙 +{moedas}"
        if subiu:
            msg += f"\n\n🎉 Subiu de nível!\n{self.personagem.nivel_atual.descricao}"
        if novas:
            nomes = [self.recompensas.CONQUISTAS[c][0] for c in novas]
            msg += "\n\n🏆 Nova conquista!\n" + "\n".join(nomes)

        messagebox.showinfo("⚔️ missão concluída!", msg)

    def _adicionar_missao(self):
        nome = simpledialog.askstring("nova missão", "nome da missão:", parent=self)
        if not nome or not nome.strip():
            return

        icone = simpledialog.askstring("ícone", "escolha um emoji:",
                                        initialvalue="🗡️", parent=self) or "🗡️"

        prazo = simpledialog.askstring(
            "prazo",
            "data limite (AAAA-MM-DD) ou deixe em branco para sem prazo:",
            parent=self)

        # valida o prazo digitado
        prazo_final = None
        if prazo and prazo.strip():
            try:
                from datetime import datetime as dt
                dt.strptime(prazo.strip(), "%Y-%m-%d")
                prazo_final = prazo.strip()
            except ValueError:
                messagebox.showwarning(
                    "data inválida",
                    "Formato errado! Use AAAA-MM-DD.\nA missão foi criada sem prazo.",
                    parent=self)

        xp_str = simpledialog.askstring(
            "recompensa", "XP de recompensa (padrão: 50):",
            initialvalue="50", parent=self) or "50"

        try:
            xp = int(xp_str)
        except ValueError:
            xp = 50

        self.missoes.append(
            Missao(nome.strip(), icone.strip(),
                   xp_recompensa=xp,
                   prazo=prazo_final))

        self.save.salvar(self.personagem, self.habitos, self.missoes)
        self._atualizar_lista()

    def _apagar_missao(self, missao: Missao):
        if messagebox.askyesno("apagar", f"Apagar missão '{missao.nome}'?", parent=self):
            self.missoes.remove(missao)
            self.save.salvar(self.personagem, self.habitos, self.missoes)
            self._atualizar_lista()

    # ── BOTÃO + DINÂMICO ──────────────────────────────
    def _adicionar_item(self):
        if self.aba_atual.get() == "habitos":
            self._adicionar_habito()
        else:
            self._adicionar_missao()


# ── MAIN ───────────────────────────────────────────────
if __name__ == "__main__":
    app = HabitQuestApp()
    app.mainloop()