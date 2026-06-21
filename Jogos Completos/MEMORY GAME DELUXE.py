"""
╔══════════════════════════════════════════════════════════════════════╗
║           🎀 MEMORY GAME DELUXE KAWAII RPG — VERSÃO 10.0            ║
╠══════════════════════════════════════════════════════════════════════╣
║  NOVIDADES DA v10.0                                                  ║
║  ✅ Loja com moedas 🪙 (comprar temas, avatares e cosméticos)        ║
║  ✅ Temas visuais: Kawaii / Dark / Harry Potter / RGB 🎨             ║
║  ✅ Sistema de avatares e cosméticos equipáveis 🦋                   ║
║  ✅ Ranking separado por dificuldade 🏆                              ║
║  ✅ Dificuldade Mestre 8×8 🔥                                        ║
║  ✅ Barra de XP animada durante a partida ✨                         ║
║  ✅ Estatísticas avançadas (acurácia, média de tempo) 📊             ║
║  ✅ Salvamento automático a cada par encontrado 💾                   ║
║  ✅ Sons com pygame (fallback silencioso) 🔊                         ║
║  ✅ Configurações persistentes (tema/dificuldade salvos) ⚙️          ║
╚══════════════════════════════════════════════════════════════════════╝

Como rodar:
    python memory_kawaii_v10.py

Requisitos:
    - Python 3.10+  (tkinter já incluso)
    - pygame        (opcional, para sons): pip install pygame
    - numpy         (opcional, para sons sintéticos): pip install numpy
"""

# ── stdlib ──────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import json
import os
import math
from enum import Enum
from datetime import datetime

# ── pygame (opcional) ────────────────────────────────────────────────────────
try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    PYGAME_OK = True
except Exception:
    PYGAME_OK = False

try:
    import numpy as np
    NUMPY_OK = True
except Exception:
    NUMPY_OK = False


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        TEMAS VISUAIS                                ║
# ╚══════════════════════════════════════════════════════════════════════╝

TEMAS_VISUAIS = {
    "Kawaii 🎀": {
        "fundo":      "#FFF0F6",
        "cartao":     "#FFE4EC",
        "acento":     "#FF8FB1",
        "acento2":    "#FFC1CC",
        "texto":      "#2D3142",
        "texto_sec":  "#A48BA6",
        "barra_xp":   "#D8B4FE",
        "btn_cores":  ["#FFB6C1","#BDE0FE","#C7F9CC","#FFD6A5","#FDFFB6","#D8B4FE","#E0C3FC","#FFB3BA"],
        "titulo_cor": "#A4133C",
        "status_bg":  "#D8B4FE",
        "mascote_bg": "#FFD6A5",
        "borda":      "#FF8FB1",
    },
    "Dark 🌙": {
        "fundo":      "#1A1A2E",
        "cartao":     "#16213E",
        "acento":     "#E94560",
        "acento2":    "#0F3460",
        "texto":      "#E0E0E0",
        "texto_sec":  "#A0A0C0",
        "barra_xp":   "#E94560",
        "btn_cores":  ["#0F3460","#1A1A4E","#16213E","#0D0D2B","#1F1F4F","#2A0A3A","#0A2A3A","#2A1A0A"],
        "titulo_cor": "#E94560",
        "status_bg":  "#0F3460",
        "mascote_bg": "#16213E",
        "borda":      "#E94560",
    },
    "Harry Potter ⚡": {
        "fundo":      "#1C1C1C",
        "cartao":     "#2C1810",
        "acento":     "#D4AF37",
        "acento2":    "#8B0000",
        "texto":      "#F5DEB3",
        "texto_sec":  "#C8A96E",
        "barra_xp":   "#D4AF37",
        "btn_cores":  ["#8B0000","#1A3A1A","#1A1A5A","#3A3A1A","#5A1A1A","#1A5A1A","#1A1A8B","#5A3A1A"],
        "titulo_cor": "#D4AF37",
        "status_bg":  "#2C1810",
        "mascote_bg": "#3A2A10",
        "borda":      "#D4AF37",
    },
    "RGB 🌈": {
        "fundo":      "#0D0D0D",
        "cartao":     "#111111",
        "acento":     "#FF0080",
        "acento2":    "#00FF80",
        "texto":      "#FFFFFF",
        "texto_sec":  "#AAAAAA",
        "barra_xp":   "#00FFFF",
        "btn_cores":  ["#FF0080","#FF8000","#FFFF00","#00FF00","#00FFFF","#0080FF","#8000FF","#FF00FF"],
        "titulo_cor": "#FF0080",
        "status_bg":  "#111111",
        "mascote_bg": "#111111",
        "borda":      "#FF0080",
    },
}

# Tema ativo (mutable, alterado pela loja/configuração)
_TEMA_ATUAL = "Kawaii 🎀"

def T(chave: str) -> str:
    """Retorna a cor do tema visual ativo."""
    return TEMAS_VISUAIS.get(_TEMA_ATUAL, TEMAS_VISUAIS["Kawaii 🎀"]).get(chave, "#FFFFFF")

def btn_cor(i: int) -> str:
    cores = TEMAS_VISUAIS.get(_TEMA_ATUAL, TEMAS_VISUAIS["Kawaii 🎀"])["btn_cores"]
    return cores[i % len(cores)]


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        CONSTANTES GLOBAIS                           ║
# ╚══════════════════════════════════════════════════════════════════════╝

# XP e progressão
XP_POR_NIVEL   = 100
XP_ACERTO      = 10
XP_VITORIA     = 50
XP_STREAK      = 20
STREAK_TRIGGER = 3
MAX_HISTORICO  = 10

# Moedas
MOEDAS_VITORIA    = 30
MOEDAS_ACERTO     = 2
MOEDAS_STREAK     = 10

# Arquivos
RANK_FILE      = "ranking_v10.json"
PERFIS_FILE    = "perfis_v10.json"
SAVE_GAME_FILE = "jogo_salvo_v10.json"
CONFIG_FILE    = "config_v10.json"

# Títulos por nível
TITULOS = {
    1:  "Aprendiz 🌱",
    3:  "Maga do Código 🔮",
    6:  "Arquimaga 👑",
    10: "Lenda Kawaii ✨",
    15: "Grã-Feiticeira 🌟",
    20: "Deusa da Memória 💫",
}

def titulo_para_nivel(level: int) -> str:
    titulo = TITULOS[1]
    for limiar, nome in TITULOS.items():
        if level >= limiar:
            titulo = nome
    return titulo


# ── Temas de cartas ──────────────────────────────────────────────────────────
TEMAS_CARTAS = {
    "Kawaii 🎀":        ["🌸","🎀","🧸","🩷","🦋","🌙","🍓","🧁","⭐","🍀","🐱","💎","🌈","🦄","🍭","🌼","🎵","☁️"],
    "Natureza 🌿":      ["🌲","🌺","🍄","🐸","🌊","🦊","🐝","🌻","🍁","🦜","🐚","🌍","🦋","🌿","🐠","🍃","🌙","⛰️"],
    "Comida 🍕":        ["🍕","🍣","🍩","🌮","🍜","🍓","🧁","🍦","🍇","🥑","🍋","🥐","🍔","🍿","🥞","🍰","🥭","🫐"],
    "Espaço 🚀":        ["🚀","🌙","⭐","🪐","☄️","🌌","👾","🛸","🔭","💫","🌠","🪨","🌟","🌑","🛰️","🌞","🌀","🔮"],
    "Harry Potter ⚡":  ["⚡","🦉","🧙","🏰","🪄","🦁","🐍","🦅","🦡","📚","🔮","🧪","💀","🌿","🕯️","🪞","🧹","🐲"],
    "Animais 🐾":       ["🐶","🐱","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐸","🐵","🐔","🐧","🦆","🦋","🐢"],
}

# ── Avatares e cosméticos ────────────────────────────────────────────────────
AVATARES = {
    "🧙 Feiticeira":     {"preco": 0,   "desbloqueado": True},
    "🦋 Borboleta":      {"preco": 100, "desbloqueado": False},
    "🌸 Flor de Cerejeira": {"preco": 150, "desbloqueado": False},
    "👑 Rainha":         {"preco": 250, "desbloqueado": False},
    "🐱 Gatinha":        {"preco": 200, "desbloqueado": False},
    "🦄 Unicórnio":      {"preco": 300, "desbloqueado": False},
    "🌙 Lua":            {"preco": 180, "desbloqueado": False},
    "⚡ Tempestade":     {"preco": 350, "desbloqueado": False},
}

