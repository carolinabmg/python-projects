"""
🎀 MEMORY GAME DELUXE KAWAII RPG - VERSÃO 9.0
╔══════════════════════════════════════════════════════════════╗
║                    NOVIDADES DA v9.0                         ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ [2]  Classe FileManager — salvar/carregar centralizado   ║
║  ✅ [3]  Constantes de nível (XP_POR_NIVEL, XP_PROXIMO)     ║
║  ✅ [4]  Títulos em dicionário (TITULOS)                     ║
║  ✅ [5]  (pronto pra separar; imports já organizados)        ║
║  ✅ [6]  Enum Dificuldade                                    ║
║  ✅ [7]  Classe Carta                                        ║
║  ✅ [8]  XP com streak (bônus a cada 3 acertos seguidos)     ║
║  ✅ [9]  Barra de progresso de nível (XP visual)             ║
║  ✅ [10] Sons com pygame (fallback silencioso se ausente)    ║
║  ✅ [+]  Animação de virar carta (flash de cor)              ║
║  ✅ [+]  Histórico das últimas 5 partidas por perfil         ║
║  ✅ [+]  Temas de carta (Kawaii / Natureza / Comida / Espaço)║
╚══════════════════════════════════════════════════════════════╝
"""

# ── stdlib ──────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import messagebox
import random
import time
import json
import os
from enum import Enum
from datetime import datetime

# ── pygame (opcional — sons) ─────────────────────────────────────────────────
try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    PYGAME_OK = True
except Exception:
    PYGAME_OK = False


# ╔══════════════════════════════════════════════════════════════╗
# ║                     CONSTANTES GLOBAIS                       ║
# ╚══════════════════════════════════════════════════════════════╝

# ── Cores kawaii ────────────────────────────────────────────────
BG         = "#FFF0F6"
PINK       = "#FFB6C1"
LILAC      = "#D8B4FE"
BLUE       = "#BDE0FE"
MINT       = "#C7F9CC"
PEACH      = "#FFD6A5"
YELLOW     = "#FDFFB6"
PURPLE     = "#E0C3FC"
CORAL      = "#FFB3BA"
LIGHT_PINK = "#FFF5F8"
RED        = "#E63946"
DARK_TEXT  = "#2D3142"
VIOLET     = "#7B2CBF"
DEEP_RED   = "#A4133C"

# ── [3] Constantes de nível ─────────────────────────────────────
XP_POR_NIVEL   = 100          # XP necessário por nível
XP_ACERTO      = 10           # XP por par acertado
XP_VITORIA     = 50           # XP bônus ao vencer
XP_STREAK      = 20           # XP bônus a cada 3 acertos seguidos
STREAK_TRIGGER = 3            # quantos acertos seguidos ativam o bônus
MAX_HISTORICO  = 5            # últimas N partidas guardadas

# ── [4] Títulos em dicionário ───────────────────────────────────
TITULOS = {
    1: "Aprendiz 🌱",
    3: "Maga do Código 🔮",
    6: "Arquimaga 👑",
    10: "Lenda Kawaii ✨",
}

def titulo_para_nivel(level: int) -> str:
    """Devolve o título correspondente ao nível."""
    titulo = TITULOS[1]
    for limiar, nome in TITULOS.items():
        if level >= limiar:
            titulo = nome
    return titulo


# ── [6] Enum de dificuldade ─────────────────────────────────────
class Dificuldade(Enum):
    FACIL  = "Fácil"
    MEDIO  = "Médio"
    DIFICIL = "Difícil"

GRADE_DIFICULDADE = {
    Dificuldade.FACIL:   (4, 4),
    Dificuldade.MEDIO:   (4, 5),
    Dificuldade.DIFICIL: (6, 6),
}


# ── Temas de cartas ─────────────────────────────────────────────
TEMAS = {
    "Kawaii 🎀": [
        "🌸","🎀","🧸","🩷","🦋","🌙",
        "🍓","🧁","⭐","🍀","🐱","💎",
        "🌈","🦄","🍭","🌼","🎵","☁️"
    ],
    "Natureza 🌿": [
        "🌲","🌺","🍄","🐸","🌊","🦊",
        "🐝","🌻","🍁","🦜","🐚","🌍",
        "🦋","🌿","🐠","🍃","🌙","⛰️"
    ],
    "Comida 🍕": [
        "🍕","🍣","🍩","🌮","🍜","🍓",
        "🧁","🍦","🍇","🥑","🍋","🥐",
        "🍔","🍿","🥞","🍰","🥭","🫐"
    ],
    "Espaço 🚀": [
        "🚀","🌙","⭐","🪐","☄️","🌌",
        "👾","🛸","🔭","💫","🌠","🪨",
        "🌟","🌑","🪐","🛰️","🌞","🌀"
    ],
}

# ── Falas da mascote ────────────────────────────────────────────
FALAS_ACERTO = [
    "Isso! Você acertou um par! 💖",
    "Que incrível! ⭐",
    "Você é a melhor! 👑",
    "Mandou bem demais! 🌟",
]
FALAS_STREAK = [
    "🔥 STREAK x3! XP bônus pra você! ✨",
    "🔥 Três seguidos! Você tá voando! 💜",
    "🔥 Combo incrível! +20 XP! 🌟",
]
FALAS_ERRO = [
    "Quase! Tenta outro par 💭",
    "Calma, você consegue! 🌸",
    "Respira e olha de novo 🦋",
]

# ── Nomes dos arquivos ──────────────────────────────────────────
RANK_FILE      = "ranking_kawaii.json"
PERFIS_FILE    = "perfis_kawaii.json"
SAVE_GAME_FILE = "jogo_salvo_kawaii.json"


# ╔══════════════════════════════════════════════════════════════╗
# ║          [2]  CLASSE FileManager                             ║
# ╚══════════════════════════════════════════════════════════════╝

class FileManager:
    """
    Centraliza TODO acesso a disco.
    Nenhuma outra classe deve abrir arquivos diretamente.
    """

    @staticmethod
    def ler(caminho: str, padrao=None):
        """Lê JSON; devolve `padrao` se o arquivo não existir ou estiver corrompido."""
        if not os.path.exists(caminho):
            return padrao
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return padrao

    @staticmethod
    def gravar(caminho: str, dados) -> bool:
        """Grava dados como JSON. Devolve True em caso de sucesso."""
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    @staticmethod
    def apagar(caminho: str) -> bool:
        """Apaga o arquivo se existir."""
        if os.path.exists(caminho):
            try:
                os.remove(caminho)
                return True
            except Exception:
                return False
        return False

    @staticmethod
    def existe(caminho: str) -> bool:
        return os.path.exists(caminho)


