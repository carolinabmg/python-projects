"""
🎀 MEMORY GAME DELUXE KAWAII RPG - VERSÃO 8.0 (POO) 🌸
╔══════════════════════════════════════════════════════╗
║        AGORA DÁ PRA RESETAR SÓ O RANKING            ║
╚══════════════════════════════════════════════════════╝

✨ NOVIDADES DA v8.0:
  ✅ Botão "♻️ Resetar Ranking" dentro da tela de Ranking
       → apaga SÓ o top 10. Os perfis e o progresso ficam intactos!
  ✅ Se o ranking já estiver vazio, o jogo avisa com carinho
       (em vez de não fazer nada).
  ✅ Corrigido um detalhe técnico: o jogo abria o "loop" duas vezes.

  (Continua tudo da v7: fluidez sem pop-ups chatos, avisos de
   segurança, navegação clara, ajuda visual, vários perfis,
   comparação, salvar/continuar, conquistas e níveis com título.)
"""

import tkinter as tk
from tkinter import messagebox, font
import random
import time
import json
import os

# =====================================================
# CORES KAWAII PASTEL
# =====================================================
BG = "#FFF0F6"
PINK = "#FFB6C1"
LILAC = "#D8B4FE"
BLUE = "#BDE0FE"
MINT = "#C7F9CC"
PEACH = "#FFD6A5"
YELLOW = "#FDFFB6"
PURPLE = "#E0C3FC"
CORAL = "#FFB3BA"
DARK_PINK = "#FFB0C9"
LIGHT_PINK = "#FFF5F8"
RED = "#E63946"

# =====================================================
# EMOJIS DAS CARTAS
# =====================================================
ICONS = [
    "🌸", "🎀", "🧸", "🩷", "🦋", "🌙",
    "🍓", "🧁", "⭐", "🍀", "🐱", "💎",
    "🌈", "🦄", "🍭", "🌼", "🎵", "☁️"
]

# =====================================================
# FALAS DA MASCOTE CIRILLA (pra faixa na tela)
# =====================================================
FALAS_ACERTO = [
    "Isso! Você acertou um par! 💖",
    "Que incrível! ⭐",
    "Você é a melhor! 👑",
    "Mandou bem demais! 🌟",
]
FALAS_ERRO = [
    "Quase! Tenta outro par 💭",
    "Calma, você consegue! 🌸",
    "Respira e olha de novo 🦋",
]

# =====================================================
# NOMES DOS ARQUIVOS
# =====================================================
RANK_FILE = "ranking_kawaii.json"
PROGRESS_FILE = "progress_kawaii.json"
PERFIS_FILE = "perfis_kawaii.json"
SAVE_GAME_FILE = "jogo_salvo_kawaii.json"


# =====================================================
# 🧙‍♀️ MOLDE 1 — A JOGADORA
# =====================================================
class Jogadora:
    """Uma maga e seu progresso (nome, xp, nível, conquistas, stats)."""

    def __init__(self, nome="Convidada"):
        self.nome = nome
        self.xp = 0
        self.level = 1
        self.achievements = []
        self.stats = {
            "games_played": 0,
            "games_won": 0,
            "total_time": 0,
            "best_time": None
        }

    def para_dicionario(self):
        """📦 Vira dicionário pra salvar (o nome fica como chave no armário)."""
        return {
            "xp": self.xp,
            "level": self.level,
            "achievements": self.achievements,
            "stats": self.stats
        }

    def carregar_de(self, dados):
        """📖 Preenche a jogadora a partir de um dicionário salvo."""
        self.xp = dados.get("xp", 0)
        self.level = dados.get("level", 1)
        self.achievements = dados.get("achievements", [])
        self.stats = dados.get("stats", self.stats)

    def ganhar_xp(self, quantidade):
        """⭐ Soma XP, recalcula o nível e devolve True se subiu de nível."""
        nivel_antigo = self.level
        self.xp += quantidade
        self.level = self.xp // 100 + 1
        return self.level > nivel_antigo

    def desbloquear_conquista(self, texto):
        """🏆 Adiciona conquista nova e devolve True (ou False se já tinha)."""
        if texto not in self.achievements:
            self.achievements.append(texto)
            return True
        return False

    def titulo(self):
        """👑 Título conforme o nível: Aprendiz → Maga do Código → Arquimaga."""
        if self.level >= 6:
            return "Arquimaga 👑"
        elif self.level >= 3:
            return "Maga do Código 🔮"
        else:
            return "Aprendiz 🌱"