TEMAS_LOJA = {
    "Kawaii 🎀":        {"preco": 0,   "desbloqueado": True},
    "Dark 🌙":          {"preco": 200, "desbloqueado": False},
    "Harry Potter ⚡":  {"preco": 300, "desbloqueado": False},
    "RGB 🌈":           {"preco": 400, "desbloqueado": False},
}

COSMETICOS_LOJA = {
    "Moldura Rosa 🌸":   {"preco": 80,  "desbloqueado": False},
    "Moldura Dourada ✨": {"preco": 200, "desbloqueado": False},
    "Moldura Arco-íris 🌈": {"preco": 350, "desbloqueado": False},
    "Trilha Sonora RPG 🎵": {"preco": 150, "desbloqueado": False},
    "Efeito Confete 🎉":  {"preco": 120, "desbloqueado": False},
}

# ── Dificuldade ──────────────────────────────────────────────────────────────
class Dificuldade(Enum):
    FACIL   = "Fácil"
    MEDIO   = "Médio"
    DIFICIL = "Difícil"
    MESTRE  = "Mestre 🔥"

GRADE_DIFICULDADE = {
    Dificuldade.FACIL:   (4, 4),
    Dificuldade.MEDIO:   (4, 5),
    Dificuldade.DIFICIL: (6, 6),
    Dificuldade.MESTRE:  (8, 8),
}

# ── Falas da mascote ─────────────────────────────────────────────────────────
FALAS_ACERTO = ["Isso! Você acertou um par! 💖","Que incrível! ⭐","Você é a melhor! 👑","Mandou bem demais! 🌟"]
FALAS_STREAK = ["🔥 STREAK x3! XP bônus pra você! ✨","🔥 Três seguidos! Você tá voando! 💜","🔥 Combo incrível! +20 XP! 🌟"]
FALAS_ERRO   = ["Quase! Tenta outro par 💭","Calma, você consegue! 🌸","Respira e olha de novo 🦋"]
FALAS_INICIO = ["Pronta pra treinar a memória? 🎀","Bora subir de nível? ✨","Você consegue, feiticeira! 🌸","Que a magia esteja com você! ⚡"]


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        FILE MANAGER                                 ║
# ╚══════════════════════════════════════════════════════════════════════╝

class FileManager:
    @staticmethod
    def ler(caminho: str, padrao=None):
        if not os.path.exists(caminho):
            return padrao
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return padrao

    @staticmethod
    def gravar(caminho: str, dados) -> bool:
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    @staticmethod
    def apagar(caminho: str) -> bool:
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


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        CLASSE CARTA                                 ║
# ╚══════════════════════════════════════════════════════════════════════╝

class Carta:
    def __init__(self, indice: int, valor: str):
        self.indice    = indice
        self.valor     = valor
        self.virada    = False
        self.combinada = False

    def virar(self):        self.virada = True
    def esconder(self):     self.virada = False
    def marcar_combinada(self):
        self.combinada = True
        self.virada    = True


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        SOM                                          ║
# ╚══════════════════════════════════════════════════════════════════════╝

class Som:
    @staticmethod
    def _gerar(freq: float, duracao: float, volume: float = 0.3):
        if not PYGAME_OK or not NUMPY_OK:
            return
        try:
            taxa   = 44100
            frames = int(taxa * duracao)
            t      = np.linspace(0, duracao, frames, False)
            onda   = (np.sin(2 * np.pi * freq * t) * 32767 * volume).astype(np.int16)
            som    = pygame.sndarray.make_sound(onda)
            som.play()
        except Exception:
            pass

    @staticmethod
    def acerto():  Som._gerar(880, 0.12)

    @staticmethod
    def erro():    Som._gerar(220, 0.18)

    @staticmethod
    def streak():  Som._gerar(1046, 0.20)

    @staticmethod
    def compra():  Som._gerar(660, 0.15)

    @staticmethod
    def vitoria():
        for freq in [523, 659, 784, 1046]:
            Som._gerar(freq, 0.10)
            time.sleep(0.08)

    @staticmethod
    def nivel_up():
        for freq in [523, 659, 784, 1046, 1318]:
            Som._gerar(freq, 0.08)
            time.sleep(0.06)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        JOGADORA                                     ║
# ╚══════════════════════════════════════════════════════════════════════╝

class Jogadora:
    def __init__(self, nome="Convidada"):
        self.nome   = nome
        self.xp     = 0
        self.level  = 1
        self.moedas = 50   # começa com 50 moedinhas de boas-vindas 🪙
        self.achievements = []
        self.historico    = []
        self.avatar       = "🧙 Feiticeira"
        self.cosmético    = None

        # inventário: o que a jogadora já comprou
        self.avatares_desbloqueados  = ["🧙 Feiticeira"]
        self.temas_desbloqueados     = ["Kawaii 🎀"]
        self.cosmeticos_desbloqueados = []

        self.stats = {
            "games_played":  0,
            "games_won":     0,
            "total_time":    0,
            "best_time":     None,
            "total_acertos": 0,
            "total_tentativas": 0,
        }

    # ── serialização ─────────────────────────────────────────────────────────
    def para_dicionario(self) -> dict:
        return {
            "xp":          self.xp,
            "level":       self.level,
            "moedas":      self.moedas,
            "achievements":self.achievements,
            "historico":   self.historico,
            "avatar":      self.avatar,
            "cosmetico":   self.cosmético,
            "avatares_desbloqueados":   self.avatares_desbloqueados,
            "temas_desbloqueados":      self.temas_desbloqueados,
            "cosmeticos_desbloqueados": self.cosmeticos_desbloqueados,
            "stats":       self.stats,
        }

    def carregar_de(self, dados: dict):
        self.xp          = dados.get("xp", 0)
        self.level       = dados.get("level", 1)
        self.moedas      = dados.get("moedas", 50)
        self.achievements= dados.get("achievements", [])
        self.historico   = dados.get("historico", [])
        self.avatar      = dados.get("avatar", "🧙 Feiticeira")
        self.cosmético   = dados.get("cosmetico")
        self.avatares_desbloqueados   = dados.get("avatares_desbloqueados", ["🧙 Feiticeira"])
        self.temas_desbloqueados      = dados.get("temas_desbloqueados", ["Kawaii 🎀"])
        self.cosmeticos_desbloqueados = dados.get("cosmeticos_desbloqueados", [])
        self.stats       = dados.get("stats", self.stats)

    # ── XP ───────────────────────────────────────────────────────────────────
    def ganhar_xp(self, qtd: int) -> bool:
        nivel_antigo = self.level
        self.xp     += qtd
        self.level   = self.xp // XP_POR_NIVEL + 1
        return self.level > nivel_antigo

    def xp_no_nivel(self) -> int:
        return self.xp % XP_POR_NIVEL

    def xp_para_proximo(self) -> int:
        return XP_POR_NIVEL

    # ── moedas ───────────────────────────────────────────────────────────────
    def ganhar_moedas(self, qtd: int):
        self.moedas += qtd

    def gastar_moedas(self, qtd: int) -> bool:
        if self.moedas >= qtd:
            self.moedas -= qtd
            return True
        return False

    # ── conquistas ────────────────────────────────────────────────────────────
    def desbloquear(self, texto: str) -> bool:
        if texto not in self.achievements:
            self.achievements.append(texto)
            return True
        return False

    def titulo(self) -> str:
        return titulo_para_nivel(self.level)

    def acuracia(self) -> float:
        t = self.stats.get("total_tentativas", 0)
        if t == 0:
            return 0.0
        return round(self.stats.get("total_acertos", 0) / t * 100, 1)

    def registrar_partida(self, tempo: int, dificuldade: str, vitoria: bool):
        entrada = {
            "data":        datetime.now().strftime("%d/%m/%Y %H:%M"),
            "tempo":       tempo,
            "dificuldade": dificuldade,
            "vitoria":     vitoria,
        }
        self.historico.insert(0, entrada)
        self.historico = self.historico[:MAX_HISTORICO]


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                   GERENCIADOR DE PERFIS                             ║
# ╚══════════════════════════════════════════════════════════════════════╝

class GerenciadorDePerfis:
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


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        RANKING                                      ║
# ╚══════════════════════════════════════════════════════════════════════╝