# ╔══════════════════════════════════════════════════════════════╗
# ║          [7]  CLASSE Carta                                   ║
# ╚══════════════════════════════════════════════════════════════╝

class Carta:
    """
    Representa uma carta individual do tabuleiro.
    Guarda seu valor (emoji), índice e estado (virada / combinada).
    """

    def __init__(self, indice: int, valor: str):
        self.indice   = indice
        self.valor    = valor
        self.virada   = False   # visível no momento?
        self.combinada = False  # já foi pareada?

    def virar(self):
        self.virada = True

    def esconder(self):
        self.virada = False

    def marcar_combinada(self):
        self.combinada = True
        self.virada = True

    def __repr__(self):
        estado = "✓" if self.combinada else ("↑" if self.virada else "↓")
        return f"Carta({self.indice}, {self.valor}, {estado})"


# ╔══════════════════════════════════════════════════════════════╗
# ║          SOM                                                 ║
# ╚══════════════════════════════════════════════════════════════╝

class Som:
    """Gera sons sintéticos via pygame. Se pygame não estiver disponível, fica em silêncio."""

    @staticmethod
    def _gerar(freq: float, duracao: float, volume: float = 0.3):
        """Sintetiza uma onda senoidal e reproduz."""
        if not PYGAME_OK:
            return
        try:
            import numpy as np
            taxa   = 44100
            frames = int(taxa * duracao)
            t      = [i / taxa for i in range(frames)]
            onda   = bytes(
                int(32767 * volume * __import__("math").sin(2 * __import__("math").pi * freq * x))
                    .to_bytes(2, "little", signed=True)
                for x in t
            )
            som = pygame.mixer.Sound(buffer=onda)
            som.play()
        except Exception:
            pass

    @staticmethod
    def acerto():
        Som._gerar(880, 0.12)

    @staticmethod
    def erro():
        Som._gerar(220, 0.18)

    @staticmethod
    def streak():
        Som._gerar(1046, 0.20)

    @staticmethod
    def vitoria():
        for freq in [523, 659, 784, 1046]:
            Som._gerar(freq, 0.10)
            time.sleep(0.08)


# ╔══════════════════════════════════════════════════════════════╗
# ║          JOGADORA                                            ║
# ╚══════════════════════════════════════════════════════════════╝

class Jogadora:
    """Uma maga e todo seu progresso."""

    def __init__(self, nome="Convidada"):
        self.nome        = nome
        self.xp          = 0
        self.level       = 1
        self.achievements = []
        self.historico   = []          # últimas MAX_HISTORICO partidas
        self.stats = {
            "games_played": 0,
            "games_won":    0,
            "total_time":   0,
            "best_time":    None,
        }

    # ── serialização ────────────────────────────────────────────
    def para_dicionario(self) -> dict:
        return {
            "xp":           self.xp,
            "level":        self.level,
            "achievements": self.achievements,
            "stats":        self.stats,
            "historico":    self.historico,
        }

    def carregar_de(self, dados: dict):
        self.xp           = dados.get("xp", 0)
        self.level        = dados.get("level", 1)
        self.achievements = dados.get("achievements", [])
        self.stats        = dados.get("stats", self.stats)
        self.historico    = dados.get("historico", [])

    # ── XP e nível ──────────────────────────────────────────────
    def ganhar_xp(self, quantidade: int) -> bool:
        """Soma XP, recalcula nível. Devolve True se subiu de nível."""
        nivel_antigo = self.level
        self.xp     += quantidade
        self.level   = self.xp // XP_POR_NIVEL + 1
        return self.level > nivel_antigo

    def xp_no_nivel_atual(self) -> int:
        """XP acumulado DENTRO do nível atual (0 … XP_POR_NIVEL-1)."""
        return self.xp % XP_POR_NIVEL

    def xp_para_proximo(self) -> int:
        return XP_POR_NIVEL

    # ── conquistas ───────────────────────────────────────────────
    def desbloquear_conquista(self, texto: str) -> bool:
        if texto not in self.achievements:
            self.achievements.append(texto)
            return True
        return False

    # ── título ──────────────────────────────────────────────────
    def titulo(self) -> str:
        return titulo_para_nivel(self.level)

    # ── histórico ───────────────────────────────────────────────
    def registrar_partida(self, tempo: int, dificuldade: str, vitoria: bool):
        """Adiciona entrada no histórico (mantém últimas MAX_HISTORICO)."""
        entrada = {
            "data":        datetime.now().strftime("%d/%m/%Y %H:%M"),
            "tempo":       tempo,
            "dificuldade": dificuldade,
            "vitoria":     vitoria,
        }
        self.historico.insert(0, entrada)
        self.historico = self.historico[:MAX_HISTORICO]


# ╔══════════════════════════════════════════════════════════════╗
# ║          GERENCIADOR DE PERFIS                               ║
# ╚══════════════════════════════════════════════════════════════╝

class GerenciadorDePerfis:
    """Cuida de TODOS os perfis usando FileManager."""

    def __init__(self):
        self.perfis: dict = {}
        self.carregar()

    def carregar(self):
        self.perfis = FileManager.ler(PERFIS_FILE, padrao={})

    def salvar(self):
        FileManager.gravar(PERFIS_FILE, self.perfis)

    def nomes(self) -> list:
        return list(self.perfis.keys())

    def existe(self, nome: str) -> bool:
        return nome in self.perfis

    def carregar_jogadora(self, nome: str) -> Jogadora:
        jog = Jogadora(nome)
        if nome in self.perfis:
            jog.carregar_de(self.perfis[nome])
        return jog

    def salvar_jogadora(self, jogadora: Jogadora):
        self.perfis[jogadora.nome] = jogadora.para_dicionario()
        self.salvar()

    def apagar(self, nome: str):
        if nome in self.perfis:
            del self.perfis[nome]
            self.salvar()

    def resetar_todos(self):
        self.perfis = {}
        FileManager.apagar(PERFIS_FILE)


# ╔══════════════════════════════════════════════════════════════╗
# ║          RANKING                                             ║
# ╚══════════════════════════════════════════════════════════════╝

