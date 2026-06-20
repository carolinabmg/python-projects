"""
widgets.py — Componentes de UI reutilizáveis.
Cada função recebe um `parent` tkinter e devolve o widget criado.
"""

import tkinter as tk
from .constants import (
    BG, LILAC, BLUE, DARK_TEXT, VIOLET, DEEP_RED, GOLD,
)


def barra_xp(parent, jogadora, largura: int = 400) -> tk.Canvas:
    """
    Desenha a barra de progresso de XP da jogadora.
    Devolve o Canvas criado (pode ser atualizado depois com atualizar_barra_xp).
    """
    frame = tk.Frame(parent, bg=BG)
    frame.pack(pady=(2, 6))

    xp_atual = jogadora.xp_no_nivel_atual()
    xp_max   = jogadora.xp_para_proximo()
    pct      = xp_atual / xp_max

    tk.Label(
        frame,
        text=f"⭐ Nível {jogadora.level} — {xp_atual}/{xp_max} XP",
        font=("Arial", 10, "bold"), bg=BG, fg=VIOLET,
    ).pack()

    canvas = tk.Canvas(
        frame, width=largura, height=18,
        bg="#E8D5F5", highlightthickness=1, highlightbackground=LILAC,
    )
    canvas.pack()
    _desenhar_barra(canvas, largura, pct, f"{int(pct * 100)}%")
    return canvas


def atualizar_barra_xp(canvas: tk.Canvas, jogadora, largura: int = 400):
    """Redesenha a barra de XP num Canvas já existente."""
    if not canvas.winfo_exists():
        return
    xp_atual = jogadora.xp_no_nivel_atual()
    xp_max   = jogadora.xp_para_proximo()
    pct      = xp_atual / xp_max
    canvas.delete("all")
    _desenhar_barra(
        canvas, largura, pct,
        f"XP Nível {jogadora.level}: {xp_atual}/{xp_max}",
    )


def _desenhar_barra(canvas: tk.Canvas, largura: int, pct: float, texto: str):
    canvas.create_rectangle(0, 0, int(largura * pct), 18, fill=LILAC, outline="")
    canvas.create_text(
        largura // 2, 9,
        text=texto, font=("Arial", 9, "bold"), fill=DARK_TEXT,
    )


def botao_padrao(
    parent,
    texto: str,
    comando,
    cor: str = BLUE,
    largura: int = 20,
    fonte_tamanho: int = 12,
) -> tk.Button:
    """Botão com estilo padrão do jogo. Devolve o Button criado."""
    from .constants import YELLOW, PEACH  # importação local pra evitar ciclo
    fg = DARK_TEXT if cor in (YELLOW, PEACH) else "white"
    btn = tk.Button(
        parent,
        text=texto,
        font=("Arial", fonte_tamanho, "bold"),
        bg=cor,
        fg=fg,
        width=largura,
        command=comando,
        relief="raised",
        bd=2,
        cursor="hand2",
    )
    return btn


def label_moedas(parent, jogadora) -> tk.Label:
    """Label que mostra o saldo de moedas da jogadora."""
    lbl = tk.Label(
        parent,
        text=f"💰 {jogadora.moedas} moedas",
        font=("Arial", 12, "bold"),
        bg=BG,
        fg="#B8860B",
    )
    return lbl


def titulo_tela(parent, texto: str, tamanho: int = 28) -> tk.Label:
    """Label de título com estilo padrão."""
    lbl = tk.Label(
        parent,
        text=texto,
        font=("Comic Sans MS", tamanho, "bold"),
        bg=BG,
        fg=DEEP_RED,
    )
    lbl.pack(pady=(20, 6))
    return lbl


def subtitulo_perfil(parent, jogadora) -> tk.Label | None:
    """Label discreta mostrando o perfil ativo."""
    if jogadora is None:
        return None
    lbl = tk.Label(
        parent,
        text=f"👤 Perfil ativo: {jogadora.nome}",
        font=("Arial", 11, "italic"),
        bg=BG,
        fg=VIOLET,
    )
    lbl.pack(pady=(0, 6))
    return lbl