class Ranking:
    """Ranking separado por dificuldade."""

    def __init__(self):
        self.dados: dict = {}
        self.carregar()

    def carregar(self):
        self.dados = FileManager.ler(RANK_FILE, padrao={})

    def salvar(self):
        FileManager.gravar(RANK_FILE, self.dados)

    def adicionar(self, nome: str, score: int, tempo: int, nivel: int, dificuldade: str):
        if dificuldade not in self.dados:
            self.dados[dificuldade] = []
        self.dados[dificuldade].append({
            "name": nome, "score": score, "time": tempo, "level": nivel
        })
        self.dados[dificuldade].sort(key=lambda x: x["score"], reverse=True)
        self.dados[dificuldade] = self.dados[dificuldade][:10]
        self.salvar()

    def lista_para(self, dificuldade: str) -> list:
        return self.dados.get(dificuldade, [])

    def resetar(self):
        self.dados = {}
        FileManager.apagar(RANK_FILE)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        CONFIGURAÇÕES                                ║
# ╚══════════════════════════════════════════════════════════════════════╝

class Config:
    """Persistência de configurações globais (tema, dificuldade, tema de cartas)."""

    def __init__(self):
        self.tema_visual   = "Kawaii 🎀"
        self.dificuldade   = Dificuldade.FACIL.value
        self.tema_cartas   = "Kawaii 🎀"
        self.carregar()

    def carregar(self):
        dados = FileManager.ler(CONFIG_FILE, padrao={})
        self.tema_visual = dados.get("tema_visual", "Kawaii 🎀")
        self.dificuldade = dados.get("dificuldade", Dificuldade.FACIL.value)
        self.tema_cartas = dados.get("tema_cartas", "Kawaii 🎀")

    def salvar(self):
        FileManager.gravar(CONFIG_FILE, {
            "tema_visual": self.tema_visual,
            "dificuldade": self.dificuldade,
            "tema_cartas": self.tema_cartas,
        })


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                     JOGO PRINCIPAL                                  ║
# ╚══════════════════════════════════════════════════════════════════════╝