class Ranking:
    """Top 10 resultados."""

    def __init__(self):
        self.lista: list = []
        self.carregar()

    def carregar(self):
        self.lista = FileManager.ler(RANK_FILE, padrao=[])

    def salvar(self):
        FileManager.gravar(RANK_FILE, self.lista)

    def adicionar(self, nome: str, score: int, tempo: int, nivel: int):
        self.lista.append({"name": nome, "score": score, "time": tempo, "level": nivel})
        self.lista.sort(key=lambda x: x["score"], reverse=True)
        self.lista = self.lista[:10]
        self.salvar()

    def esta_vazio(self) -> bool:
        return len(self.lista) == 0

    def resetar(self):
        self.lista = []
        FileManager.apagar(RANK_FILE)


# ╔══════════════════════════════════════════════════════════════╗
# ║          JOGO PRINCIPAL                                      ║
# ╚══════════════════════════════════════════════════════════════╝

class KawaiiMemoryGame:

    # ── inicialização ────────────────────────────────────────────
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎀 Memory Game Deluxe Kawaii RPG v9.0")
        self.root.geometry("1200x950")
        self.root.configure(bg=BG)

        self.gerenciador    = GerenciadorDePerfis()
        self.ranking        = Ranking()
        self.jogadora: Jogadora | None = None

        # controles de jogo
        self.diff        = tk.StringVar(value=Dificuldade.FACIL.value)
        self.tema_atual  = tk.StringVar(value="Kawaii 🎀")
        self.novo_perfil = tk.StringVar()

        self.tempo_acumulado = 0
        self.start_time      = None
        self.streak          = 0      # acertos seguidos

        # cartas (lista de objetos Carta)
        self.cartas: list[Carta] = []
        self.primeira: Carta | None = None
        self.segunda:  Carta | None = None

        self.tela_perfis()

    # ── utilitários de tela ──────────────────────────────────────
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _botao_voltar(self, parent, destino):
        tk.Button(
            parent, text="🔙 Voltar",
            font=("Arial", 12, "bold"), bg=BLUE, fg="white", width=20,
            command=destino
        ).pack(pady=20)

    def _subtitulo_perfil(self, parent):
        if self.jogadora:
            tk.Label(
                parent,
                text=f"👤 Perfil ativo: {self.jogadora.nome}",
                font=("Arial", 11, "italic"), bg=BG, fg=VIOLET
            ).pack(pady=(0, 8))

    # ── [9] Barra de progresso de XP ────────────────────────────
    def _barra_xp(self, parent):
        """Desenha a barra de progresso de nível da jogadora ativa."""
        if not self.jogadora:
            return
        xp_atual  = self.jogadora.xp_no_nivel_atual()
        xp_max    = self.jogadora.xp_para_proximo()
        pct       = xp_atual / xp_max

        frame = tk.Frame(parent, bg=BG)
        frame.pack(pady=(4, 8))

        tk.Label(
            frame,
            text=f"⭐ Nível {self.jogadora.level} — {xp_atual}/{xp_max} XP",
            font=("Arial", 10, "bold"), bg=BG, fg=VIOLET
        ).pack()

        canvas = tk.Canvas(frame, width=400, height=18, bg="#E8D5F5",
                           highlightthickness=1, highlightbackground=LILAC)
        canvas.pack()
        canvas.create_rectangle(0, 0, int(400 * pct), 18, fill=LILAC, outline="")
        canvas.create_text(200, 9, text=f"{int(pct*100)}%",
                           font=("Arial", 9, "bold"), fill=DARK_TEXT)

    # ── atalhos jogadora ─────────────────────────────────────────
    def _ganhar_xp(self, qtd: int):
        subiu = self.jogadora.ganhar_xp(qtd)
        self.gerenciador.salvar_jogadora(self.jogadora)
        if subiu:
            messagebox.showinfo(
                "✨ LEVEL UP!",
                f"Parabéns, {self.jogadora.nome}!\n"
                f"Você chegou ao nível {self.jogadora.level}!\n"
                f"Agora você é: {self.jogadora.titulo()} 🎉"
            )

    def _desbloquear(self, texto: str):
        if self.jogadora.desbloquear_conquista(texto):
            self.gerenciador.salvar_jogadora(self.jogadora)
            messagebox.showinfo("🏆 CONQUISTA!", texto)

    # ─────────────────────────────────────────────────────────────
    # TELA DE PERFIS
    # ─────────────────────────────────────────────────────────────
    def tela_perfis(self):
        self.start_time = None
        self.clear()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)

        tk.Label(main, text="👥 PERFIS DAS FEITICEIRAS 🌸",
                 font=("Comic Sans MS", 28, "bold"), bg=BG, fg=DEEP_RED).pack(pady=(25, 5))
        tk.Label(main, text="Escolha um perfil ou crie um novo:",
                 font=("Arial", 13), bg=BG, fg=VIOLET).pack(pady=(0, 12))

        nomes = self.gerenciador.nomes()
        if not nomes:
            tk.Label(main, text="Nenhum perfil ainda… crie o primeiro! 🌱",
                     font=("Arial", 13, "italic"), bg=BG, fg="#999999").pack(pady=10)
        else:
            lista = tk.Frame(main, bg=BG)
            lista.pack(pady=4)
            for nome in nomes:
                jog  = self.gerenciador.carregar_jogadora(nome)
                linha = tk.Frame(lista, bg=BG)
                linha.pack(pady=4)
                tk.Button(
                    linha,
                    text=f"👤 {nome}  —  Nível {jog.level}  —  {jog.titulo()}",
                    font=("Arial", 12, "bold"), bg=LILAC, fg="white", width=36,
                    command=lambda n=nome: self.escolher_perfil(n)
                ).pack(side="left", padx=5)
                tk.Button(
                    linha, text="🗑️",
                    font=("Arial", 12, "bold"), bg=RED, fg="white", width=4,
                    command=lambda n=nome: self.apagar_perfil(n)
                ).pack(side="left")

        # criar novo perfil
        criar = tk.Frame(main, bg=BG)
        criar.pack(pady=(18, 5))
        tk.Label(criar, text="➕ Nome do novo perfil:",
                 font=("Arial", 13, "bold"), bg=BG, fg=VIOLET).pack(side="left", padx=5)
        tk.Entry(criar, font=("Arial", 14), width=16,
                 textvariable=self.novo_perfil).pack(side="left", padx=5)
        tk.Button(criar, text="Criar",
                  font=("Arial", 12, "bold"), bg=MINT, fg=DARK_TEXT, width=8,
                  command=self.criar_perfil).pack(side="left", padx=5)

        botoes = tk.Frame(main, bg=BG)
        botoes.pack(pady=20)
        if nomes:
            tk.Button(botoes, text="📊 COMPARAR PERFIS",
                      font=("Arial", 13, "bold"), bg=BLUE, fg="white", width=22,
                      command=self.comparar_perfis).pack(pady=5)
            tk.Button(botoes, text="🏆 RANKING GERAL",
                      font=("Arial", 12, "bold"), bg=YELLOW, fg=DARK_TEXT, width=22,
                      command=self.show_ranking).pack(pady=4)
        tk.Button(botoes, text="♻️ RESETAR TUDO",
                  font=("Arial", 12, "bold"), bg=RED, fg="white", width=22,
                  command=self.resetar_tudo).pack(pady=(10, 4))
        tk.Button(botoes, text="🚪 SAIR",
                  font=("Arial", 12, "bold"), bg=CORAL, fg="white", width=22,
                  command=self.sair_do_jogo).pack(pady=4)

    def criar_perfil(self):
        nome = self.novo_perfil.get().strip()
        if not nome:
            messagebox.showinfo("Ops!", "Digite um nome pro perfil. 🌸")
            return
        if self.gerenciador.existe(nome):
            messagebox.showinfo("Ops!", f"Já existe um perfil '{nome}'. 💭")
            return
        self.gerenciador.salvar_jogadora(Jogadora(nome))
        self.novo_perfil.set("")
        self.escolher_perfil(nome)

    def escolher_perfil(self, nome: str):
        self.jogadora = self.gerenciador.carregar_jogadora(nome)
        self.home()

    def apagar_perfil(self, nome: str):
        if messagebox.askyesno("Apagar perfil",
                               f"Apagar '{nome}' para sempre? 🌙\nTodo o progresso será perdido."):
            self.gerenciador.apagar(nome)
            if self.jogadora and self.jogadora.nome == nome:
                self.jogadora = None
            self.tela_perfis()

    # ─────────────────────────────────────────────────────────────
    # COMPARAR PERFIS
    # ─────────────────────────────────────────────────────────────
    def comparar_perfis(self):
        self.clear()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="📊 COMPARAR PERFIS 📊",
                 font=("Comic Sans MS", 28, "bold"), bg=BG, fg=DEEP_RED).pack(pady=20)

        nomes = self.gerenciador.nomes()
        if not nomes:
            tk.Label(main, text="Nenhum perfil pra comparar ainda… 🌱",
                     font=("Arial", 14), bg=BG, fg=VIOLET).pack(pady=40)
        else:
            jogadoras = sorted(
                [self.gerenciador.carregar_jogadora(n) for n in nomes],
                key=lambda j: j.xp, reverse=True
            )
            tabela = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
            tabela.pack(padx=30, pady=15, fill="both")
            medalhas = {0: "🥇", 1: "🥈", 2: "🥉"}
            for pos, jog in enumerate(jogadoras):
                cor   = YELLOW if pos == 0 else LIGHT_PINK
                texto = (
                    f"{medalhas.get(pos, f'{pos+1}º')}  👤 {jog.nome}  |  "
                    f"{jog.titulo()}  |  ⭐ Nível {jog.level}  |  "
                    f"💜 XP {jog.xp}  |  🏆 {jog.stats['games_won']} vitórias"
                )
                tk.Label(tabela, text=texto,
                         font=("Arial", 12, "bold"), bg=cor, fg=DARK_TEXT).pack(
                    padx=10, pady=6, fill="x")

        self._botao_voltar(main, self.tela_perfis)

    # ─────────────────────────────────────────────────────────────
    # RESETAR
    # ─────────────────────────────────────────────────────────────
    def resetar_tudo(self):
        if messagebox.askyesno("♻️ Resetar tudo",
                               "Isso vai APAGAR para sempre:\n\n"
                               "• TODOS os perfis 👥\n• O ranking 🥇\n• A partida salva 💾\n\n"
                               "Tem certeza, feiticeira? 🌙"):
            self.gerenciador.resetar_todos()
            self.ranking.resetar()
            FileManager.apagar(SAVE_GAME_FILE)
            self.jogadora = None
            messagebox.showinfo("✨ Tudo limpo!", "A Academia recomeçou do zero. 🌱")
            self.tela_perfis()

    def resetar_ranking(self):
        if self.ranking.esta_vazio():
            messagebox.showinfo("Ranking vazio",
                                "O ranking já está vazio — vença uma partida primeiro! 🌸")
            return
        if messagebox.askyesno("♻️ Resetar ranking",
                               "Apagar todo o ranking (top 10)?\nOs perfis continuam intactos."):
            self.ranking.resetar()
            messagebox.showinfo("✨ Pronto!", "Ranking zerado! Nova disputa começa agora. 🌸")
            self.show_ranking()

    def sair_do_jogo(self):
        if messagebox.askyesno("Sair", "Quer mesmo fechar a Academia de Magia? 🌙✨"):
            self.root.destroy()

    # ─────────────────────────────────────────────────────────────
    # HOME
    # ─────────────────────────────────────────────────────────────
    def home(self):
        if not self.jogadora:
            self.tela_perfis()
            return
        self.start_time = None
        self.clear()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)

        tk.Label(main, text="🎀 Memory Game Deluxe 🌸",
                 font=("Comic Sans MS", 32, "bold"), bg=BG, fg=DEEP_RED).pack(pady=(16, 4))

        # perfil + título
        nivel_frame = tk.Frame(main, bg=PURPLE, relief="raised", bd=3)
        nivel_frame.pack(padx=30, pady=4)
        tk.Label(nivel_frame, text=f"👤 {self.jogadora.nome}",
                 font=("Comic Sans MS", 17, "bold"), bg=PURPLE, fg="#4C0080").pack(padx=20, pady=(6, 0))
        tk.Label(nivel_frame,
                 text=f"👑 Nível {self.jogadora.level}  —  {self.jogadora.titulo()}",
                 font=("Arial", 12, "bold"), bg=PURPLE, fg=VIOLET).pack(padx=20, pady=(0, 6))

        # [9] barra de XP
        self._barra_xp(main)

        # stats
        stats_frame = tk.Frame(main, bg=LILAC, relief="raised", bd=2)
        stats_frame.pack(padx=30, pady=4)
        tk.Label(
            stats_frame,
            text=(f"💜 XP: {self.jogadora.xp}  |  "
                  f"🎮 Jogos: {self.jogadora.stats['games_played']}  |  "
                  f"🏆 Vitórias: {self.jogadora.stats['games_won']}"),
            font=("Arial", 11, "bold"), bg=LILAC, fg="#4C0080"
        ).pack(padx=10, pady=7)

        # mascote
        mascote = tk.Frame(main, bg=PEACH, relief="raised", bd=2)
        mascote.pack(padx=30, pady=4)
        tk.Label(mascote,
                 text=f"🦋 Cirilla: {random.choice(['Pronta pra treinar a memória? 🎀','Bora subir de nível? ✨','Você consegue, feiticeira! 🌸'])}",
                 font=("Arial", 11, "italic"), bg=PEACH, fg=DARK_TEXT).pack(padx=10, pady=5)

        # dificuldade + tema
        config_frame = tk.Frame(main, bg=BG)
        config_frame.pack(pady=6)

        tk.Label(config_frame, text="Dificuldade:",
                 font=("Arial", 12, "bold"), bg=BG, fg=VIOLET).grid(row=0, column=0, padx=8)
        diff_inner = tk.Frame(config_frame, bg=BG)
        diff_inner.grid(row=0, column=1, padx=8)
        for d in Dificuldade:
            tk.Radiobutton(diff_inner, text=d.value, variable=self.diff, value=d.value,
                           font=("Arial", 11), bg=BG, activebackground=PINK).pack(side="left", padx=6)

        tk.Label(config_frame, text="Tema das cartas:",
                 font=("Arial", 12, "bold"), bg=BG, fg=VIOLET).grid(row=1, column=0, padx=8, pady=4)
        tema_inner = tk.Frame(config_frame, bg=BG)
        tema_inner.grid(row=1, column=1, padx=8, pady=4)
        for nome_tema in TEMAS:
            tk.Radiobutton(tema_inner, text=nome_tema, variable=self.tema_atual,
                           value=nome_tema, font=("Arial", 10), bg=BG,
                           activebackground=MINT).pack(side="left", padx=5)

        # botões
        botoes = tk.Frame(main, bg=BG)
        botoes.pack(pady=8)

        tk.Label(botoes, text="▶️ Jogar",
                 font=("Arial", 11, "bold"), bg=BG, fg=DEEP_RED).pack(pady=(0, 2))
        tk.Button(botoes, text="🎮 JOGAR",
                  font=("Arial", 13, "bold"), bg=PINK, fg="white", width=22,
                  command=self.new_game).pack(pady=3)
        if FileManager.existe(SAVE_GAME_FILE):
            tk.Button(botoes, text="▶️ CONTINUAR JOGO",
                      font=("Arial", 12, "bold"), bg=MINT, fg=DARK_TEXT, width=22,
                      command=self.continuar_jogo).pack(pady=3)

        tk.Label(botoes, text="⚙️ Gerenciar",
                 font=("Arial", 11, "bold"), bg=BG, fg=DEEP_RED).pack(pady=(10, 2))
        for texto, cor, cmd in [
            ("📊 COMPARAR PERFIS",   BLUE,   self.comparar_perfis),
            ("👑 MEU PERFIL",        LILAC,  self.show_profile),
            ("🏆 RANKING",           YELLOW, self.show_ranking),
            ("⭐ CONQUISTAS",         PEACH,  self.show_achievements),
            ("📜 HISTÓRICO",         PURPLE, self.show_historico),
            ("👥 TROCAR PERFIL",     CORAL,  self.tela_perfis),
        ]:
            fg = DARK_TEXT if cor in (YELLOW, PEACH) else "white"
            tk.Button(botoes, text=texto, font=("Arial", 11, "bold"),
                      bg=cor, fg=fg, width=22, command=cmd).pack(pady=2)

    # ─────────────────────────────────────────────────────────────
    # PERFIL / RANKING / CONQUISTAS / HISTÓRICO
    # ─────────────────────────────────────────────────────────────
    def show_profile(self):
        self.clear()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="👑 MEU PERFIL 👑",
                 font=("Comic Sans MS", 30, "bold"), bg=BG, fg=DEEP_RED).pack(pady=18)

        frame = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
        frame.pack(padx=30, pady=12, fill="both")
        melhor = self.jogadora.stats["best_time"]
        info = (
            f"👤 Nome: {self.jogadora.nome}\n"
            f"👑 Título: {self.jogadora.titulo()}\n"
            f"⭐ Nível: {self.jogadora.level}\n"
            f"💜 XP Total: {self.jogadora.xp}\n"
            f"🎮 Jogos jogados: {self.jogadora.stats['games_played']}\n"
            f"🏆 Vitórias: {self.jogadora.stats['games_won']}\n"
            f"⏱️ Melhor tempo: {melhor}s" if melhor else "⏱️ Melhor tempo: —"
        )
        tk.Label(frame, text=info, font=("Arial", 13),
                 bg=LIGHT_PINK, fg=DARK_TEXT, justify="left").pack(padx=20, pady=16)

        self._barra_xp(frame)

        if self.jogadora.achievements:
            tk.Label(frame, text="Suas Conquistas 🏆:",
                     font=("Arial", 12, "bold"), bg=LIGHT_PINK, fg=DEEP_RED).pack()
            for c in self.jogadora.achievements:
                tk.Label(frame, text=f"  ✓ {c}",
                         font=("Arial", 11), bg=LIGHT_PINK, fg="#4C0080").pack()

        self._botao_voltar(main, self.home)

    def show_ranking(self):
        self.clear()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="🏆 RANKING TOP 10 🏆",
                 font=("Comic Sans MS", 30, "bold"), bg=BG, fg=DEEP_RED).pack(pady=18)
        self._subtitulo_perfil(main)

        if self.ranking.esta_vazio():
            tk.Label(main, text="Sem dados ainda… Seja a primeira! 🌸",
                     font=("Arial", 14), bg=BG, fg=VIOLET).pack(pady=50)
        else:
            frame = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
            frame.pack(padx=30, pady=16, fill="both")
            medalhas = {0: "🥇", 1: "🥈", 2: "🥉"}
            cores    = {0: YELLOW, 1: PEACH, 2: CORAL}
            for i, p in enumerate(self.ranking.lista[:10]):
                bg = cores.get(i, LIGHT_PINK)
                tk.Label(
                    frame,
                    text=f"{medalhas.get(i, f'{i+1:2d}.')} {p['name']} — Score: {p['score']} — ⏱️ {p['time']}s",
                    font=("Arial", 12, "bold"), bg=bg, fg=DARK_TEXT
                ).pack(padx=10, pady=7, fill="x")

        tk.Button(main, text="♻️ Resetar Ranking",
                  font=("Arial", 11, "bold"), bg=RED, fg="white", width=22,
                  command=self.resetar_ranking).pack(pady=(8, 0))
        destino = self.home if self.jogadora else self.tela_perfis
        self._botao_voltar(main, destino)

    def show_achievements(self):
        self.clear()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="⭐ CONQUISTAS ⭐",
                 font=("Comic Sans MS", 30, "bold"), bg=BG, fg=DEEP_RED).pack(pady=18)
        self._subtitulo_perfil(main)

        frame = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
        frame.pack(padx=30, pady=16, fill="both")
        todas = [
            "Primeira Vitória 🏆", "Velocista ⚡", "Mestre da Memória 🧙‍♀️",
            "Campeã Fácil 🌸",     "Campeã Médio 💜", "Campeã Difícil 🔥",
            "10 Vitórias 🎉",       "Nivel 10 👑",    "Perfecta 💯",
            "Speedrun Master ⚡⚡⚡", "Streak Master 🔥🔥🔥",
        ]
        for c in todas:
            if c in self.jogadora.achievements:
                tk.Label(frame, text=f"✓ {c}",
                         font=("Arial", 11, "bold"), bg="#FFD6A5", fg=DARK_TEXT).pack(
                    padx=10, pady=5, fill="x")
            else:
                tk.Label(frame, text=f"🔒 {c}",
                         font=("Arial", 11), bg=LIGHT_PINK, fg="#999999").pack(
                    padx=10, pady=5, fill="x")

        self._botao_voltar(main, self.home)

    def show_historico(self):
        """📜 Últimas MAX_HISTORICO partidas da jogadora ativa."""
        self.clear()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="📜 HISTÓRICO DE PARTIDAS 📜",
                 font=("Comic Sans MS", 26, "bold"), bg=BG, fg=DEEP_RED).pack(pady=18)
        self._subtitulo_perfil(main)

        hist = self.jogadora.historico
        if not hist:
            tk.Label(main, text="Nenhuma partida registrada ainda… Jogue primeiro! 🎮",
                     font=("Arial", 13, "italic"), bg=BG, fg=VIOLET).pack(pady=40)
        else:
            frame = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
            frame.pack(padx=30, pady=12, fill="both")
            cabecalho = "  #  |  Data & Hora          |  Dificuldade  |  Tempo  |  Resultado"
            tk.Label(frame, text=cabecalho,
                     font=("Courier", 11, "bold"), bg=LILAC, fg=DARK_TEXT).pack(
                padx=8, pady=6, fill="x")
            for i, h in enumerate(hist, 1):
                resultado = "✅ Vitória" if h["vitoria"] else "❌ Derrota"
                linha = (
                    f"  {i}  |  {h['data']}  |  "
                    f"{h['dificuldade']:<13}|  {h['tempo']:>4}s  |  {resultado}"
                )
                cor = MINT if h["vitoria"] else CORAL
                tk.Label(frame, text=linha,
                         font=("Courier", 11), bg=cor, fg=DARK_TEXT).pack(
                    padx=8, pady=4, fill="x")

        self._botao_voltar(main, self.home)

    # ─────────────────────────────────────────────────────────────
    # SALVAR / CARREGAR PARTIDA
    # ─────────────────────────────────────────────────────────────
    def salvar_jogo(self):
        elapsed = (self.tempo_acumulado + int(time.time() - self.start_time)
                   if self.start_time else self.tempo_acumulado)
        estado = {
            "valores":    [c.valor for c in self.cartas],
            "combinadas": [c.indice for c in self.cartas if c.combinada],
            "linhas":     self.rows,
            "colunas":    self.cols,
            "pares":      self.pairs,
            "dificuldade": self.diff.get(),
            "tema":        self.tema_atual.get(),
            "nome":        self.jogadora.nome,
            "tempo":       elapsed,
            "streak":      self.streak,
        }
        FileManager.gravar(SAVE_GAME_FILE, estado)
        self.start_time = None
        messagebox.showinfo("💾 Jogo salvo!",
                            "Partida guardada no grimório! ✨\n"
                            "Clique em '▶️ Continuar Jogo' quando voltar. 🌸")
        self.home()

    def continuar_jogo(self):
        if not FileManager.existe(SAVE_GAME_FILE):
            messagebox.showinfo("Ops!", "Nenhum jogo salvo encontrado. 🌙")
            self.home()
            return
        estado = FileManager.ler(SAVE_GAME_FILE)
        if not estado:
            messagebox.showinfo("Ops!", "O arquivo salvo está ilegível. 😢")
            self.home()
            return
        nome_salvo = estado.get("nome")
        if nome_salvo and self.gerenciador.existe(nome_salvo):
            self.jogadora = self.gerenciador.carregar_jogadora(nome_salvo)
        self.new_game(estado_salvo=estado)

    # ─────────────────────────────────────────────────────────────
    # SEGURANÇA: sair / reiniciar durante a partida
    # ─────────────────────────────────────────────────────────────
    def voltar_da_partida(self):
        if messagebox.askyesno("Voltar",
                               "Se voltar agora, perde a partida (salve antes).\nQuer mesmo voltar? 🌙"):
            self.home()

    def reiniciar_partida(self):
        if messagebox.askyesno("Novo jogo",
                               "Recomeçar vai perder a partida atual. Tem certeza? 🔄"):
            self.new_game()

    # ─────────────────────────────────────────────────────────────
    # A PARTIDA
    # ─────────────────────────────────────────────────────────────
    def _dificuldade_atual(self) -> Dificuldade:
        for d in Dificuldade:
            if d.value == self.diff.get():
                return d
        return Dificuldade.FACIL

    def new_game(self, estado_salvo=None):
        self.clear()
        self.streak   = 0
        self.primeira = None
        self.segunda  = None

        if estado_salvo is None:
            self.jogadora.stats["games_played"] += 1
            self.gerenciador.salvar_jogadora(self.jogadora)
            rows, cols = GRADE_DIFICULDADE[self._dificuldade_atual()]
            pairs      = (rows * cols) // 2
            icons      = TEMAS[self.tema_atual.get()][:pairs]
            valores    = icons * 2
            random.shuffle(valores)
            self.cartas         = [Carta(i, v) for i, v in enumerate(valores)]
            self.tempo_acumulado = 0
        else:
            rows   = estado_salvo["linhas"]
            cols   = estado_salvo["colunas"]
            pairs  = estado_salvo["pares"]
            self.diff.set(estado_salvo["dificuldade"])
            self.tema_atual.set(estado_salvo.get("tema", "Kawaii 🎀"))
            valores = estado_salvo["valores"]
            combinadas = set(estado_salvo["combinadas"])
            self.cartas = [Carta(i, v) for i, v in enumerate(valores)]
            for c in self.cartas:
                if c.indice in combinadas:
                    c.marcar_combinada()
            self.tempo_acumulado = estado_salvo["tempo"]
            self.streak          = estado_salvo.get("streak", 0)

        self.rows  = rows
        self.cols  = cols
        self.pairs = pairs
        total      = rows * cols
        self.start_time = None
        found_ini  = sum(1 for c in self.cartas if c.combinada) // 2

        # ── construção da tela ───────────────────────────────────
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)

        # status
        status = tk.Frame(main, bg=LILAC, relief="raised", bd=2)
        status.pack(padx=18, pady=10, fill="x")
        tk.Label(status,
                 text=f"👤 {self.jogadora.nome}  |  👑 Nível {self.jogadora.level}  |  📊 {self.diff.get()}  |  {self.tema_atual.get()}",
                 font=("Arial", 11, "bold"), bg=LILAC, fg="#4C0080").pack(side="left", padx=10, pady=7)
        self.timer = tk.Label(status, text="⏱️ 00:00",
                              font=("Arial", 11, "bold"), bg=LILAC, fg=VIOLET)
        self.timer.pack(side="right", padx=10)
        self.progress_lbl = tk.Label(status, text=f"🎁 Pares: {found_ini}/{pairs}",
                                     font=("Arial", 11, "bold"), bg=LILAC, fg=DEEP_RED)
        self.progress_lbl.pack(side="right", padx=10)

        # [9] barra de XP inline
        xp_frame = tk.Frame(main, bg=BG)
        xp_frame.pack(fill="x", padx=18, pady=(0, 2))
        xp_atual = self.jogadora.xp_no_nivel_atual()
        xp_max   = self.jogadora.xp_para_proximo()
        pct      = xp_atual / xp_max
        self.xp_canvas = tk.Canvas(xp_frame, width=500, height=16,
                                   bg="#E8D5F5", highlightthickness=1,
                                   highlightbackground=LILAC)
        self.xp_canvas.pack(side="left", padx=8)
        self.xp_canvas.create_rectangle(0, 0, int(500 * pct), 16, fill=LILAC, outline="")
        self.xp_canvas.create_text(250, 8,
                                   text=f"XP Nível {self.jogadora.level}: {xp_atual}/{xp_max}",
                                   font=("Arial", 9, "bold"), fill=DARK_TEXT)

        # streak display
        self.streak_lbl = tk.Label(xp_frame,
                                   text=f"🔥 Streak: {self.streak}",
                                   font=("Arial", 10, "bold"), bg=BG, fg=DEEP_RED)
        self.streak_lbl.pack(side="left", padx=10)

        # dica
        tk.Label(main, text="💡 Vire duas cartas e tente formar pares iguais!",
                 font=("Arial", 10, "italic"), bg=BG, fg=VIOLET).pack(pady=(4, 0))

        # mascote
        self.mascote_label = tk.Label(
            main, text="🦋 Cirilla: boa sorte! 💖",
            font=("Arial", 12, "bold"), bg=PEACH, fg=DARK_TEXT,
            relief="raised", bd=2, width=52
        )
        self.mascote_label.pack(pady=(4, 6), ipady=3)

        # tabuleiro
        board = tk.Frame(main, bg=BG)
        board.pack(padx=16, pady=4)
        cores_btn = [PINK, BLUE, MINT, PEACH, YELLOW, LILAC, PURPLE, CORAL]
        self.btns: list[tk.Button] = []
        for i in range(total):
            btn = tk.Button(
                board, text="", width=5, height=2,
                font=("Arial", 22, "bold"),
                bg=cores_btn[i % len(cores_btn)],
                activebackground="#FFFFFF", relief="raised", bd=2,
                command=lambda x=i: self.flip(x)
            )
            btn.grid(row=i // cols, column=i % cols, padx=5, pady=5)
            self.btns.append(btn)

        # controles
        ctrl = tk.Frame(main, bg=BG)
        ctrl.pack(pady=10)
        for texto, cor, cmd in [
            ("🔙 Voltar",       BLUE,  self.voltar_da_partida),
            ("🔄 Novo Jogo",    PINK,  self.reiniciar_partida),
            ("💾 Salvar e Sair", MINT,  self.salvar_jogo),
            ("🚪 Sair",         CORAL, self.sair_do_jogo),
        ]:
            tk.Button(ctrl, text=texto, font=("Arial", 10, "bold"),
                      bg=cor, width=14, command=cmd).pack(side="left", padx=5)

        if estado_salvo is None:
            self.show_cards_memory()
        else:
            self._restaurar_tabuleiro()

    # ── tabuleiro (restaurar jogo salvo) ────────────────────────
    def _restaurar_tabuleiro(self):
        for carta in self.cartas:
            if carta.combinada:
                self.btns[carta.indice].config(
                    text=carta.valor, state="disabled", bg="#FDE2E4")
        self.mascote_label.config(text="🦋 Cirilla: bem-vinda de volta! 🌙", bg=PEACH)
        self.start_time = time.time()
        self.update_timer()

    # ── memorização ──────────────────────────────────────────────
    def show_cards_memory(self):
        for i, carta in enumerate(self.cartas):
            self.btns[i].config(text=carta.valor, state="disabled")
        self.segundos_memo = 5
        self._contar_memo()

    def _contar_memo(self):
        if not self.mascote_label.winfo_exists():
            return
        if self.segundos_memo > 0:
            self.mascote_label.config(
                text=f"🧠 Memorize! Escondendo em {self.segundos_memo}…", bg=YELLOW)
            self.segundos_memo -= 1
            self.root.after(1000, self._contar_memo)
        else:
            self.mascote_label.config(text="🎮 Valendo! Encontre os pares! 💪", bg=PEACH)
            self._iniciar_jogo_real()

    def _iniciar_jogo_real(self):
        for i, btn in enumerate(self.btns):
            if not self.cartas[i].combinada:
                btn.config(text="", state="normal")
        self.start_time = time.time()
        self.update_timer()

    # ── cronômetro ───────────────────────────────────────────────
    def update_timer(self):
        if not self.timer.winfo_exists():
            return
        combinados = sum(1 for c in self.cartas if c.combinada)
        if self.start_time and combinados < self.pairs * 2:
            elapsed  = self.tempo_acumulado + int(time.time() - self.start_time)
            self.timer.config(text=f"⏱️ {elapsed//60:02d}:{elapsed%60:02d}")
            self.root.after(1000, self.update_timer)

    # ── [+] animação de virar carta ──────────────────────────────
    def _animar_carta(self, idx: int, valor: str, passos=3):
        """Flash rápido na cor do botão antes de revelar o emoji."""
        cores_flash = ["#FFFFFF", "#FFE0F0", "#FFB6C1"]
        btn = self.btns[idx]

        def passo(n):
            if n < len(cores_flash):
                btn.config(bg=cores_flash[n])
                self.root.after(50, lambda: passo(n + 1))
            else:
                btn.config(text=valor)

        passo(0)

    # ── virar carta ──────────────────────────────────────────────
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
            # desabilita cliques enquanto confere
            for btn in self.btns:
                btn.config(state="disabled")
            self.root.after(700, self.check_match)

    # ── conferir par ─────────────────────────────────────────────
    def check_match(self):
        a, b = self.primeira, self.segunda

        if a.valor == b.valor:
            a.marcar_combinada()
            b.marcar_combinada()
            self.btns[a.indice].config(state="disabled", bg="#FDE2E4")
            self.btns[b.indice].config(state="disabled", bg="#FDE2E4")

            # [8] streak
            self.streak += 1
            self.streak_lbl.config(text=f"🔥 Streak: {self.streak}")

            if self.streak > 0 and self.streak % STREAK_TRIGGER == 0:
                # bônus de streak!
                self.mascote_label.config(
                    text=f"🦋 Cirilla: {random.choice(FALAS_STREAK)}", bg=YELLOW)
                self._ganhar_xp(XP_STREAK)
                Som.streak()
                self._desbloquear("Streak Master 🔥🔥🔥")
            else:
                self.mascote_label.config(
                    text=f"🦋 Cirilla: {random.choice(FALAS_ACERTO)}", bg=MINT)
                Som.acerto()

            self._ganhar_xp(XP_ACERTO)
            self._atualizar_barra_xp()

        else:
            self.btns[a.indice].config(text="", bg=self._cor_botao(a.indice))
            self.btns[b.indice].config(text="", bg=self._cor_botao(b.indice))
            a.esconder()
            b.esconder()
            self.mascote_label.config(
                text=f"🦋 Cirilla: {random.choice(FALAS_ERRO)}", bg=PEACH)
            Som.erro()
            self.streak = 0
            self.streak_lbl.config(text=f"🔥 Streak: {self.streak}")

        self.primeira = None
        self.segunda  = None

        # reabilita cartas não combinadas
        for carta in self.cartas:
            if not carta.combinada:
                self.btns[carta.indice].config(state="normal")

        combinados = sum(1 for c in self.cartas if c.combinada)
        self.progress_lbl.config(text=f"🎁 Pares: {combinados//2}/{self.pairs}")

        if combinados == self.pairs * 2:
            self.vitoria()

    def _cor_botao(self, i: int) -> str:
        cores = [PINK, BLUE, MINT, PEACH, YELLOW, LILAC, PURPLE, CORAL]
        return cores[i % len(cores)]

    def _atualizar_barra_xp(self):
        """Redesenha a barra de XP inline durante a partida."""
        if not hasattr(self, "xp_canvas") or not self.xp_canvas.winfo_exists():
            return
        xp_atual = self.jogadora.xp_no_nivel_atual()
        xp_max   = self.jogadora.xp_para_proximo()
        pct      = xp_atual / xp_max
        self.xp_canvas.delete("all")
        self.xp_canvas.create_rectangle(0, 0, int(500 * pct), 16, fill=LILAC, outline="")
        self.xp_canvas.create_text(
            250, 8,
            text=f"XP Nível {self.jogadora.level}: {xp_atual}/{xp_max}",
            font=("Arial", 9, "bold"), fill=DARK_TEXT
        )

    # ── vitória ──────────────────────────────────────────────────
    def vitoria(self):
        elapsed     = self.tempo_acumulado + int(time.time() - self.start_time)
        self.start_time = None

        self.jogadora.stats["games_won"]  += 1
        self.jogadora.stats["total_time"] += elapsed
        if (self.jogadora.stats["best_time"] is None
                or elapsed < self.jogadora.stats["best_time"]):
            self.jogadora.stats["best_time"] = elapsed

        # histórico
        self.jogadora.registrar_partida(elapsed, self.diff.get(), vitoria=True)
        self.gerenciador.salvar_jogadora(self.jogadora)

        self._ganhar_xp(XP_VITORIA)
        self._desbloquear("Primeira Vitória 🏆")
        if elapsed <= 60:
            self._desbloquear("Velocista ⚡")
        if self._dificuldade_atual() == Dificuldade.DIFICIL:
            self._desbloquear("Mestre da Memória 🧙‍♀️")
        if self.jogadora.stats["games_won"] == 10:
            self._desbloquear("10 Vitórias 🎉")
        if self.jogadora.level >= 10:
            self._desbloquear("Nivel 10 👑")

        FileManager.apagar(SAVE_GAME_FILE)
        self.ranking.adicionar(
            self.jogadora.nome, self.jogadora.xp, elapsed, self.jogadora.level)

        Som.vitoria()
        messagebox.showinfo(
            "🎉 VITÓRIA!",
            f"PARABÉNS! 🎉\n\n"
            f"👤 {self.jogadora.nome}\n"
            f"👑 {self.jogadora.titulo()}\n"
            f"⏱️ Tempo: {elapsed}s\n"
            f"⭐ Nível: {self.jogadora.level}\n"
            f"💜 XP Total: {self.jogadora.xp}\n\n"
            f"Você é incrível! ✨"
        )
        self.home()


# ╔══════════════════════════════════════════════════════════════╗
# ║          INICIAR                                             ║
# ╚══════════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    root = tk.Tk()
    jogo = KawaiiMemoryGame(root)
    root.mainloop()