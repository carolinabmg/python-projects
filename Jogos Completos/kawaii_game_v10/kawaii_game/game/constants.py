"""
constants.py — Todas as constantes e configurações do jogo.
Nenhum outro módulo define valores "mágicos" — tudo vem daqui.
"""

from enum import Enum


# ══════════════════════════════════════════════════════
# CORES
# ══════════════════════════════════════════════════════
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
GOLD       = "#FFD700"

CORES_BOTOES = [PINK, BLUE, MINT, PEACH, YELLOW, LILAC, PURPLE, CORAL]


# ══════════════════════════════════════════════════════
# XP E NÍVEIS
# ══════════════════════════════════════════════════════
XP_POR_NIVEL   = 100
XP_ACERTO      = 10
XP_VITORIA     = 50
XP_STREAK      = 20
STREAK_TRIGGER = 3
MAX_HISTORICO  = 5

TITULOS: dict[int, str] = {
    1:  "Aprendiz 🌱",
    3:  "Maga do Código 🔮",
    6:  "Arquimaga 👑",
    10: "Lenda Kawaii ✨",
}


def titulo_para_nivel(level: int) -> str:
    """Devolve o título correspondente ao nível."""
    resultado = TITULOS[1]
    for limiar, nome in TITULOS.items():
        if level >= limiar:
            resultado = nome
    return resultado


# ══════════════════════════════════════════════════════
# MOEDAS
# ══════════════════════════════════════════════════════
MOEDAS_VITORIA_FACIL  = 10
MOEDAS_VITORIA_MEDIO  = 20
MOEDAS_VITORIA_DIFICIL = 35
MOEDAS_STREAK_BONUS   = 5   # bônus extra de moedas a cada streak

MOEDAS_POR_DIFICULDADE: dict[str, int] = {
    "Fácil":  MOEDAS_VITORIA_FACIL,
    "Médio":  MOEDAS_VITORIA_MEDIO,
    "Difícil": MOEDAS_VITORIA_DIFICIL,
}


# ══════════════════════════════════════════════════════
# DIFICULDADE
# ══════════════════════════════════════════════════════
class Dificuldade(Enum):
    FACIL   = "Fácil"
    MEDIO   = "Médio"
    DIFICIL = "Difícil"


GRADE_DIFICULDADE: dict[Dificuldade, tuple[int, int]] = {
    Dificuldade.FACIL:   (4, 4),
    Dificuldade.MEDIO:   (4, 5),
    Dificuldade.DIFICIL: (6, 6),
}


# ══════════════════════════════════════════════════════
# TEMAS DE CARTAS (emojis — base gratuita)
# ══════════════════════════════════════════════════════
TEMAS: dict[str, list[str]] = {
    "Kawaii 🎀": [
        "🌸","🎀","🧸","🩷","🦋","🌙",
        "🍓","🧁","⭐","🍀","🐱","💎",
        "🌈","🦄","🍭","🌼","🎵","☁️",
    ],
    "Natureza 🌿": [
        "🌲","🌺","🍄","🐸","🌊","🦊",
        "🐝","🌻","🍁","🦜","🐚","🌍",
        "🦋","🌿","🐠","🍃","🌙","⛰️",
    ],
    "Comida 🍕": [
        "🍕","🍣","🍩","🌮","🍜","🍓",
        "🧁","🍦","🍇","🥑","🍋","🥐",
        "🍔","🍿","🥞","🍰","🥭","🫐",
    ],
    "Espaço 🚀": [
        "🚀","🌙","⭐","🪐","☄️","🌌",
        "👾","🛸","🔭","💫","🌠","🪨",
        "🌟","🌑","🛰️","🌞","🌀","🔮",
    ],
    "Halloween 🎃": [
        "🎃","👻","🦇","🕷️","🕸️","🧙",
        "💀","🌕","🔮","🪄","🧪","🦉",
        "🐍","🌙","⚡","🖤","🩸","🪦",
    ],
    "Natal 🎄": [
        "🎄","⛄","🎅","🦌","🎁","🔔",
        "❄️","🌟","🕯️","🧦","🍪","🥛",
        "🎶","🏔️","🌨️","🧤","🎿","🪔",
    ],
}

# Temas que precisam ser desbloqueados na loja
TEMAS_BASE    = {"Kawaii 🎀", "Natureza 🌿"}   # disponíveis desde o início
TEMAS_PREMIUM = {"Comida 🍕", "Espaço 🚀", "Halloween 🎃", "Natal 🎄"}


# ══════════════════════════════════════════════════════
# LOJA — CATÁLOGO DE SKINS
# ══════════════════════════════════════════════════════
CATALOGO_LOJA: list[dict] = [
    {
        "id":        "tema_comida",
        "nome":      "Comida 🍕",
        "descricao": "Delícias gastronômicas nas cartas!",
        "preco":     30,
        "tipo":      "tema",
        "chave":     "Comida 🍕",
        "preview":   "🍕🍣🍩🌮",
    },
    {
        "id":        "tema_espaco",
        "nome":      "Espaço 🚀",
        "descricao": "Explore o cosmos nas suas cartas.",
        "preco":     30,
        "tipo":      "tema",
        "chave":     "Espaço 🚀",
        "preview":   "🚀🌙⭐🪐",
    },
    {
        "id":        "tema_halloween",
        "nome":      "Halloween 🎃",
        "descricao": "Tema assustador pra noites de treino.",
        "preco":     50,
        "tipo":      "tema",
        "chave":     "Halloween 🎃",
        "preview":   "🎃👻🦇🕷️",
    },
    {
        "id":        "tema_natal",
        "nome":      "Natal 🎄",
        "descricao": "Espírito natalino em cada carta.",
        "preco":     50,
        "tipo":      "tema",
        "chave":     "Natal 🎄",
        "preview":   "🎄⛄🎅🦌",
    },
]


# ══════════════════════════════════════════════════════
# CONQUISTAS
# ══════════════════════════════════════════════════════
TODAS_CONQUISTAS: list[str] = [
    "Primeira Vitória 🏆",
    "Velocista ⚡",
    "Mestre da Memória 🧙‍♀️",
    "Campeã Fácil 🌸",
    "Campeã Médio 💜",
    "Campeã Difícil 🔥",
    "10 Vitórias 🎉",
    "Nivel 10 👑",
    "Streak Master 🔥🔥🔥",
    "Milionária 💰",
]


# ══════════════════════════════════════════════════════
# ARQUIVOS DE DADOS
# ══════════════════════════════════════════════════════
RANK_FILE      = "ranking_kawaii.json"
PERFIS_FILE    = "perfis_kawaii.json"
SAVE_GAME_FILE = "jogo_salvo_kawaii.json"


# ══════════════════════════════════════════════════════
# FALAS DA MASCOTE
# ══════════════════════════════════════════════════════
FALAS_ACERTO: list[str] = [
    "Isso! Você acertou um par! 💖",
    "Que incrível! ⭐",
    "Você é a melhor! 👑",
    "Mandou bem demais! 🌟",
]
FALAS_STREAK: list[str] = [
    "🔥 STREAK x3! XP e moedas bônus! ✨",
    "🔥 Três seguidos! Você tá voando! 💜",
    "🔥 Combo incrível! Bônus garantido! 🌟",
]
FALAS_ERRO: list[str] = [
    "Quase! Tenta outro par 💭",
    "Calma, você consegue! 🌸",
    "Respira e olha de novo 🦋",
]
FALAS_HOME: list[str] = [
    "Pronta pra treinar a memória? 🎀",
    "Bora subir de nível? ✨",
    "Você consegue, feiticeira! 🌸",
]