class KawaiiMemoryGame:

    # ── init ─────────────────────────────────────────────────────────────────
    def __init__(self, root: tk.Tk):
        global _TEMA_ATUAL
        self.root = root
        self.root.title("🎀 Memory Game Kawaii RPG v10.0")
        self.root.geometry("1200x980")

        self.config      = Config()
        _TEMA_ATUAL      = self.config.tema_visual

        self.gerenciador = GerenciadorDePerfis()
        self.ranking     = Ranking()
        self.jogadora: Jogadora | None = None

        # controles de estado
        self.diff        = tk.StringVar(value=self.config.dificuldade)
        self.tema_cartas = tk.StringVar(value=self.config.tema_cartas)
        self.novo_perfil = tk.StringVar()

        self.tempo_acumulado = 0
        self.start_time      = None
        self.streak          = 0
        self.cartas: list[Carta] = []
        self.primeira: Carta | None = None
        self.segunda:  Carta | None = None
        self._bloqueado = False   # impede cliques duplos

        self._aplicar_tema_root()
        self.tela_perfis()

    # ── tema global ──────────────────────────────────────────────────────────
    def _aplicar_tema_root(self):
        self.root.configure(bg=T("fundo"))

    def _mudar_tema(self, novo_tema: str, salvar=True):
        global _TEMA_ATUAL
        _TEMA_ATUAL           = novo_tema
        self.config.tema_visual = novo_tema
        if salvar:
            self.config.salvar()
        self._aplicar_tema_root()

    # ── utilitários de tela ──────────────────────────────────────────────────
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _label(self, parent, texto, tamanho=12, bold=False, cor=None, bg=None, **kw):
        fonte  = ("Comic Sans MS" if bold else "Arial", tamanho, "bold" if bold else "normal")
        cor    = cor  or T("texto")
        bg     = bg   or T("fundo")
        return tk.Label(parent, text=texto, font=fonte, fg=cor, bg=bg, **kw)

    def _botao(self, parent, texto, cmd, cor=None, fg="white", largura=22, **kw):
        cor = cor or T("acento")
        return tk.Button(
            parent, text=texto, command=cmd,
            font=("Arial", 11, "bold"), bg=cor, fg=fg,
            width=largura, relief="flat", cursor="hand2",
            activebackground=T("acento2"), activeforeground=fg,
            bd=0, padx=8, pady=6, **kw
        )

    def _botao_voltar(self, parent, destino):
        self._botao(parent, "🔙 Voltar", destino, cor=T("acento2"),
                    fg=T("texto")).pack(pady=18)

    def _subtitulo_perfil(self, parent):
        if self.jogadora:
            self._label(
                parent,
                f"👤 {self.jogadora.nome}  |  {self.jogadora.avatar}  |  🪙 {self.jogadora.moedas}",
                tamanho=11, cor=T("texto_sec")
            ).pack(pady=(0, 6))

    # ── barra de XP animada ──────────────────────────────────────────────────
    def _barra_xp(self, parent, largura=420, altura=20) -> tk.Canvas:
        if not self.jogadora:
            return None
        xp_atual = self.jogadora.xp_no_nivel()
        xp_max   = self.jogadora.xp_para_proximo()
        pct      = xp_atual / xp_max

        frame = tk.Frame(parent, bg=T("fundo"))
        frame.pack(pady=(2, 6))
        self._label(frame,
                    f"⭐ Nível {self.jogadora.level} — {xp_atual}/{xp_max} XP",
                    tamanho=10, cor=T("texto_sec")).pack()

        canvas = tk.Canvas(frame, width=largura, height=altura,
                           bg=T("cartao"), highlightthickness=1,
                           highlightbackground=T("borda"))
        canvas.pack()

        def _animar(pct_atual=0.0):
            canvas.delete("all")
            canvas.create_rectangle(0, 0, int(largura * pct_atual), altura,
                                    fill=T("barra_xp"), outline="")
            canvas.create_text(largura // 2, altura // 2,
                                text=f"{int(pct_atual * 100)}%",
                                font=("Arial", 9, "bold"), fill=T("texto"))
            if pct_atual < pct:
                novo = min(pct_atual + 0.04, pct)
                canvas.after(20, lambda: _animar(novo))

        _animar()
        return canvas

    # ── atualizar barra XP inline (durante partida) ──────────────────────────
    def _atualizar_barra_xp_inline(self):
        if not hasattr(self, "xp_canvas") or not self.xp_canvas.winfo_exists():
            return
        xp_atual = self.jogadora.xp_no_nivel()
        xp_max   = self.jogadora.xp_para_proximo()
        pct      = xp_atual / xp_max
        c        = self.xp_canvas
        c.delete("all")
        c.create_rectangle(0, 0, int(500 * pct), 18, fill=T("barra_xp"), outline="")
        c.create_text(250, 9,
                      text=f"XP Nível {self.jogadora.level}: {xp_atual}/{xp_max}",
                      font=("Arial", 9, "bold"), fill=T("texto"))

    # ── helpers de jogadora ──────────────────────────────────────────────────
    def _ganhar_xp(self, qtd: int):
        subiu = self.jogadora.ganhar_xp(qtd)
        self.gerenciador.salvar_jogadora(self.jogadora)
        if subiu:
            Som.nivel_up()
            messagebox.showinfo(
                "✨ LEVEL UP!",
                f"Parabéns, {self.jogadora.nome}!\n"
                f"Você chegou ao nível {self.jogadora.level}!\n"
                f"Agora você é: {self.jogadora.titulo()} 🎉\n"
                f"🪙 +20 moedas de bônus!"
            )
            self.jogadora.ganhar_moedas(20)

    def _ganhar_moedas(self, qtd: int):
        self.jogadora.ganhar_moedas(qtd)
        self.gerenciador.salvar_jogadora(self.jogadora)

    def _desbloquear(self, texto: str):
        if self.jogadora.desbloquear(texto):
            self.gerenciador.salvar_jogadora(self.jogadora)
            messagebox.showinfo("🏆 CONQUISTA DESBLOQUEADA!", f"✨ {texto}")

    def _salvar_config(self):
        self.config.dificuldade  = self.diff.get()
        self.config.tema_cartas  = self.tema_cartas.get()
        self.config.salvar()

    # ─────────────────────────────────────────────────────────────────────────
    # TELA DE PERFIS
    # ─────────────────────────────────────────────────────────────────────────
    def tela_perfis(self):
        self.start_time = None
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)

        self._label(main, "👥 PERFIS DAS FEITICEIRAS 🌸",
                    tamanho=26, bold=True, cor=T("titulo_cor")).pack(pady=(24, 4))
        self._label(main, "Escolha um perfil ou crie um novo:",
                    tamanho=13, cor=T("texto_sec")).pack(pady=(0, 10))

        nomes = self.gerenciador.nomes()
        if not nomes:
            self._label(main, "Nenhum perfil ainda… crie o primeiro! 🌱",
                        tamanho=13, cor=T("texto_sec")).pack(pady=10)
        else:
            lista = tk.Frame(main, bg=T("fundo"))
            lista.pack(pady=4)
            for nome in nomes:
                jog   = self.gerenciador.carregar_jogadora(nome)
                linha = tk.Frame(lista, bg=T("fundo"))
                linha.pack(pady=4)
                tk.Button(
                    linha,
                    text=f"{jog.avatar}  {nome}  —  Nível {jog.level}  —  {jog.titulo()}  —  🪙{jog.moedas}",
                    font=("Arial", 12, "bold"),
                    bg=T("acento"), fg="white", width=46, relief="flat",
                    cursor="hand2",
                    command=lambda n=nome: self.escolher_perfil(n)
                ).pack(side="left", padx=5)
                tk.Button(
                    linha, text="🗑️",
                    font=("Arial", 12, "bold"),
                    bg="#E63946", fg="white", width=4, relief="flat",
                    cursor="hand2",
                    command=lambda n=nome: self.apagar_perfil(n)
                ).pack(side="left")

        # criar novo perfil
        criar = tk.Frame(main, bg=T("fundo"))
        criar.pack(pady=(16, 4))
        self._label(criar, "➕ Nome do novo perfil:", tamanho=12).pack(side="left", padx=6)
        tk.Entry(criar, font=("Arial", 13), width=16,
                 textvariable=self.novo_perfil,
                 bg=T("cartao"), fg=T("texto"), relief="flat",
                 highlightthickness=1, highlightbackground=T("borda")).pack(side="left", padx=5)
        self._botao(criar, "Criar ✨", self.criar_perfil,
                    cor=T("acento2"), fg=T("texto"), largura=8).pack(side="left", padx=5)

        botoes = tk.Frame(main, bg=T("fundo"))
        botoes.pack(pady=16)
        if nomes:
            self._botao(botoes, "📊 COMPARAR PERFIS", self.comparar_perfis).pack(pady=3)
            self._botao(botoes, "🏆 RANKING GERAL",   self.show_ranking).pack(pady=3)
        self._botao(botoes, "♻️ RESETAR TUDO", self.resetar_tudo, cor="#E63946").pack(pady=(10,3))
        self._botao(botoes, "🚪 SAIR",          self.sair_do_jogo, cor="#888888").pack(pady=3)

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
        # Aplicar tema da jogadora se ela tiver um desbloqueado
        if self.jogadora.temas_desbloqueados:
            ultimo = self.config.tema_visual
            if ultimo in self.jogadora.temas_desbloqueados:
                self._mudar_tema(ultimo, salvar=False)
        self.home()

    def apagar_perfil(self, nome: str):
        if messagebox.askyesno("Apagar perfil",
                               f"Apagar '{nome}' para sempre? 🌙\nTodo o progresso será perdido."):
            self.gerenciador.apagar(nome)
            if self.jogadora and self.jogadora.nome == nome:
                self.jogadora = None
            self.tela_perfis()

    # ─────────────────────────────────────────────────────────────────────────
    # HOME
    # ─────────────────────────────────────────────────────────────────────────
    def home(self):
        if not self.jogadora:
            self.tela_perfis()
            return
        self.start_time = None
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)

        self._label(main, "🎀 Memory Game Kawaii RPG v10 🌸",
                    tamanho=28, bold=True, cor=T("titulo_cor")).pack(pady=(14, 4))

        # painel de perfil
        nivel_frame = tk.Frame(main, bg=T("cartao"), relief="flat", bd=0)
        nivel_frame.pack(padx=30, pady=4, fill="x")
        self._label(nivel_frame,
                    f"{self.jogadora.avatar}  {self.jogadora.nome}  |  👑 Nível {self.jogadora.level}  |  {self.jogadora.titulo()}  |  🪙 {self.jogadora.moedas}",
                    tamanho=14, bold=True, cor=T("titulo_cor"), bg=T("cartao")).pack(pady=(8,2))
        self._label(nivel_frame,
                    f"🎮 Jogos: {self.jogadora.stats['games_played']}  |  🏆 Vitórias: {self.jogadora.stats['games_won']}  |  🎯 Acurácia: {self.jogadora.acuracia()}%",
                    tamanho=11, cor=T("texto_sec"), bg=T("cartao")).pack(pady=(0, 8))

        # barra de XP animada
        self._barra_xp(main)

        # mascote
        mascote = tk.Frame(main, bg=T("mascote_bg"), relief="flat", bd=0)
        mascote.pack(padx=30, pady=4, fill="x")
        self._label(mascote, f"🦋 Cirilla: {random.choice(FALAS_INICIO)}",
                    tamanho=12, cor=T("texto"), bg=T("mascote_bg")).pack(padx=10, pady=6)

        # configurações
        cfg = tk.Frame(main, bg=T("fundo"))
        cfg.pack(pady=6)

        self._label(cfg, "Dificuldade:", tamanho=12, cor=T("texto")).grid(row=0, column=0, padx=8, sticky="e")
        d_inner = tk.Frame(cfg, bg=T("fundo"))
        d_inner.grid(row=0, column=1, padx=6)
        for d in Dificuldade:
            tk.Radiobutton(
                d_inner, text=d.value, variable=self.diff, value=d.value,
                font=("Arial", 11), bg=T("fundo"), fg=T("texto"),
                selectcolor=T("cartao"), activebackground=T("fundo")
            ).pack(side="left", padx=5)

        self._label(cfg, "Tema das cartas:", tamanho=12, cor=T("texto")).grid(row=1, column=0, padx=8, pady=4, sticky="e")
        t_inner = tk.Frame(cfg, bg=T("fundo"))
        t_inner.grid(row=1, column=1, padx=6, pady=4)
        for nome_tema in TEMAS_CARTAS:
            tk.Radiobutton(
                t_inner, text=nome_tema, variable=self.tema_cartas, value=nome_tema,
                font=("Arial", 10), bg=T("fundo"), fg=T("texto"),
                selectcolor=T("cartao"), activebackground=T("fundo")
            ).pack(side="left", padx=4)

        # botões principais (2 colunas)
        botoes = tk.Frame(main, bg=T("fundo"))
        botoes.pack(pady=8)

        col1 = tk.Frame(botoes, bg=T("fundo"))
        col1.pack(side="left", padx=12)
        col2 = tk.Frame(botoes, bg=T("fundo"))
        col2.pack(side="left", padx=12)

        self._botao(col1, "🎮 JOGAR",            self.new_game).pack(pady=3)
        if FileManager.existe(SAVE_GAME_FILE):
            self._botao(col1, "▶️ CONTINUAR JOGO", self.continuar_jogo, cor="#7CBB8A").pack(pady=3)
        self._botao(col1, "🛍️ LOJA",             self.show_loja,        cor=T("acento2"), fg=T("texto")).pack(pady=3)
        self._botao(col1, "🎨 TEMA VISUAL",       self.show_temas_visuais, cor=T("acento2"), fg=T("texto")).pack(pady=3)

        self._botao(col2, "👑 MEU PERFIL",        self.show_profile).pack(pady=3)
        self._botao(col2, "🏆 RANKING",           self.show_ranking,     cor=T("acento2"), fg=T("texto")).pack(pady=3)
        self._botao(col2, "⭐ CONQUISTAS",         self.show_achievements, cor=T("acento2"), fg=T("texto")).pack(pady=3)
        self._botao(col2, "📜 HISTÓRICO",         self.show_historico,   cor=T("acento2"), fg=T("texto")).pack(pady=3)
        self._botao(col2, "📊 COMPARAR PERFIS",   self.comparar_perfis,  cor=T("acento2"), fg=T("texto")).pack(pady=3)
        self._botao(col2, "👥 TROCAR PERFIL",     self.tela_perfis,      cor="#888888").pack(pady=3)

    # ─────────────────────────────────────────────────────────────────────────
    # LOJA 🛍️
    # ─────────────────────────────────────────────────────────────────────────
    def show_loja(self):
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)

        self._label(main, "🛍️ LOJA DA ACADEMIA 🪙",
                    tamanho=24, bold=True, cor=T("titulo_cor")).pack(pady=(20, 4))
        self._label(main, f"Seu saldo: 🪙 {self.jogadora.moedas} moedas",
                    tamanho=13, cor=T("texto_sec")).pack(pady=(0, 12))

        notebook = ttk.Notebook(main)
        notebook.pack(padx=20, pady=4, fill="both", expand=True)

        # ── aba avatares ─────────────────────────────────────────────────────
        aba_av = tk.Frame(notebook, bg=T("fundo"))
        notebook.add(aba_av, text="🦋 Avatares")
        self._label(aba_av, "Escolha seu avatar:",
                    tamanho=12, cor=T("texto")).pack(pady=8)
        for nome_av, info in AVATARES.items():
            desbloqueado = nome_av in self.jogadora.avatares_desbloqueados
            equipado     = self.jogadora.avatar == nome_av
            linha = tk.Frame(aba_av, bg=T("cartao"), relief="flat")
            linha.pack(padx=30, pady=3, fill="x")
            self._label(linha, f"{nome_av}",
                        tamanho=12, cor=T("texto"), bg=T("cartao")).pack(side="left", padx=12, pady=6)
            if equipado:
                self._label(linha, "✅ Equipado",
                            tamanho=11, cor="#7CBB8A", bg=T("cartao")).pack(side="right", padx=12)
            elif desbloqueado:
                tk.Button(
                    linha, text="Equipar 🎽",
                    font=("Arial", 10, "bold"), bg=T("acento"), fg="white",
                    relief="flat", cursor="hand2",
                    command=lambda n=nome_av: self._equipar_avatar(n)
                ).pack(side="right", padx=12, pady=4)
            else:
                tk.Button(
                    linha, text=f"Comprar 🪙 {info['preco']}",
                    font=("Arial", 10, "bold"), bg="#D4AF37", fg="white",
                    relief="flat", cursor="hand2",
                    command=lambda n=nome_av, p=info['preco']: self._comprar_avatar(n, p)
                ).pack(side="right", padx=12, pady=4)

        # ── aba cosméticos ───────────────────────────────────────────────────
        aba_cos = tk.Frame(notebook, bg=T("fundo"))
        notebook.add(aba_cos, text="✨ Cosméticos")
        self._label(aba_cos, "Cosméticos e melhorias:",
                    tamanho=12, cor=T("texto")).pack(pady=8)
        for nome_cos, info in COSMETICOS_LOJA.items():
            desbloqueado = nome_cos in self.jogadora.cosmeticos_desbloqueados
            linha = tk.Frame(aba_cos, bg=T("cartao"), relief="flat")
            linha.pack(padx=30, pady=3, fill="x")
            self._label(linha, nome_cos,
                        tamanho=12, cor=T("texto"), bg=T("cartao")).pack(side="left", padx=12, pady=6)
            if desbloqueado:
                self._label(linha, "✅ Desbloqueado",
                            tamanho=11, cor="#7CBB8A", bg=T("cartao")).pack(side="right", padx=12)
            else:
                tk.Button(
                    linha, text=f"Comprar 🪙 {info['preco']}",
                    font=("Arial", 10, "bold"), bg="#D4AF37", fg="white",
                    relief="flat", cursor="hand2",
                    command=lambda n=nome_cos, p=info['preco']: self._comprar_cosmetico(n, p)
                ).pack(side="right", padx=12, pady=4)

        self._botao_voltar(main, self.home)

    def _equipar_avatar(self, nome: str):
        self.jogadora.avatar = nome
        self.gerenciador.salvar_jogadora(self.jogadora)
        messagebox.showinfo("🎽 Avatar equipado!", f"Você agora é {nome}! ✨")
        self.show_loja()

    def _comprar_avatar(self, nome: str, preco: int):
        if not self.jogadora.gastar_moedas(preco):
            messagebox.showinfo("🪙 Saldo insuficiente!",
                                f"Você precisa de 🪙 {preco} moedas.\nVoce tem: 🪙 {self.jogadora.moedas}")
            return
        self.jogadora.avatares_desbloqueados.append(nome)
        self.jogadora.avatar = nome
        self.gerenciador.salvar_jogadora(self.jogadora)
        Som.compra()
        messagebox.showinfo("✨ Compra realizada!", f"Avatar {nome} desbloqueado e equipado!")
        self.show_loja()

    def _comprar_cosmetico(self, nome: str, preco: int):
        if not self.jogadora.gastar_moedas(preco):
            messagebox.showinfo("🪙 Saldo insuficiente!",
                                f"Você precisa de 🪙 {preco} moedas.\nVoce tem: 🪙 {self.jogadora.moedas}")
            return
        self.jogadora.cosmeticos_desbloqueados.append(nome)
        self.gerenciador.salvar_jogadora(self.jogadora)
        Som.compra()
        messagebox.showinfo("✨ Compra realizada!", f"{nome} desbloqueado!")
        self.show_loja()

    # ─────────────────────────────────────────────────────────────────────────
    # TEMAS VISUAIS 🎨
    # ─────────────────────────────────────────────────────────────────────────
    def show_temas_visuais(self):
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)

        self._label(main, "🎨 TEMAS VISUAIS",
                    tamanho=24, bold=True, cor=T("titulo_cor")).pack(pady=(20, 4))
        self._label(main, f"Saldo: 🪙 {self.jogadora.moedas}  |  Tema ativo: {_TEMA_ATUAL}",
                    tamanho=12, cor=T("texto_sec")).pack(pady=(0, 12))

        for nome_tema, info in TEMAS_LOJA.items():
            desbloqueado = nome_tema in self.jogadora.temas_desbloqueados
            ativo        = _TEMA_ATUAL == nome_tema
            t            = TEMAS_VISUAIS[nome_tema]

            linha = tk.Frame(main, bg=t["cartao"], relief="flat", bd=0)
            linha.pack(padx=40, pady=5, fill="x")

            # preview de cor
            preview = tk.Frame(linha, bg=t["acento"], width=40, height=40)
            preview.pack(side="left", padx=10, pady=8)
            preview.pack_propagate(False)

            self._label(linha, f"{nome_tema}",
                        tamanho=13, bold=True, cor=t["titulo_cor"],
                        bg=t["cartao"]).pack(side="left", padx=8, pady=8)

            if ativo:
                self._label(linha, "🌟 ATIVO",
                            tamanho=11, cor="#7CBB8A", bg=t["cartao"]).pack(side="right", padx=14)
            elif desbloqueado:
                tk.Button(
                    linha, text="Ativar ✅",
                    font=("Arial", 10, "bold"), bg=t["acento"], fg="white",
                    relief="flat", cursor="hand2",
                    command=lambda n=nome_tema: self._ativar_tema(n)
                ).pack(side="right", padx=12, pady=6)
            else:
                tk.Button(
                    linha, text=f"Comprar 🪙 {info['preco']}",
                    font=("Arial", 10, "bold"), bg="#D4AF37", fg="white",
                    relief="flat", cursor="hand2",
                    command=lambda n=nome_tema, p=info['preco']: self._comprar_tema(n, p)
                ).pack(side="right", padx=12, pady=6)

        self._botao_voltar(main, self.home)

    def _ativar_tema(self, nome: str):
        self._mudar_tema(nome)
        messagebox.showinfo("🎨 Tema ativado!", f"Tema '{nome}' ativado! ✨")
        self.show_temas_visuais()

    def _comprar_tema(self, nome: str, preco: int):
        if not self.jogadora.gastar_moedas(preco):
            messagebox.showinfo("🪙 Saldo insuficiente!",
                                f"Você precisa de 🪙 {preco} moedas.")
            return
        self.jogadora.temas_desbloqueados.append(nome)
        self.gerenciador.salvar_jogadora(self.jogadora)
        self._mudar_tema(nome)
        Som.compra()
        messagebox.showinfo("✨ Tema comprado!", f"Tema '{nome}' ativo!")
        self.show_temas_visuais()

    # ─────────────────────────────────────────────────────────────────────────
    # PERFIL / CONQUISTAS / HISTÓRICO / RANKING / COMPARAR
    # ─────────────────────────────────────────────────────────────────────────
    def show_profile(self):
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)
        self._label(main, "👑 MEU PERFIL 👑",
                    tamanho=26, bold=True, cor=T("titulo_cor")).pack(pady=18)

        frame = tk.Frame(main, bg=T("cartao"), relief="flat", bd=0)
        frame.pack(padx=30, pady=10, fill="both")

        melhor = self.jogadora.stats["best_time"]
        media  = (self.jogadora.stats["total_time"] // max(self.jogadora.stats["games_won"], 1))
        linhas = [
            f"👤 Nome:          {self.jogadora.nome}",
            f"{self.jogadora.avatar}  Avatar equipado",
            f"👑 Título:        {self.jogadora.titulo()}",
            f"⭐ Nível:         {self.jogadora.level}",
            f"💜 XP Total:      {self.jogadora.xp}",
            f"🪙 Moedas:        {self.jogadora.moedas}",
            f"🎮 Jogos jogados: {self.jogadora.stats['games_played']}",
            f"🏆 Vitórias:      {self.jogadora.stats['games_won']}",
            f"🎯 Acurácia:      {self.jogadora.acuracia()}%",
            f"⏱️ Melhor tempo:  {melhor}s" if melhor else "⏱️ Melhor tempo:  —",
            f"⌛ Média de tempo: {media}s",
            f"🔥 Cosméticos:    {len(self.jogadora.cosmeticos_desbloqueados)} desbloqueados",
        ]
        for l in linhas:
            self._label(frame, l, tamanho=12, cor=T("texto"), bg=T("cartao")).pack(
                anchor="w", padx=20, pady=2)

        self._barra_xp(frame)
        self._botao_voltar(main, self.home)

    def show_ranking(self):
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)
        self._label(main, "🏆 RANKING POR DIFICULDADE 🏆",
                    tamanho=24, bold=True, cor=T("titulo_cor")).pack(pady=18)
        self._subtitulo_perfil(main)

        notebook = ttk.Notebook(main)
        notebook.pack(padx=20, pady=4, fill="both", expand=True)

        medalhas = {0: "🥇", 1: "🥈", 2: "🥉"}
        for d in Dificuldade:
            aba   = tk.Frame(notebook, bg=T("fundo"))
            notebook.add(aba, text=d.value)
            lista = self.ranking.lista_para(d.value)
            if not lista:
                self._label(aba, "Sem resultados ainda para esta dificuldade 🌸",
                            tamanho=13, cor=T("texto_sec")).pack(pady=30)
            else:
                for i, p in enumerate(lista):
                    bg_cor = T("acento") if i == 0 else T("cartao")
                    self._label(
                        aba,
                        f"  {medalhas.get(i, f'{i+1}.')}  {p['name']}  —  Score: {p['score']}  —  ⏱️ {p['time']}s  —  Nível {p['level']}",
                        tamanho=12, cor=T("texto"), bg=bg_cor
                    ).pack(padx=10, pady=5, fill="x")

        tk.Button(main, text="♻️ Resetar Ranking",
                  font=("Arial", 11, "bold"), bg="#E63946", fg="white",
                  relief="flat", cursor="hand2", width=22,
                  command=self.resetar_ranking).pack(pady=(8, 0))
        destino = self.home if self.jogadora else self.tela_perfis
        self._botao_voltar(main, destino)

    def show_achievements(self):
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)
        self._label(main, "⭐ CONQUISTAS ⭐",
                    tamanho=24, bold=True, cor=T("titulo_cor")).pack(pady=18)
        self._subtitulo_perfil(main)

        todas = [
            "Primeira Vitória 🏆",    "Velocista ⚡",
            "Mestre da Memória 🧙‍♀️",  "Campeã Fácil 🌸",
            "Campeã Médio 💜",         "Campeã Difícil 🔥",
            "Campeã Mestre 🔥🔥",      "10 Vitórias 🎉",
            "Nível 10 👑",              "Perfecta 💯",
            "Speedrun Master ⚡⚡⚡",   "Streak Master 🔥🔥🔥",
            "Colecionadora 🛍️",        "Multimilionária 🪙",
        ]
        frame = tk.Frame(main, bg=T("cartao"), relief="flat")
        frame.pack(padx=30, pady=10, fill="both")

        col1 = tk.Frame(frame, bg=T("cartao"))
        col1.pack(side="left", fill="both", expand=True)
        col2 = tk.Frame(frame, bg=T("cartao"))
        col2.pack(side="left", fill="both", expand=True)

        for i, c in enumerate(todas):
            alvo = col1 if i % 2 == 0 else col2
            if c in self.jogadora.achievements:
                bg_cor  = T("acento2")
                texto_c = f"✓ {c}"
                cor_txt = T("texto")
            else:
                bg_cor  = T("cartao")
                texto_c = f"🔒 {c}"
                cor_txt = T("texto_sec")
            self._label(alvo, texto_c, tamanho=11, cor=cor_txt, bg=bg_cor).pack(
                padx=10, pady=5, fill="x")

        self._botao_voltar(main, self.home)

    def show_historico(self):
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)
        self._label(main, "📜 HISTÓRICO DE PARTIDAS",
                    tamanho=24, bold=True, cor=T("titulo_cor")).pack(pady=18)
        self._subtitulo_perfil(main)

        hist = self.jogadora.historico
        if not hist:
            self._label(main, "Nenhuma partida ainda… Jogue primeiro! 🎮",
                        tamanho=13, cor=T("texto_sec")).pack(pady=40)
        else:
            frame = tk.Frame(main, bg=T("cartao"), relief="flat")
            frame.pack(padx=30, pady=10, fill="both")
            self._label(frame,
                        "  #  │  Data & Hora          │  Dificuldade   │  Tempo  │  Resultado",
                        tamanho=11, cor=T("texto"), bg=T("status_bg")).pack(padx=8, pady=6, fill="x")
            for i, h in enumerate(hist, 1):
                resultado = "✅ Vitória" if h["vitoria"] else "❌ Derrota"
                linha     = (f"  {i}  │  {h['data']}  │  "
                             f"{h['dificuldade']:<14}│  {h['tempo']:>4}s  │  {resultado}")
                bg_cor = T("acento2") if h["vitoria"] else T("cartao")
                self._label(frame, linha, tamanho=11, cor=T("texto"), bg=bg_cor).pack(
                    padx=8, pady=3, fill="x")

        self._botao_voltar(main, self.home)

    def comparar_perfis(self):
        self.clear()
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)
        self._label(main, "📊 COMPARAR PERFIS",
                    tamanho=24, bold=True, cor=T("titulo_cor")).pack(pady=20)

        nomes = self.gerenciador.nomes()
        if not nomes:
            self._label(main, "Nenhum perfil pra comparar ainda… 🌱",
                        tamanho=14, cor=T("texto_sec")).pack(pady=40)
        else:
            jogadoras = sorted(
                [self.gerenciador.carregar_jogadora(n) for n in nomes],
                key=lambda j: j.xp, reverse=True
            )
            medalhas = {0: "🥇", 1: "🥈", 2: "🥉"}
            frame    = tk.Frame(main, bg=T("cartao"), relief="flat")
            frame.pack(padx=30, pady=10, fill="both")
            for pos, jog in enumerate(jogadoras):
                bg_cor = T("acento") if pos == 0 else T("cartao")
                texto  = (
                    f"  {medalhas.get(pos, f'{pos+1}º')}  {jog.avatar} {jog.nome}  │  "
                    f"{jog.titulo()}  │  ⭐ Nível {jog.level}  │  "
                    f"💜 XP {jog.xp}  │  🏆 {jog.stats['games_won']} vitórias  │  "
                    f"🎯 {jog.acuracia()}%  │  🪙 {jog.moedas}"
                )
                self._label(frame, texto, tamanho=11, cor=T("texto"), bg=bg_cor).pack(
                    padx=10, pady=6, fill="x")

        self._botao_voltar(main, self.tela_perfis if not self.jogadora else self.home)

    # ─────────────────────────────────────────────────────────────────────────
    # RESETAR / SAIR
    # ─────────────────────────────────────────────────────────────────────────
    def resetar_tudo(self):
        if messagebox.askyesno("♻️ Resetar tudo",
                               "Isso vai APAGAR:\n• Todos os perfis 👥\n• O ranking 🥇\n• A partida salva 💾\n\nTem certeza?"):
            self.gerenciador.resetar_todos()
            self.ranking.resetar()
            FileManager.apagar(SAVE_GAME_FILE)
            self.jogadora = None
            messagebox.showinfo("✨ Tudo limpo!", "A Academia recomeçou do zero. 🌱")
            self.tela_perfis()

    def resetar_ranking(self):
        if messagebox.askyesno("♻️ Resetar ranking", "Apagar todo o ranking?\nOs perfis continuam intactos."):
            self.ranking.resetar()
            messagebox.showinfo("✨ Pronto!", "Ranking zerado! 🌸")
            self.show_ranking()

    def sair_do_jogo(self):
        if messagebox.askyesno("Sair", "Quer mesmo fechar a Academia? 🌙✨"):
            self.root.destroy()

    # ─────────────────────────────────────────────────────────────────────────
    # SALVAR / CARREGAR PARTIDA
    # ─────────────────────────────────────────────────────────────────────────
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
            "tema_cartas": self.tema_cartas.get(),
            "nome":        self.jogadora.nome,
            "tempo":       elapsed,
            "streak":      self.streak,
        }
        FileManager.gravar(SAVE_GAME_FILE, estado)
        self.start_time = None
        messagebox.showinfo("💾 Jogo salvo!", "Partida guardada no grimório! ✨")
        self.home()

    def _auto_salvar(self):
        """Salvamento automático silencioso a cada par encontrado."""
        if not self.start_time:
            return
        elapsed = self.tempo_acumulado + int(time.time() - self.start_time)
        estado  = {
            "valores":    [c.valor for c in self.cartas],
            "combinadas": [c.indice for c in self.cartas if c.combinada],
            "linhas":     self.rows,
            "colunas":    self.cols,
            "pares":      self.pairs,
            "dificuldade": self.diff.get(),
            "tema_cartas": self.tema_cartas.get(),
            "nome":        self.jogadora.nome,
            "tempo":       elapsed,
            "streak":      self.streak,
        }
        FileManager.gravar(SAVE_GAME_FILE, estado)

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

    # ─────────────────────────────────────────────────────────────────────────
    # PROTEÇÃO: voltar / reiniciar durante partida
    # ─────────────────────────────────────────────────────────────────────────
    def voltar_da_partida(self):
        if messagebox.askyesno("Voltar", "Se voltar agora, perde a partida (salve antes).\nQuer mesmo voltar? 🌙"):
            self.home()

    def reiniciar_partida(self):
        if messagebox.askyesno("Novo jogo", "Recomeçar vai perder a partida atual. Tem certeza? 🔄"):
            self.new_game()

    # ─────────────────────────────────────────────────────────────────────────
    # A PARTIDA 🎮
    # ─────────────────────────────────────────────────────────────────────────
    def _dificuldade_atual(self) -> Dificuldade:
        for d in Dificuldade:
            if d.value == self.diff.get():
                return d
        return Dificuldade.FACIL

    def new_game(self, estado_salvo=None):
        self._salvar_config()
        self.clear()
        self.streak    = 0
        self.primeira  = None
        self.segunda   = None
        self._bloqueado = False

        if estado_salvo is None:
            self.jogadora.stats["games_played"] += 1
            self.gerenciador.salvar_jogadora(self.jogadora)
            rows, cols = GRADE_DIFICULDADE[self._dificuldade_atual()]
            pairs      = (rows * cols) // 2
            icons      = TEMAS_CARTAS[self.tema_cartas.get()][:pairs]
            valores    = icons * 2
            random.shuffle(valores)
            self.cartas          = [Carta(i, v) for i, v in enumerate(valores)]
            self.tempo_acumulado = 0
        else:
            rows   = estado_salvo["linhas"]
            cols   = estado_salvo["colunas"]
            pairs  = estado_salvo["pares"]
            self.diff.set(estado_salvo["dificuldade"])
            self.tema_cartas.set(estado_salvo.get("tema_cartas", "Kawaii 🎀"))
            valores    = estado_salvo["valores"]
            combinadas = set(estado_salvo["combinadas"])
            self.cartas = [Carta(i, v) for i, v in enumerate(valores)]
            for c in self.cartas:
                if c.indice in combinadas:
                    c.marcar_combinada()
            self.tempo_acumulado = estado_salvo["tempo"]
            self.streak          = estado_salvo.get("streak", 0)

        self.rows   = rows
        self.cols   = cols
        self.pairs  = pairs
        total       = rows * cols
        found_ini   = sum(1 for c in self.cartas if c.combinada) // 2
        self.start_time = None

        # ── construção da tela ────────────────────────────────────────────────
        main = tk.Frame(self.root, bg=T("fundo"))
        main.pack(fill="both", expand=True)

        # status bar
        status = tk.Frame(main, bg=T("status_bg"), relief="flat")
        status.pack(padx=12, pady=6, fill="x")
        self._label(status,
                    f"{self.jogadora.avatar} {self.jogadora.nome}  │  Nível {self.jogadora.level}  │  {self.diff.get()}  │  {self.tema_cartas.get()}",
                    tamanho=11, bold=True, cor=T("titulo_cor"), bg=T("status_bg")).pack(side="left", padx=10, pady=6)
        self._label(status, f"🪙 {self.jogadora.moedas}",
                    tamanho=11, bold=True, cor=T("titulo_cor"), bg=T("status_bg")).pack(side="right", padx=10)
        self.timer = self._label(status, "⏱️ 00:00",
                                 tamanho=11, bold=True, cor=T("titulo_cor"), bg=T("status_bg"))
        self.timer.pack(side="right", padx=10)
        self.progress_lbl = self._label(status, f"🎁 Pares: {found_ini}/{pairs}",
                                        tamanho=11, bold=True, cor=T("titulo_cor"), bg=T("status_bg"))
        self.progress_lbl.pack(side="right", padx=10)

        # barra de XP inline (animada)
        xp_frame = tk.Frame(main, bg=T("fundo"))
        xp_frame.pack(fill="x", padx=12, pady=(0, 2))
        xp_atual = self.jogadora.xp_no_nivel()
        xp_max   = self.jogadora.xp_para_proximo()
        pct      = xp_atual / xp_max
        self.xp_canvas = tk.Canvas(xp_frame, width=500, height=18,
                                   bg=T("cartao"), highlightthickness=1,
                                   highlightbackground=T("borda"))
        self.xp_canvas.pack(side="left", padx=8)
        self.xp_canvas.create_rectangle(0, 0, int(500 * pct), 18, fill=T("barra_xp"), outline="")
        self.xp_canvas.create_text(250, 9,
                                   text=f"XP Nível {self.jogadora.level}: {xp_atual}/{xp_max}",
                                   font=("Arial", 9, "bold"), fill=T("texto"))

        self.streak_lbl = self._label(xp_frame, f"🔥 Streak: {self.streak}",
                                      tamanho=10, bold=True, cor=T("titulo_cor"))
        self.streak_lbl.pack(side="left", padx=12)

        # mascote
        self.mascote_label = self._label(
            main, "🦋 Cirilla: boa sorte! 💖",
            tamanho=12, bold=True, cor=T("texto"), bg=T("mascote_bg")
        )
        self.mascote_label.pack(pady=(2, 4), ipady=4, padx=12, fill="x")

        # tabuleiro
        board = tk.Frame(main, bg=T("fundo"))
        board.pack(padx=10, pady=4)

        # tamanho do botão inversamente proporcional ao grid
        btn_w = max(3, 7 - cols // 2)
        btn_h = max(1, 3 - rows // 4)
        fonte_size = max(14, 28 - cols * 2)

        self.btns: list[tk.Button] = []
        for i in range(total):
            btn = tk.Button(
                board, text="", width=btn_w, height=btn_h,
                font=("Arial", fonte_size, "bold"),
                bg=btn_cor(i), activebackground=T("acento2"),
                relief="raised", bd=2, cursor="hand2",
                command=lambda x=i: self.flip(x)
            )
            btn.grid(row=i // cols, column=i % cols, padx=3, pady=3)
            self.btns.append(btn)

        # controles
        ctrl = tk.Frame(main, bg=T("fundo"))
        ctrl.pack(pady=8)
        for texto, cor, cmd in [
            ("🔙 Voltar",        T("acento2"), self.voltar_da_partida),
            ("🔄 Novo Jogo",     T("acento"),  self.reiniciar_partida),
            ("💾 Salvar e Sair", "#7CBB8A",    self.salvar_jogo),
            ("🚪 Sair",          "#888888",    self.sair_do_jogo),
        ]:
            tk.Button(ctrl, text=texto, font=("Arial", 10, "bold"),
                      bg=cor, fg="white", width=14, relief="flat",
                      cursor="hand2", command=cmd).pack(side="left", padx=4)

        if estado_salvo is None:
            self.show_cards_memory()
        else:
            self._restaurar_tabuleiro()

    # ── restaurar jogo salvo ──────────────────────────────────────────────────
    def _restaurar_tabuleiro(self):
        for carta in self.cartas:
            if carta.combinada:
                self.btns[carta.indice].config(
                    text=carta.valor, state="disabled",
                    bg=T("acento2"), relief="sunken")
        self.mascote_label.config(text="🦋 Cirilla: bem-vinda de volta! 🌙",
                                  bg=T("mascote_bg"))
        self.start_time = time.time()
        self.update_timer()

    # ── memorização ───────────────────────────────────────────────────────────
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
                text=f"🧠 Memorize! Escondendo em {self.segundos_memo}s…",
                bg="#FDFFB6" if _TEMA_ATUAL == "Kawaii 🎀" else T("cartao"))
            self.segundos_memo -= 1
            self.root.after(1000, self._contar_memo)
        else:
            self.mascote_label.config(
                text="🎮 Valendo! Encontre os pares! 💪",
                bg=T("mascote_bg"))
            self._iniciar_jogo_real()

    def _iniciar_jogo_real(self):
        for i, btn in enumerate(self.btns):
            if not self.cartas[i].combinada:
                btn.config(text="", state="normal")
        self.start_time = time.time()
        self.update_timer()

    # ── cronômetro ────────────────────────────────────────────────────────────
    def update_timer(self):
        if not self.timer.winfo_exists():
            return
        combinados = sum(1 for c in self.cartas if c.combinada)
        if self.start_time and combinados < self.pairs * 2:
            elapsed = self.tempo_acumulado + int(time.time() - self.start_time)
            self.timer.config(text=f"⏱️ {elapsed//60:02d}:{elapsed%60:02d}")
            self.root.after(1000, self.update_timer)

    # ── animação de virar carta ───────────────────────────────────────────────
    def _animar_carta(self, idx: int, valor: str):
        btn    = self.btns[idx]
        flashes = [T("acento2"), T("acento"), T("fundo"), T("acento")]

        def passo(n):
            if n < len(flashes):
                btn.config(bg=flashes[n])
                self.root.after(45, lambda: passo(n + 1))
            else:
                btn.config(text=valor, relief="sunken")

        passo(0)

    # ── virar carta ───────────────────────────────────────────────────────────
    def flip(self, i: int):
        carta = self.cartas[i]
        if carta.combinada or carta.virada or self._bloqueado:
            return
        if self.primeira and self.segunda:
            return

        carta.virar()
        self._animar_carta(i, carta.valor)

        if self.primeira is None:
            self.primeira = carta
        else:
            self.segunda    = carta
            self._bloqueado = True
            for btn in self.btns:
                btn.config(state="disabled")
            self.root.after(700, self.check_match)

    # ── conferir par ──────────────────────────────────────────────────────────
    def check_match(self):
        a, b = self.primeira, self.segunda
        self.jogadora.stats["total_tentativas"] += 1

        if a.valor == b.valor:
            # ✅ par encontrado
            a.marcar_combinada()
            b.marcar_combinada()
            for idx in (a.indice, b.indice):
                self.btns[idx].config(state="disabled",
                                      bg=T("acento2"), relief="sunken")

            self.jogadora.stats["total_acertos"] += 1
            self.streak += 1
            self.streak_lbl.config(text=f"🔥 Streak: {self.streak}")

            if self.streak > 0 and self.streak % STREAK_TRIGGER == 0:
                self.mascote_label.config(
                    text=f"🦋 Cirilla: {random.choice(FALAS_STREAK)}",
                    bg=T("mascote_bg"))
                self._ganhar_xp(XP_STREAK)
                self._ganhar_moedas(MOEDAS_STREAK)
                Som.streak()
                self._desbloquear("Streak Master 🔥🔥🔥")
            else:
                self.mascote_label.config(
                    text=f"🦋 Cirilla: {random.choice(FALAS_ACERTO)}",
                    bg=T("mascote_bg"))
                Som.acerto()

            self._ganhar_xp(XP_ACERTO)
            self._ganhar_moedas(MOEDAS_ACERTO)
            self._atualizar_barra_xp_inline()
            self._auto_salvar()  # 💾 auto-salva a cada par

        else:
            # ❌ par errado
            self.root.after(100, lambda: [
                self.btns[a.indice].config(text="", bg=btn_cor(a.indice), relief="raised"),
                self.btns[b.indice].config(text="", bg=btn_cor(b.indice), relief="raised"),
            ])
            a.esconder()
            b.esconder()
            self.mascote_label.config(
                text=f"🦋 Cirilla: {random.choice(FALAS_ERRO)}",
                bg=T("mascote_bg"))
            Som.erro()
            self.streak = 0
            self.streak_lbl.config(text=f"🔥 Streak: {self.streak}")

        self.primeira    = None
        self.segunda     = None
        self._bloqueado  = False

        # reabilitar cartas não combinadas
        for carta in self.cartas:
            if not carta.combinada:
                self.btns[carta.indice].config(state="normal")

        combinados = sum(1 for c in self.cartas if c.combinada)
        self.progress_lbl.config(text=f"🎁 Pares: {combinados//2}/{self.pairs}")
        self.gerenciador.salvar_jogadora(self.jogadora)

        if combinados == self.pairs * 2:
            self.vitoria()

    # ── vitória ───────────────────────────────────────────────────────────────
    def vitoria(self):
        elapsed     = self.tempo_acumulado + int(time.time() - self.start_time)
        self.start_time = None

        self.jogadora.stats["games_won"]  += 1
        self.jogadora.stats["total_time"] += elapsed
        if (self.jogadora.stats["best_time"] is None
                or elapsed < self.jogadora.stats["best_time"]):
            self.jogadora.stats["best_time"] = elapsed

        diff_atual = self._dificuldade_atual()
        self.jogadora.registrar_partida(elapsed, self.diff.get(), vitoria=True)
        self.gerenciador.salvar_jogadora(self.jogadora)

        self._ganhar_xp(XP_VITORIA)
        self._ganhar_moedas(MOEDAS_VITORIA)

        # conquistas
        self._desbloquear("Primeira Vitória 🏆")
        if elapsed <= 60:
            self._desbloquear("Velocista ⚡")
        if elapsed <= 30:
            self._desbloquear("Speedrun Master ⚡⚡⚡")
        if diff_atual == Dificuldade.DIFICIL:
            self._desbloquear("Campeã Difícil 🔥")
        if diff_atual == Dificuldade.MESTRE:
            self._desbloquear("Campeã Mestre 🔥🔥")
            self._desbloquear("Mestre da Memória 🧙‍♀️")
        if diff_atual == Dificuldade.FACIL:
            self._desbloquear("Campeã Fácil 🌸")
        if diff_atual == Dificuldade.MEDIO:
            self._desbloquear("Campeã Médio 💜")
        if self.jogadora.stats["games_won"] >= 10:
            self._desbloquear("10 Vitórias 🎉")
        if self.jogadora.level >= 10:
            self._desbloquear("Nível 10 👑")
        if self.jogadora.moedas >= 1000:
            self._desbloquear("Multimilionária 🪙")
        if len(self.jogadora.cosmeticos_desbloqueados) >= 3:
            self._desbloquear("Colecionadora 🛍️")

        FileManager.apagar(SAVE_GAME_FILE)
        self.ranking.adicionar(
            self.jogadora.nome, self.jogadora.xp, elapsed,
            self.jogadora.level, self.diff.get()
        )

        Som.vitoria()
        messagebox.showinfo(
            "🎉 VITÓRIA!",
            f"PARABÉNS! 🎉\n\n"
            f"{self.jogadora.avatar}  {self.jogadora.nome}\n"
            f"👑 {self.jogadora.titulo()}\n"
            f"⏱️ Tempo: {elapsed}s\n"
            f"⭐ Nível: {self.jogadora.level}\n"
            f"💜 XP Total: {self.jogadora.xp}\n"
            f"🪙 Moedas: {self.jogadora.moedas}\n"
            f"🎯 Acurácia: {self.jogadora.acuracia()}%\n\n"
            f"Você é incrível! ✨"
        )
        self.home()


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        INICIAR                                      ║
# ╚══════════════════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    root = tk.Tk()
    jogo = KawaiiMemoryGame(root)
    root.mainloop()