# =====================================================
# 👥 MOLDE 2 — O GERENCIADOR DE PERFIS
# =====================================================
class GerenciadorDePerfis:
    """Cuida de TODOS os perfis (o armário de gavetas). 👥"""

    def __init__(self):
        self.perfis = {}
        self.carregar()

    def carregar(self):
        """📖 Abre o arquivo de perfis (e migra o progresso antigo, se houver)."""
        if os.path.exists(PERFIS_FILE):
            try:
                with open(PERFIS_FILE, "r", encoding="utf-8") as f:
                    self.perfis = json.load(f)
            except:
                self.perfis = {}
        else:
            self.perfis = {}
            if os.path.exists(PROGRESS_FILE):
                try:
                    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                        antigo = json.load(f)
                    self.perfis["Convidada"] = antigo
                    self.salvar()
                except:
                    pass

    def salvar(self):
        """✍️ Grava o armário inteiro no arquivo."""
        with open(PERFIS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.perfis, f, ensure_ascii=False, indent=2)

    def nomes(self):
        """📋 Lista os nomes de todos os perfis."""
        return list(self.perfis.keys())

    def existe(self, nome):
        return nome in self.perfis

    def carregar_jogadora(self, nome):
        """🧙‍♀️ Monta uma Jogadora pronta a partir da gaveta 'nome'."""
        jogadora = Jogadora(nome)
        if nome in self.perfis:
            jogadora.carregar_de(self.perfis[nome])
        return jogadora

    def salvar_jogadora(self, jogadora):
        """💾 Guarda os dados da jogadora de volta na gaveta dela."""
        self.perfis[jogadora.nome] = jogadora.para_dicionario()
        self.salvar()

    def apagar(self, nome):
        """🗑️ Joga fora a gaveta de um perfil."""
        if nome in self.perfis:
            del self.perfis[nome]
            self.salvar()

    def resetar_todos(self):
        """♻️ Esvazia o armário inteiro e apaga o arquivo."""
        self.perfis = {}
        if os.path.exists(PERFIS_FILE):
            os.remove(PERFIS_FILE)


# =====================================================
# 🏆 MOLDE 3 — O RANKING
# =====================================================
class Ranking:
    """A tabela dos melhores resultados (top 10). 🏆"""

    def __init__(self):
        self.lista = []
        self.carregar()

    def carregar(self):
        if os.path.exists(RANK_FILE):
            try:
                with open(RANK_FILE, "r", encoding="utf-8") as f:
                    self.lista = json.load(f)
            except:
                self.lista = []
        else:
            self.lista = []

    def salvar(self):
        with open(RANK_FILE, "w", encoding="utf-8") as f:
            json.dump(self.lista, f, ensure_ascii=False, indent=2)

    def adicionar(self, nome, score, tempo, nivel):
        novo = {"name": nome, "score": score, "time": tempo, "level": nivel}
        self.lista.append(novo)
        self.lista.sort(key=lambda x: x["score"], reverse=True)
        self.lista = self.lista[:10]
        self.salvar()

    def esta_vazio(self):
        """🆕 Diz se o ranking está vazio (sem nenhum resultado)."""
        return len(self.lista) == 0

    def resetar(self):
        """♻️ Esvazia o ranking e apaga o arquivo."""
        self.lista = []
        if os.path.exists(RANK_FILE):
            os.remove(RANK_FILE)


# =====================================================
# 🎮 MOLDE 4 — O JOGO
# =====================================================
class KawaiiMemoryGame:
    """O jogo inteiro. Contém um gerenciador, um ranking e a jogadora ativa. 🪆"""

    # -------------------------------------------------
    # NASCIMENTO E FERRAMENTAS BÁSICAS
    # -------------------------------------------------

    def __init__(self, root):
        self.root = root
        self.root.title("🎀 Memory Game Deluxe Kawaii RPG v8.0 (POO)")
        self.root.geometry("1200x900")
        self.root.configure(bg=BG)

        self.gerenciador = GerenciadorDePerfis()
        self.ranking = Ranking()
        self.jogadora = None

        self.diff = tk.StringVar(value="Fácil")
        self.novo_perfil = tk.StringVar()
        self.tempo_acumulado = 0
        self.start_time = None  # cronômetro desligado

        self.tela_perfis()

    def clear(self):
        """🧹 Apaga tudo da tela."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def _botao_voltar(self, parent, destino):
        """🧭 Cria SEMPRE o mesmo botão "Voltar" (idêntico em todas as telas)."""
        tk.Button(
            parent, text="🔙 Voltar",
            font=("Arial", 12, "bold"), bg=BLUE, fg="white", width=20,
            command=destino
        ).pack(pady=20)

    def _subtitulo_perfil(self, parent):
        """💡 AJUDA VISUAL: mostra qual perfil está ativo numa telinha."""
        if self.jogadora is not None:
            tk.Label(
                parent, text=f"👤 Perfil ativo: {self.jogadora.nome}",
                font=("Arial", 11, "italic"), bg=BG, fg="#7B2CBF"
            ).pack(pady=(0, 8))

    # -------------------------------------------------
    # ATALHOS PRA FALAR COM A JOGADORA ATIVA
    # -------------------------------------------------

    def _ganhar_xp(self, quantidade):
        """Dá XP, guarda no perfil e (só se subir de nível) mostra pop-up."""
        subiu = self.jogadora.ganhar_xp(quantidade)
        self.gerenciador.salvar_jogadora(self.jogadora)
        if subiu:
            messagebox.showinfo(
                "✨ LEVEL UP!",
                f"Parabéns, {self.jogadora.nome}! Você chegou ao nível {self.jogadora.level}!\n"
                f"Agora você é: {self.jogadora.titulo()} 🎉"
            )

    def _desbloquear(self, texto):
        """Desbloqueia conquista, guarda e (só se for nova) mostra pop-up."""
        if self.jogadora.desbloquear_conquista(texto):
            self.gerenciador.salvar_jogadora(self.jogadora)
            messagebox.showinfo("🏆 CONQUISTA!", texto)

    # -------------------------------------------------
    # TELA DE PERFIS
    # -------------------------------------------------

    def tela_perfis(self):
        """👥 Escolher / criar / apagar perfis."""
        self.start_time = None
        self.clear()
        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame, text="👥 PERFIS DAS FEITICEIRAS 🌸",
            font=("Comic Sans MS", 30, "bold"), bg=BG, fg="#A4133C"
        ).pack(pady=(25, 5))
        tk.Label(
            main_frame, text="Escolha um perfil pra jogar, ou crie um novo:",
            font=("Arial", 13), bg=BG, fg="#7B2CBF"
        ).pack(pady=(0, 15))

        nomes = self.gerenciador.nomes()

        if not nomes:
            tk.Label(
                main_frame, text="Nenhum perfil ainda... crie o primeiro! 🌱",
                font=("Arial", 13, "italic"), bg=BG, fg="#999999"
            ).pack(pady=10)
        else:
            lista_frame = tk.Frame(main_frame, bg=BG)
            lista_frame.pack(pady=5)
            for nome in nomes:
                jog = self.gerenciador.carregar_jogadora(nome)
                linha = tk.Frame(lista_frame, bg=BG)
                linha.pack(pady=4)
                tk.Button(
                    linha,
                    text=f"👤 {nome}  —  Nível {jog.level}  —  {jog.titulo()}",
                    font=("Arial", 12, "bold"), bg=LILAC, fg="white", width=34,
                    command=lambda n=nome: self.escolher_perfil(n)
                ).pack(side="left", padx=5)
                tk.Button(
                    linha, text="🗑️",
                    font=("Arial", 12, "bold"), bg=RED, fg="white", width=4,
                    command=lambda n=nome: self.apagar_perfil(n)
                ).pack(side="left")

        # ----- CRIAR NOVO PERFIL -----
        criar_frame = tk.Frame(main_frame, bg=BG)
        criar_frame.pack(pady=(20, 5))
        tk.Label(
            criar_frame, text="➕ Nome do novo perfil:",
            font=("Arial", 13, "bold"), bg=BG, fg="#7B2CBF"
        ).pack(side="left", padx=5)
        tk.Entry(
            criar_frame, font=("Arial", 14), width=16, textvariable=self.novo_perfil
        ).pack(side="left", padx=5)
        tk.Button(
            criar_frame, text="Criar",
            font=("Arial", 12, "bold"), bg=MINT, fg="#2D3142", width=8,
            command=self.criar_perfil
        ).pack(side="left", padx=5)

        # ----- BOTÕES DE BAIXO -----
        botoes_frame = tk.Frame(main_frame, bg=BG)
        botoes_frame.pack(pady=25)
        if nomes:
            tk.Button(
                botoes_frame, text="📊 COMPARAR PERFIS",
                font=("Arial", 13, "bold"), bg=BLUE, fg="white", width=20,
                command=self.comparar_perfis
            ).pack(pady=6)
            tk.Button(
                botoes_frame, text="🏆 RANKING GERAL",
                font=("Arial", 12, "bold"), bg=YELLOW, fg="#2D3142", width=20,
                command=self.show_ranking
            ).pack(pady=4)
        tk.Button(
            botoes_frame, text="♻️ RESETAR TUDO",
            font=("Arial", 12, "bold"), bg=RED, fg="white", width=20,
            command=self.resetar_tudo
        ).pack(pady=(12, 4))
        tk.Button(
            botoes_frame, text="🚪 SAIR",
            font=("Arial", 12, "bold"), bg=CORAL, fg="white", width=20,
            command=self.sair_do_jogo
        ).pack(pady=4)

    def criar_perfil(self):
        """➕ Cria um perfil novo a partir do nome digitado."""
        nome = self.novo_perfil.get().strip()
        if nome == "":
            messagebox.showinfo("Ops!", "Digite um nome pro perfil. 🌸")
            return
        if self.gerenciador.existe(nome):
            messagebox.showinfo("Ops!", f"Já existe um perfil '{nome}'. 💭")
            return
        nova = Jogadora(nome)
        self.gerenciador.salvar_jogadora(nova)
        self.novo_perfil.set("")
        self.escolher_perfil(nome)

    def escolher_perfil(self, nome):
        """✅ Define o perfil ativo e vai pra tela inicial do jogo."""
        self.jogadora = self.gerenciador.carregar_jogadora(nome)
        self.home()

    def apagar_perfil(self, nome):
        """🗑️ Apaga um perfil (com confirmação)."""
        resposta = messagebox.askyesno(
            "Apagar perfil",
            f"Apagar o perfil '{nome}' para sempre? 🌙\n"
            "Todo o progresso dele será perdido."
        )
        if resposta:
            self.gerenciador.apagar(nome)
            if self.jogadora is not None and self.jogadora.nome == nome:
                self.jogadora = None
            self.tela_perfis()

    # -------------------------------------------------
    # TELA DE COMPARAÇÃO
    # -------------------------------------------------

    def comparar_perfis(self):
        """📊 Todos os perfis lado a lado, do maior XP pro menor."""
        self.clear()
        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame, text="📊 COMPARAR PERFIS 📊",
            font=("Comic Sans MS", 30, "bold"), bg=BG, fg="#A4133C"
        ).pack(pady=20)

        nomes = self.gerenciador.nomes()
        if not nomes:
            tk.Label(
                main_frame, text="Nenhum perfil pra comparar ainda... 🌱",
                font=("Arial", 14), bg=BG, fg="#7B2CBF"
            ).pack(pady=40)
        else:
            jogadoras = [self.gerenciador.carregar_jogadora(n) for n in nomes]
            jogadoras.sort(key=lambda j: j.xp, reverse=True)

            tabela = tk.Frame(main_frame, bg=LIGHT_PINK, relief="raised", bd=3)
            tabela.pack(padx=30, pady=15, fill="both")
            medalhas = {0: "🥇", 1: "🥈", 2: "🥉"}
            for pos, jog in enumerate(jogadoras):
                medalha = medalhas.get(pos, f"{pos+1}º")
                cor = YELLOW if pos == 0 else LIGHT_PINK
                texto = (
                    f"{medalha}  👤 {jog.nome}   |   {jog.titulo()}   |   "
                    f"⭐ Nível {jog.level}   |   💜 XP {jog.xp}   |   "
                    f"🏆 {jog.stats['games_won']} vitórias"
                )
                tk.Label(
                    tabela, text=texto,
                    font=("Arial", 12, "bold"), bg=cor, fg="#2D3142"
                ).pack(padx=10, pady=6, fill="x")

        self._botao_voltar(main_frame, self.tela_perfis)

    # -------------------------------------------------
    # RESETAR TUDO / RESETAR RANKING / SAIR
    # -------------------------------------------------

    def resetar_tudo(self):
        """♻️ Apaga TODOS os perfis + ranking + partida salva."""
        resposta = messagebox.askyesno(
            "♻️ Resetar tudo",
            "Isso vai APAGAR para sempre:\n\n"
            "• TODOS os perfis 👥\n"
            "• O ranking 🥇\n"
            "• A partida salva 💾\n\n"
            "Tem certeza, feiticeira? 🌙"
        )
        if resposta:
            self.gerenciador.resetar_todos()
            self.ranking.resetar()
            self._apagar_jogo_salvo()
            self.jogadora = None
            messagebox.showinfo("✨ Tudo limpo!", "Pronto! A Academia recomeçou do zero. 🌱")
            self.tela_perfis()

    def resetar_ranking(self):
        """
        🆕 ♻️ Apaga SÓ o ranking (top 10). Os perfis ficam intactos!

        Detalhe importante: se o ranking JÁ estiver vazio, a gente
        avisa com carinho em vez de fazer um reset "à toa". 🌙
        Pra isso usamos o método esta_vazio() do molde Ranking.
        """
        if self.ranking.esta_vazio():
            messagebox.showinfo(
                "Ranking vazio",
                "O ranking já está vazinho — não tem nada pra apagar ainda. 🌱\n"
                "Vença uma partida pra aparecer aqui! 🏆"
            )
            return

        resposta = messagebox.askyesno(
            "♻️ Resetar ranking",
            "Apagar TODO o ranking (top 10)?\n\n"
            "Só o ranking some — os perfis e o progresso continuam intactos. 🥇"
        )
        if resposta:
            self.ranking.resetar()
            messagebox.showinfo("✨ Pronto!", "Ranking zerado! Hora de uma nova disputa. 🌸")
            self.show_ranking()  # recarrega a tela já vazia

    def sair_do_jogo(self):
        """🚪 Fecha o jogo — mas só DEPOIS de confirmar."""
        resposta = messagebox.askyesno(
            "Sair do jogo",
            "Quer mesmo fechar a Academia de Magia? 🌙✨"
        )
        if resposta:
            self.root.destroy()

    # -------------------------------------------------
    # GUARDAR / RECUPERAR A PARTIDA ATUAL
    # -------------------------------------------------

    def existe_jogo_salvo(self):
        return os.path.exists(SAVE_GAME_FILE)

    def _ler_jogo_salvo(self):
        try:
            with open(SAVE_GAME_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None

    def _apagar_jogo_salvo(self):
        if self.existe_jogo_salvo():
            os.remove(SAVE_GAME_FILE)

    def salvar_jogo(self):
        """💾 Guarda a partida atual no baú."""
        if self.start_time is not None:
            tempo_total = self.tempo_acumulado + int(time.time() - self.start_time)
        else:
            tempo_total = self.tempo_acumulado

        estado = {
            "valores": self.values,
            "encontradas": list(self.matched),
            "linhas": self.rows,
            "colunas": self.cols,
            "pares": self.pairs,
            "dificuldade": self.diff.get(),
            "nome": self.jogadora.nome,
            "tempo": tempo_total
        }
        with open(SAVE_GAME_FILE, "w", encoding="utf-8") as f:
            json.dump(estado, f, ensure_ascii=False, indent=2)

        self.start_time = None
        messagebox.showinfo(
            "💾 Jogo salvo!",
            "Sua partida foi guardada no grimório! ✨\n\n"
            "Quando voltar, é só clicar em '▶️ Continuar Jogo'. 🌸"
        )
        self.home()

    def continuar_jogo(self):
        """▶️ Recomeça a partida de onde parou."""
        if not self.existe_jogo_salvo():
            messagebox.showinfo("Ops!", "Não encontrei nenhum jogo salvo. 🌙")
            self.home()
            return
        estado = self._ler_jogo_salvo()
        if estado is None:
            messagebox.showinfo("Ops!", "O jogo salvo está ilegível. 😢")
            self.home()
            return
        nome_salvo = estado.get("nome")
        if nome_salvo and self.gerenciador.existe(nome_salvo):
            self.jogadora = self.gerenciador.carregar_jogadora(nome_salvo)
        self.new_game(estado_salvo=estado)

    # -------------------------------------------------
    # 🛡️ SEGURANÇA: sair/recomeçar a partida com aviso
    # -------------------------------------------------

    def voltar_da_partida(self):
        """🛡️ "Voltar" durante o jogo → pergunta antes de perder a partida."""
        resposta = messagebox.askyesno(
            "Voltar pro início",
            "Se você voltar agora, perde esta partida (a não ser que salve antes).\n"
            "Quer mesmo voltar? 🌙"
        )
        if resposta:
            self.home()

    def reiniciar_partida(self):
        """🛡️ "Novo Jogo" durante o jogo → pergunta antes de recomeçar."""
        resposta = messagebox.askyesno(
            "Novo jogo",
            "Começar de novo vai perder a partida atual. Tem certeza? 🔄"
        )
        if resposta:
            self.new_game()

    # -------------------------------------------------
    # TELA INICIAL (do perfil ativo)
    # -------------------------------------------------

    def home(self):
        """🏠 Tela inicial da maga que está logada."""
        if self.jogadora is None:
            self.tela_perfis()
            return

        self.start_time = None
        self.clear()
        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill="both", expand=True)

        # ----- TÍTULO -----
        tk.Label(
            main_frame, text="🎀 Memory Game Deluxe 🌸",
            font=("Comic Sans MS", 34, "bold"), bg=BG, fg="#A4133C"
        ).pack(pady=(18, 6))

        # ----- PERFIL ATIVO + NÍVEL (destacado) -----
        nivel_frame = tk.Frame(main_frame, bg=PURPLE, relief="raised", bd=3)
        nivel_frame.pack(padx=30, pady=6)
        tk.Label(
            nivel_frame, text=f"👤 {self.jogadora.nome}",
            font=("Comic Sans MS", 18, "bold"), bg=PURPLE, fg="#4C0080"
        ).pack(padx=20, pady=(8, 0))
        tk.Label(
            nivel_frame,
            text=f"👑 Nível Geral: {self.jogadora.level}  —  {self.jogadora.titulo()}",
            font=("Arial", 13, "bold"), bg=PURPLE, fg="#7B2CBF"
        ).pack(padx=20, pady=(0, 8))

        # ----- MASCOTE -----
        mascot_text = random.choice([
            "🎀 Pronta pra treinar a memória?",
            "✨ Bora subir de nível?",
            "🌸 Você consegue, feiticeira!"
        ])
        mascot_frame = tk.Frame(main_frame, bg=PEACH, relief="raised", bd=2)
        mascot_frame.pack(padx=30, pady=6)
        tk.Label(
            mascot_frame, text=f"🦋 Cirilla: {mascot_text}",
            font=("Arial", 11, "italic"), bg=PEACH, fg="#2D3142"
        ).pack(padx=10, pady=6)

        # ----- ESTATÍSTICAS -----
        stats_frame = tk.Frame(main_frame, bg=LILAC, relief="raised", bd=2)
        stats_frame.pack(padx=30, pady=6)
        stats_text = (
            f"💜 XP: {self.jogadora.xp} | "
            f"🎮 Jogos: {self.jogadora.stats['games_played']} | "
            f"🏆 Vitórias: {self.jogadora.stats['games_won']}"
        )
        tk.Label(
            stats_frame, text=stats_text,
            font=("Arial", 12, "bold"), bg=LILAC, fg="#4C0080"
        ).pack(padx=10, pady=8)

        # ----- DIFICULDADE -----
        tk.Label(
            main_frame, text="Escolha a dificuldade:",
            font=("Arial", 13, "bold"), bg=BG, fg="#7B2CBF"
        ).pack(pady=(10, 4))
        diff_frame = tk.Frame(main_frame, bg=BG)
        diff_frame.pack()
        for diff in ["Fácil", "Médio", "Difícil"]:
            tk.Radiobutton(
                diff_frame, text=diff, variable=self.diff, value=diff,
                font=("Arial", 12), bg=BG, activebackground=PINK
            ).pack(side="left", padx=10)

        # ----- BOTÕES AGRUPADOS POR FUNÇÃO -----
        button_frame = tk.Frame(main_frame, bg=BG)
        button_frame.pack(pady=10)

        # >>> Grupo JOGAR
        tk.Label(
            button_frame, text="▶️ Jogar",
            font=("Arial", 11, "bold"), bg=BG, fg="#A4133C"
        ).pack(pady=(0, 2))
        tk.Button(
            button_frame, text="🎮 JOGAR",
            font=("Arial", 14, "bold"), bg=PINK, fg="white", width=20,
            command=self.new_game
        ).pack(pady=3)
        if self.existe_jogo_salvo():
            tk.Button(
                button_frame, text="▶️ CONTINUAR JOGO",
                font=("Arial", 13, "bold"), bg=MINT, fg="#2D3142", width=20,
                command=self.continuar_jogo
            ).pack(pady=3)

        # >>> Grupo GERENCIAR
        tk.Label(
            button_frame, text="⚙️ Gerenciar",
            font=("Arial", 11, "bold"), bg=BG, fg="#A4133C"
        ).pack(pady=(10, 2))
        tk.Button(
            button_frame, text="📊 COMPARAR PERFIS",
            font=("Arial", 11, "bold"), bg=BLUE, fg="white", width=20,
            command=self.comparar_perfis
        ).pack(pady=2)
        tk.Button(
            button_frame, text="👑 MEU PERFIL",
            font=("Arial", 11, "bold"), bg=LILAC, fg="white", width=20,
            command=self.show_profile
        ).pack(pady=2)
        tk.Button(
            button_frame, text="🏆 RANKING",
            font=("Arial", 11, "bold"), bg=YELLOW, fg="#2D3142", width=20,
            command=self.show_ranking
        ).pack(pady=2)
        tk.Button(
            button_frame, text="⭐ CONQUISTAS",
            font=("Arial", 11, "bold"), bg=PEACH, fg="#2D3142", width=20,
            command=self.show_achievements
        ).pack(pady=2)
        tk.Button(
            button_frame, text="👥 TROCAR PERFIL",
            font=("Arial", 11, "bold"), bg=CORAL, fg="white", width=20,
            command=self.tela_perfis
        ).pack(pady=(8, 2))

    # -------------------------------------------------
    # TELA DE PERFIL / RANKING / CONQUISTAS
    # -------------------------------------------------

    def show_profile(self):
        """👑 Detalhe do perfil ATIVO."""
        self.clear()
        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame, text="👑 MEU PERFIL 👑",
            font=("Comic Sans MS", 32, "bold"), bg=BG, fg="#A4133C"
        ).pack(pady=20)

        profile_frame = tk.Frame(main_frame, bg=LIGHT_PINK, relief="raised", bd=3)
        profile_frame.pack(padx=30, pady=20, fill="both")
        profile_info = f"""
👤 Nome: {self.jogadora.nome}
👑 Título: {self.jogadora.titulo()}
⭐ Nível Geral: {self.jogadora.level}
💜 XP Total: {self.jogadora.xp}
🎮 Jogos Jogados: {self.jogadora.stats['games_played']}
🏆 Vitórias: {self.jogadora.stats['games_won']}
⏱️ Melhor Tempo: {self.jogadora.stats['best_time']}s (se houver)
🎀 Conquistas: {len(self.jogadora.achievements)}/10
        """
        tk.Label(
            profile_frame, text=profile_info, font=("Arial", 14),
            bg=LIGHT_PINK, fg="#2D3142", justify="left"
        ).pack(padx=20, pady=20)

        if self.jogadora.achievements:
            tk.Label(
                profile_frame, text="Suas Conquistas 🏆:",
                font=("Arial", 12, "bold"), bg=LIGHT_PINK, fg="#A4133C"
            ).pack()
            for conquista in self.jogadora.achievements:
                tk.Label(
                    profile_frame, text=f"  ✓ {conquista}",
                    font=("Arial", 11), bg=LIGHT_PINK, fg="#4C0080"
                ).pack()

        self._botao_voltar(main_frame, self.home)

    def show_ranking(self):
        """🏆 Top 10 com medalhas e cores (+ botão de resetar SÓ o ranking)."""
        self.clear()
        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame, text="🏆 RANKING TOP 10 🏆",
            font=("Comic Sans MS", 32, "bold"), bg=BG, fg="#A4133C"
        ).pack(pady=20)
        self._subtitulo_perfil(main_frame)

        lista = self.ranking.lista
        if not lista:
            tk.Label(
                main_frame,
                text="Sem dados de ranking ainda... Seja a primeira! 🌸",
                font=("Arial", 14), bg=BG, fg="#7B2CBF"
            ).pack(pady=50)
        else:
            rank_frame = tk.Frame(main_frame, bg=LIGHT_PINK, relief="raised", bd=3)
            rank_frame.pack(padx=30, pady=20, fill="both")
            medals = {0: "🥇", 1: "🥈", 2: "🥉"}
            for i, player in enumerate(lista[:10]):
                medal = medals.get(i, f"{i+1:2d}. ")
                if i == 0:
                    bg_color, fg_color = YELLOW, "#000000"
                elif i == 1:
                    bg_color, fg_color = PEACH, "#000000"
                elif i == 2:
                    bg_color, fg_color = CORAL, "#000000"
                else:
                    bg_color, fg_color = LIGHT_PINK, "#2D3142"
                tk.Label(
                    rank_frame,
                    text=f"{medal} {player['name']} — Score: {player['score']} — ⏱️ {player['time']}s",
                    font=("Arial", 12, "bold"), bg=bg_color, fg=fg_color
                ).pack(padx=10, pady=8, fill="x")

        # 🆕 Botão pra resetar SÓ o ranking (os perfis continuam intactos)
        tk.Button(
            main_frame, text="♻️ Resetar Ranking",
            font=("Arial", 11, "bold"), bg=RED, fg="white", width=20,
            command=self.resetar_ranking
        ).pack(pady=(10, 0))

        # Volta pra home (se há perfil ativo) ou pra tela de perfis
        destino = self.home if self.jogadora is not None else self.tela_perfis
        self._botao_voltar(main_frame, destino)

    def show_achievements(self):
        """⭐ Conquistas (✓ e 🔒) do perfil ativo."""
        self.clear()
        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame, text="⭐ CONQUISTAS ⭐",
            font=("Comic Sans MS", 32, "bold"), bg=BG, fg="#A4133C"
        ).pack(pady=20)
        self._subtitulo_perfil(main_frame)

        achiev_frame = tk.Frame(main_frame, bg=LIGHT_PINK, relief="raised", bd=3)
        achiev_frame.pack(padx=30, pady=20, fill="both")
        todas = [
            "Primeira Vitória 🏆", "Velocista ⚡", "Mestre da Memória 🧙‍♀️",
            "Campeã Fácil 🌸", "Campeã Médio 💜", "Campeã Difícil 🔥",
            "10 Vitórias 🎉", "Nivel 10 👑", "Perfecta 💯",
            "Speedrun Master ⚡⚡⚡"
        ]
        for conquista in todas:
            if conquista in self.jogadora.achievements:
                tk.Label(
                    achiev_frame, text=f"✓ {conquista}",
                    font=("Arial", 11, "bold"), bg="#FFD6A5", fg="#000000"
                ).pack(padx=10, pady=5, fill="x")
            else:
                tk.Label(
                    achiev_frame, text=f"🔒 {conquista}",
                    font=("Arial", 11), bg=LIGHT_PINK, fg="#999999"
                ).pack(padx=10, pady=5, fill="x")

        self._botao_voltar(main_frame, self.home)

    # -------------------------------------------------
    # A PARTIDA EM SI
    # -------------------------------------------------

    def difficulty_size(self):
        diffs = {"Fácil": (4, 4), "Médio": (4, 5), "Difícil": (6, 6)}
        return diffs[self.diff.get()]

    def new_game(self, estado_salvo=None):
        """🎮 Monta uma partida (nova OU continuação de um salvo)."""
        self.clear()

        if estado_salvo is None:
            self.jogadora.stats["games_played"] += 1
            self.gerenciador.salvar_jogadora(self.jogadora)
            rows, cols = self.difficulty_size()
            total = rows * cols
            pairs = total // 2
            icons = ICONS[:pairs]
            self.values = icons * 2
            random.shuffle(self.values)
            self.matched = set()
            self.tempo_acumulado = 0
        else:
            rows = estado_salvo["linhas"]
            cols = estado_salvo["colunas"]
            pairs = estado_salvo["pares"]
            total = rows * cols
            self.values = estado_salvo["valores"]
            self.matched = set(estado_salvo["encontradas"])
            self.tempo_acumulado = estado_salvo["tempo"]
            self.diff.set(estado_salvo["dificuldade"])

        self.first = None
        self.second = None
        self.buttons = []
        self.start_time = None
        self.rows = rows
        self.cols = cols
        self.pairs = pairs
        found_inicial = len(self.matched) // 2

        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill="both", expand=True)

        # ----- BARRA DE STATUS -----
        status_frame = tk.Frame(main_frame, bg=LILAC, relief="raised", bd=2)
        status_frame.pack(padx=20, pady=12, fill="x")
        tk.Label(
            status_frame,
            text=f"👤 {self.jogadora.nome} | 👑 Nível {self.jogadora.level} | 📊 {self.diff.get()}",
            font=("Arial", 12, "bold"), bg=LILAC, fg="#4C0080"
        ).pack(side="left", padx=10, pady=8)
        self.timer = tk.Label(
            status_frame, text="⏱️ 00:00",
            font=("Arial", 12, "bold"), bg=LILAC, fg="#7B2CBF"
        )
        self.timer.pack(side="right", padx=10, pady=8)
        self.progress = tk.Label(
            status_frame, text=f"🎁 Pares: {found_inicial}/{pairs}",
            font=("Arial", 12, "bold"), bg=LILAC, fg="#A4133C"
        )
        self.progress.pack(side="right", padx=10, pady=8)

        # ----- 💡 COMO JOGAR -----
        tk.Label(
            main_frame,
            text="💡 Vire duas cartas e tente formar pares iguais!",
            font=("Arial", 11, "italic"), bg=BG, fg="#7B2CBF"
        ).pack(pady=(6, 2))

        # ----- 🌊 FAIXA DA CIRILLA (fala sem pop-up!) -----
        self.mascote_label = tk.Label(
            main_frame, text="🦋 Cirilla: boa sorte! 💖",
            font=("Arial", 12, "bold"), bg=PEACH, fg="#2D3142",
            relief="raised", bd=2, width=46
        )
        self.mascote_label.pack(pady=(0, 8), ipady=4)

        # ----- TABULEIRO -----
        board_frame = tk.Frame(main_frame, bg=BG)
        board_frame.pack(padx=20, pady=6)
        colors = [PINK, BLUE, MINT, PEACH, YELLOW, LILAC, PURPLE, CORAL]
        for i in range(total):
            btn = tk.Button(
                board_frame, text="", width=6, height=3,
                font=("Arial", 24, "bold"),
                bg=colors[i % len(colors)],
                activebackground="#FFFFFF", relief="raised", bd=2,
                command=lambda x=i: self.flip(x)
            )
            btn.grid(row=i // cols, column=i % cols, padx=6, pady=6)
            self.buttons.append(btn)

        # ----- BOTÕES DE CONTROLE (🛡️ com aviso de segurança) -----
        control_frame = tk.Frame(main_frame, bg=BG)
        control_frame.pack(pady=12)
        tk.Button(
            control_frame, text="🔙 Voltar",
            font=("Arial", 10, "bold"), bg=BLUE, width=14,
            command=self.voltar_da_partida
        ).pack(side="left", padx=5)
        tk.Button(
            control_frame, text="🔄 Novo Jogo",
            font=("Arial", 10, "bold"), bg=PINK, width=14,
            command=self.reiniciar_partida
        ).pack(side="left", padx=5)
        tk.Button(
            control_frame, text="💾 Salvar e Sair",
            font=("Arial", 10, "bold"), bg=MINT, width=14,
            command=self.salvar_jogo
        ).pack(side="left", padx=5)
        tk.Button(
            control_frame, text="🚪 Sair",
            font=("Arial", 10, "bold"), bg=CORAL, width=14,
            command=self.sair_do_jogo
        ).pack(side="left", padx=5)

        if estado_salvo is None:
            self.show_cards_memory()
        else:
            self.restaurar_jogo()

    def restaurar_jogo(self):
        """♻️ Prepara o tabuleiro de um jogo CONTINUADO."""
        for i, btn in enumerate(self.buttons):
            if i in self.matched:
                btn.config(text=self.values[i], state="disabled", bg="#FDE2E4")
        self.mascote_label.config(text="🦋 Cirilla: bem-vinda de volta! 🌙", bg=PEACH)
        self.start_time = time.time()
        self.update_timer()

    def show_cards_memory(self):
        """🧠 Mostra as cartas e faz a CONTAGEM REGRESSIVA (sem pop-up)."""
        for i, btn in enumerate(self.buttons):
            btn.config(text=self.values[i], state="disabled")
        self.segundos_memorizar = 5
        self._contar_memorizacao()

    def _contar_memorizacao(self):
        """🌊 Conta 5…4…3… na faixa da Cirilla e depois esconde as cartas."""
        if not self.mascote_label.winfo_exists():
            return
        if self.segundos_memorizar > 0:
            self.mascote_label.config(
                text=f"🧠 Memorize! Escondendo em {self.segundos_memorizar}…",
                bg=YELLOW
            )
            self.segundos_memorizar -= 1
            self.root.after(1000, self._contar_memorizacao)
        else:
            self.mascote_label.config(text="🎮 Valendo! Encontre os pares! 💪", bg=PEACH)
            self.start_real_game()

    def start_real_game(self):
        """Esconde as cartas e liga o cronômetro."""
        for btn in self.buttons:
            btn.config(text="", state="normal")
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """🕐 Atualiza o cronômetro a cada 1 segundo (MM:SS)."""
        if not self.timer.winfo_exists():
            return
        if self.start_time and len(self.matched) < self.pairs * 2:
            elapsed = self.tempo_acumulado + int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer.config(text=f"⏱️ {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def flip(self, i):
        """🃏 Vira a carta de número i quando você clica."""
        if i in self.matched:
            return
        if self.first is not None and self.second is not None:
            return
        self.buttons[i].config(text=self.values[i])
        if self.first is None:
            self.first = i
            return
        if self.first == i:
            return
        self.second = i
        self.root.after(700, self.check_match)

    def check_match(self):
        """🔍 Confere se as duas cartas viradas são iguais."""
        a = self.first
        b = self.second

        if self.values[a] == self.values[b]:
            self.matched.add(a)
            self.matched.add(b)
            self.buttons[a].config(state="disabled", bg="#FDE2E4")
            self.buttons[b].config(state="disabled", bg="#FDE2E4")
            self.mascote_label.config(
                text=f"🦋 Cirilla: {random.choice(FALAS_ACERTO)}", bg=MINT
            )
            self._ganhar_xp(10)
        else:
            self.buttons[a].config(text="")
            self.buttons[b].config(text="")
            self.mascote_label.config(
                text=f"🦋 Cirilla: {random.choice(FALAS_ERRO)}", bg=PEACH
            )

        self.first = None
        self.second = None

        found = len(self.matched) // 2
        self.progress.config(text=f"🎁 Pares: {found}/{self.pairs}")

        if found == self.pairs:
            self.victory()

    def victory(self):
        """🎉 Final feliz (stats, XP, conquistas, ranking)."""
        elapsed = self.tempo_acumulado + int(time.time() - self.start_time)
        self.start_time = None

        self.jogadora.stats["games_won"] += 1
        self.jogadora.stats["total_time"] += elapsed
        if (self.jogadora.stats["best_time"] is None
                or elapsed < self.jogadora.stats["best_time"]):
            self.jogadora.stats["best_time"] = elapsed
        self.gerenciador.salvar_jogadora(self.jogadora)

        self._ganhar_xp(50)
        self._desbloquear("Primeira Vitória 🏆")
        if elapsed <= 60:
            self._desbloquear("Velocista ⚡")
        if self.diff.get() == "Difícil":
            self._desbloquear("Mestre da Memória 🧙‍♀️")
        if self.jogadora.stats["games_won"] == 10:
            self._desbloquear("10 Vitórias 🎉")

        self._apagar_jogo_salvo()
        self.ranking.adicionar(
            self.jogadora.nome, self.jogadora.xp, elapsed, self.jogadora.level
        )

        victory_text = f"""
🎉 PARABÉNS! 🎉

👤 {self.jogadora.nome}
👑 {self.jogadora.titulo()}
⏱️ Tempo: {elapsed}s
⭐ Nível Geral: {self.jogadora.level}
💜 XP Total: {self.jogadora.xp}

Que incrível! Você é incrível! 👑✨
        """
        messagebox.showinfo("VITÓRIA!", victory_text)
        self.home()


# =====================================================
# 🚀 LIGAR O JOGO
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    jogo = KawaiiMemoryGame(root)
    root.mainloop()   # ← só UMA vez! (na v7 tinha aparecido duplicad