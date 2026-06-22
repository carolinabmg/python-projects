"""
screens.py — Telas de navegação (sem a tela de jogo em si).

Telas implementadas:
    tela_perfis, tela_comparar, tela_home,
    tela_perfil_detalhe, tela_ranking,
    tela_conquistas, tela_historico
"""

import tkinter as tk
from tkinter import messagebox
import random

from .constants import (
    BG, PINK, LILAC, BLUE, MINT, PEACH, YELLOW,
    PURPLE, CORAL, LIGHT_PINK, RED, DARK_TEXT, VIOLET, DEEP_RED,
    CORES_BOTOES, TODAS_CONQUISTAS, FALAS_HOME,
    Dificuldade, TEMAS, TEMAS_BASE, TEMAS_PREMIUM,
)
from .models import Jogadora, GerenciadorDePerfis, Ranking
from .file_manager import FileManager
from . import widgets as W


class NavMixin:
    """
    Mixin com helpers de navegação.
    Requer que a classe concreta tenha: self.root, self.clear(),
    self.jogadora, self.gerenciador, self.ranking.
    """

    def _botao_voltar(self, parent, destino, pady: int = 18):
        btn = W.botao_padrao(parent, "🔙 Voltar", destino, cor=BLUE)
        btn.pack(pady=pady)
        return btn


# ══════════════════════════════════════════════════════════════
# TELA DE PERFIS
# ══════════════════════════════════════════════════════════════
def build_tela_perfis(app):
    """Monta a tela de seleção/criação/exclusão de perfis."""
    app.start_time = None
    app.clear()
    main = tk.Frame(app.root, bg=BG)
    main.pack(fill="both", expand=True)

    W.titulo_tela(main, "👥 PERFIS DAS FEITICEIRAS 🌸")
    tk.Label(main, text="Escolha um perfil ou crie um novo:",
             font=("Arial", 13), bg=BG, fg=VIOLET).pack(pady=(0, 10))

    nomes = app.gerenciador.nomes()
    if not nomes:
        tk.Label(main, text="Nenhum perfil ainda… crie o primeiro! 🌱",
                 font=("Arial", 13, "italic"), bg=BG, fg="#999999").pack(pady=10)
    else:
        lista_f = tk.Frame(main, bg=BG)
        lista_f.pack(pady=4)
        for nome in nomes:
            jog  = app.gerenciador.carregar_jogadora(nome)
            linha = tk.Frame(lista_f, bg=BG)
            linha.pack(pady=3)
            tk.Button(
                linha,
                text=f"👤 {nome}  —  Nível {jog.level}  —  {jog.titulo()}  —  💰{jog.moedas}",
                font=("Arial", 12, "bold"), bg=LILAC, fg="white", width=42,
                command=lambda n=nome: app.escolher_perfil(n),
            ).pack(side="left", padx=4)
            tk.Button(
                linha, text="🗑️",
                font=("Arial", 12, "bold"), bg=RED, fg="white", width=4,
                command=lambda n=nome: app.apagar_perfil(n),
            ).pack(side="left")

    # criar novo perfil
    criar_f = tk.Frame(main, bg=BG)
    criar_f.pack(pady=(16, 4))
    tk.Label(criar_f, text="➕ Nome:", font=("Arial", 13, "bold"),
             bg=BG, fg=VIOLET).pack(side="left", padx=4)
    tk.Entry(criar_f, font=("Arial", 14), width=16,
             textvariable=app.novo_perfil).pack(side="left", padx=4)
    tk.Button(criar_f, text="Criar", font=("Arial", 12, "bold"),
              bg=MINT, fg=DARK_TEXT, width=8,
              command=app.criar_perfil).pack(side="left", padx=4)

    botoes_f = tk.Frame(main, bg=BG)
    botoes_f.pack(pady=16)
    if nomes:
        W.botao_padrao(botoes_f, "📊 COMPARAR PERFIS", app.tela_comparar, cor=BLUE).pack(pady=4)
        W.botao_padrao(botoes_f, "🏆 RANKING GERAL", app.tela_ranking, cor=YELLOW).pack(pady=3)
    W.botao_padrao(botoes_f, "♻️ RESETAR TUDO", app.resetar_tudo, cor=RED).pack(pady=(10, 3))
    W.botao_padrao(botoes_f, "🚪 SAIR", app.sair_do_jogo, cor=CORAL).pack(pady=3)


# ══════════════════════════════════════════════════════════════
# TELA DE COMPARAÇÃO
# ══════════════════════════════════════════════════════════════
def build_tela_comparar(app):
    app.clear()
    main = tk.Frame(app.root, bg=BG)
    main.pack(fill="both", expand=True)
    W.titulo_tela(main, "📊 COMPARAR PERFIS 📊")

    nomes = app.gerenciador.nomes()
    if not nomes:
        tk.Label(main, text="Nenhum perfil pra comparar ainda… 🌱",
                 font=("Arial", 14), bg=BG, fg=VIOLET).pack(pady=40)
    else:
        jogadoras = sorted(
            [app.gerenciador.carregar_jogadora(n) for n in nomes],
            key=lambda j: j.xp, reverse=True,
        )
        tabela = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
        tabela.pack(padx=28, pady=12, fill="both")
        medalhas = {0: "🥇", 1: "🥈", 2: "🥉"}
        for pos, jog in enumerate(jogadoras):
            cor   = YELLOW if pos == 0 else LIGHT_PINK
            texto = (
                f"{medalhas.get(pos, f'{pos+1}º')}  👤 {jog.nome}  |  "
                f"{jog.titulo()}  |  ⭐ Nível {jog.level}  |  "
                f"💜 XP {jog.xp}  |  💰 {jog.moedas}  |  🏆 {jog.stats['games_won']}v"
            )
            tk.Label(tabela, text=texto,
                     font=("Arial", 11, "bold"), bg=cor, fg=DARK_TEXT).pack(
                padx=8, pady=5, fill="x")

    W.botao_padrao(main, "🔙 Voltar", app.tela_perfis, cor=BLUE).pack(pady=18)


# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
def build_home(app):
    if not app.jogadora:
        app.tela_perfis()
        return
    app.start_time = None
    app.clear()
    main = tk.Frame(app.root, bg=BG)
    main.pack(fill="both", expand=True)

    W.titulo_tela(main, "🎀 Memory Game Deluxe 🌸", tamanho=30)

    # perfil + moedas
    nivel_f = tk.Frame(main, bg=PURPLE, relief="raised", bd=3)
    nivel_f.pack(padx=28, pady=4)
    tk.Label(nivel_f, text=f"👤 {app.jogadora.nome}",
             font=("Comic Sans MS", 16, "bold"), bg=PURPLE, fg="#4C0080").pack(padx=18, pady=(6, 0))
    tk.Label(nivel_f,
             text=f"👑 Nível {app.jogadora.level}  —  {app.jogadora.titulo()}  —  💰 {app.jogadora.moedas} moedas",
             font=("Arial", 11, "bold"), bg=PURPLE, fg=VIOLET).pack(padx=18, pady=(0, 6))

    W.barra_xp(main, app.jogadora)

    # stats
    stats_f = tk.Frame(main, bg=LILAC, relief="raised", bd=2)
    stats_f.pack(padx=28, pady=4)
    tk.Label(stats_f,
             text=(f"💜 XP: {app.jogadora.xp}  |  "
                   f"🎮 Jogos: {app.jogadora.stats['games_played']}  |  "
                   f"🏆 Vitórias: {app.jogadora.stats['games_won']}"),
             font=("Arial", 11, "bold"), bg=LILAC, fg="#4C0080").pack(padx=8, pady=6)

    # mascote
    mascote_f = tk.Frame(main, bg=PEACH, relief="raised", bd=2)
    mascote_f.pack(padx=28, pady=4)
    tk.Label(mascote_f, text=f"🦋 Cirilla: {random.choice(FALAS_HOME)}",
             font=("Arial", 11, "italic"), bg=PEACH, fg=DARK_TEXT).pack(padx=8, pady=5)

    # config
    config_f = tk.Frame(main, bg=BG)
    config_f.pack(pady=6)

    tk.Label(config_f, text="Dificuldade:",
             font=("Arial", 11, "bold"), bg=BG, fg=VIOLET).grid(row=0, column=0, padx=8, sticky="w")
    diff_inner = tk.Frame(config_f, bg=BG)
    diff_inner.grid(row=0, column=1, padx=6)
    for d in Dificuldade:
        tk.Radiobutton(diff_inner, text=d.value, variable=app.diff, value=d.value,
                       font=("Arial", 11), bg=BG, activebackground=PINK).pack(side="left", padx=5)

    tk.Label(config_f, text="Tema:",
             font=("Arial", 11, "bold"), bg=BG, fg=VIOLET).grid(row=1, column=0, padx=8, pady=4, sticky="w")
    tema_inner = tk.Frame(config_f, bg=BG)
    tema_inner.grid(row=1, column=1, padx=6, pady=4)
    for nome_tema in TEMAS:
        disponivel = app.jogadora.tema_disponivel(nome_tema)
        cor_rb     = BG if disponivel else "#EEEEEE"
        rb = tk.Radiobutton(
            tema_inner, text=nome_tema,
            variable=app.tema_atual, value=nome_tema,
            font=("Arial", 10), bg=cor_rb, activebackground=MINT,
            state="normal" if disponivel else "disabled",
        )
        rb.pack(side="left", padx=4)

    # botões
    botoes_f = tk.Frame(main, bg=BG)
    botoes_f.pack(pady=6)

    tk.Label(botoes_f, text="▶️ Jogar", font=("Arial", 10, "bold"),
             bg=BG, fg=DEEP_RED).pack(pady=(0, 2))
    W.botao_padrao(botoes_f, "🎮 JOGAR", app.new_game, cor=PINK, fonte_tamanho=13).pack(pady=3)
    if FileManager.existe(app.save_file):
        W.botao_padrao(botoes_f, "▶️ CONTINUAR JOGO", app.continuar_jogo,
                       cor=MINT, fonte_tamanho=11).pack(pady=3)

    tk.Label(botoes_f, text="⚙️ Gerenciar", font=("Arial", 10, "bold"),
             bg=BG, fg=DEEP_RED).pack(pady=(8, 2))
    acoes = [
        ("🛒 LOJA",             PEACH,  app.tela_loja),
        ("📊 COMPARAR PERFIS",  BLUE,   app.tela_comparar),
        ("👑 MEU PERFIL",       LILAC,  app.tela_perfil_detalhe),
        ("🏆 RANKING",          YELLOW, app.tela_ranking),
        ("⭐ CONQUISTAS",        PEACH,  app.tela_conquistas),
        ("📜 HISTÓRICO",        PURPLE, app.tela_historico),
        ("👥 TROCAR PERFIL",    CORAL,  app.tela_perfis),
    ]
    for texto, cor, cmd in acoes:
        W.botao_padrao(botoes_f, texto, cmd, cor=cor, largura=22,
                       fonte_tamanho=11).pack(pady=2)


# ══════════════════════════════════════════════════════════════
# PERFIL DETALHE
# ══════════════════════════════════════════════════════════════
def build_tela_perfil_detalhe(app):
    app.clear()
    main = tk.Frame(app.root, bg=BG)
    main.pack(fill="both", expand=True)
    W.titulo_tela(main, "👑 MEU PERFIL 👑")

    frame = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
    frame.pack(padx=28, pady=10, fill="both")

    melhor = app.jogadora.stats["best_time"]
    melhor_txt = f"{melhor}s" if melhor else "—"
    info = (
        f"👤 Nome: {app.jogadora.nome}\n"
        f"👑 Título: {app.jogadora.titulo()}\n"
        f"⭐ Nível: {app.jogadora.level}\n"
        f"💜 XP Total: {app.jogadora.xp}\n"
        f"💰 Moedas: {app.jogadora.moedas}\n"
        f"🎮 Jogos jogados: {app.jogadora.stats['games_played']}\n"
        f"🏆 Vitórias: {app.jogadora.stats['games_won']}\n"
        f"⏱️ Melhor tempo: {melhor_txt}"
    )
    tk.Label(frame, text=info, font=("Arial", 13),
             bg=LIGHT_PINK, fg=DARK_TEXT, justify="left").pack(padx=18, pady=14)

    W.barra_xp(frame, app.jogadora)

    if app.jogadora.achievements:
        tk.Label(frame, text="Conquistas 🏆:",
                 font=("Arial", 12, "bold"), bg=LIGHT_PINK, fg=DEEP_RED).pack()
        for c in app.jogadora.achievements:
            tk.Label(frame, text=f"  ✓ {c}",
                     font=("Arial", 11), bg=LIGHT_PINK, fg="#4C0080").pack()

    W.botao_padrao(main, "🔙 Voltar", app.home, cor=BLUE).pack(pady=16)


# ══════════════════════════════════════════════════════════════
# RANKING
# ══════════════════════════════════════════════════════════════
def build_tela_ranking(app):
    app.clear()
    main = tk.Frame(app.root, bg=BG)
    main.pack(fill="both", expand=True)
    W.titulo_tela(main, "🏆 RANKING TOP 10 🏆")
    W.subtitulo_perfil(main, app.jogadora)

    if app.ranking.esta_vazio():
        tk.Label(main, text="Sem dados ainda… Seja a primeira! 🌸",
                 font=("Arial", 14), bg=BG, fg=VIOLET).pack(pady=40)
    else:
        frame = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
        frame.pack(padx=28, pady=14, fill="both")
        medalhas = {0: "🥇", 1: "🥈", 2: "🥉"}
        cores    = {0: YELLOW, 1: PEACH, 2: CORAL}
        for i, p in enumerate(app.ranking.lista[:10]):
            bg = cores.get(i, LIGHT_PINK)
            tk.Label(
                frame,
                text=f"{medalhas.get(i, f'{i+1:2d}.')} {p['name']} — Score: {p['score']} — ⏱️ {p['time']}s",
                font=("Arial", 12, "bold"), bg=bg, fg=DARK_TEXT,
            ).pack(padx=8, pady=6, fill="x")

    W.botao_padrao(main, "♻️ Resetar Ranking", app.resetar_ranking, cor=RED,
                   largura=22).pack(pady=(8, 0))
    destino = app.home if app.jogadora else app.tela_perfis
    W.botao_padrao(main, "🔙 Voltar", destino, cor=BLUE).pack(pady=14)


# ══════════════════════════════════════════════════════════════
# CONQUISTAS
# ══════════════════════════════════════════════════════════════
def build_tela_conquistas(app):
    app.clear()
    main = tk.Frame(app.root, bg=BG)
    main.pack(fill="both", expand=True)
    W.titulo_tela(main, "⭐ CONQUISTAS ⭐")
    W.subtitulo_perfil(main, app.jogadora)

    frame = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
    frame.pack(padx=28, pady=12, fill="both")
    for c in TODAS_CONQUISTAS:
        if c in app.jogadora.achievements:
            tk.Label(frame, text=f"✓ {c}",
                     font=("Arial", 11, "bold"), bg="#FFD6A5", fg=DARK_TEXT).pack(
                padx=8, pady=5, fill="x")
        else:
            tk.Label(frame, text=f"🔒 {c}",
                     font=("Arial", 11), bg=LIGHT_PINK, fg="#999999").pack(
                padx=8, pady=5, fill="x")

    W.botao_padrao(main, "🔙 Voltar", app.home, cor=BLUE).pack(pady=16)


# ══════════════════════════════════════════════════════════════
# HISTÓRICO
# ══════════════════════════════════════════════════════════════
def build_tela_historico(app):
    app.clear()
    main = tk.Frame(app.root, bg=BG)
    main.pack(fill="both", expand=True)
    W.titulo_tela(main, "📜 HISTÓRICO DE PARTIDAS 📜", tamanho=24)
    W.subtitulo_perfil(main, app.jogadora)

    hist = app.jogadora.historico
    if not hist:
        tk.Label(main, text="Nenhuma partida registrada ainda… Jogue primeiro! 🎮",
                 font=("Arial", 13, "italic"), bg=BG, fg=VIOLET).pack(pady=40)
    else:
        frame = tk.Frame(main, bg=LIGHT_PINK, relief="raised", bd=3)
        frame.pack(padx=28, pady=10, fill="both")
        cabecalho = "  #  |  Data & Hora         |  Dificuldade  |  Tempo  |  Resultado"
        tk.Label(frame, text=cabecalho,
                 font=("Courier", 11, "bold"), bg=LILAC, fg=DARK_TEXT).pack(
            padx=6, pady=5, fill="x")
        for i, h in enumerate(hist, 1):
            resultado = "✅ Vitória" if h["vitoria"] else "❌ Derrota"
            linha = (
                f"  {i}  |  {h['data']}  |  "
                f"{h['dificuldade']:<13}|  {h['tempo']:>4}s  |  {resultado}"
            )
            cor = MINT if h["vitoria"] else CORAL
            tk.Label(frame, text=linha,
                     font=("Courier", 11), bg=cor, fg=DARK_TEXT).pack(
                padx=6, pady=3, fill="x")

    W.botao_padrao(main, "🔙 Voltar", app.home, cor=BLUE).pack(pady=16)


# ══════════════════════════════════════════════════════════════
# LOJA
# ══════════════════════════════════════════════════════════════
def build_tela_loja(app):
    """Tela da loja de skins com sistema de moedas."""
    from .constants import CATALOGO_LOJA
    app.clear()
    main = tk.Frame(app.root, bg=BG)
    main.pack(fill="both", expand=True)
    W.titulo_tela(main, "🛒 LOJA DE SKINS 🛒")
    W.subtitulo_perfil(main, app.jogadora)

    # saldo
    saldo_f = tk.Frame(main, bg="#FFF9E6", relief="raised", bd=2)
    saldo_f.pack(padx=28, pady=4)
    app.lbl_moedas_loja = tk.Label(
        saldo_f,
        text=f"💰 Seu saldo: {app.jogadora.moedas} moedas",
        font=("Arial", 14, "bold"), bg="#FFF9E6", fg="#B8860B",
    )
    app.lbl_moedas_loja.pack(padx=20, pady=10)

    tk.Label(main,
             text="Compre novos temas de cartas! Cada tema libera um novo conjunto de emojis.",
             font=("Arial", 11, "italic"), bg=BG, fg=VIOLET).pack(pady=(4, 8))

    # catálogo
    catalogo_f = tk.Frame(main, bg=BG)
    catalogo_f.pack(padx=28, fill="both", expand=True)

    for item in CATALOGO_LOJA:
        _card_loja(catalogo_f, app, item)

    W.botao_padrao(main, "🔙 Voltar", app.home, cor=BLUE).pack(pady=14)


def _card_loja(parent, app, item: dict):
    """Renderiza um card de item na loja."""
    ja_tem   = app.jogadora.possui_item(item["id"])
    cor_card = MINT if ja_tem else LIGHT_PINK

    card = tk.Frame(parent, bg=cor_card, relief="raised", bd=2)
    card.pack(fill="x", pady=5, padx=8)

    info_f = tk.Frame(card, bg=cor_card)
    info_f.pack(side="left", padx=12, pady=8, fill="both", expand=True)

    tk.Label(info_f, text=item["nome"],
             font=("Arial", 13, "bold"), bg=cor_card, fg=DEEP_RED).pack(anchor="w")
    tk.Label(info_f, text=item["descricao"],
             font=("Arial", 11), bg=cor_card, fg=DARK_TEXT).pack(anchor="w")
    tk.Label(info_f, text=f"Preview: {item['preview']}",
             font=("Arial", 14), bg=cor_card).pack(anchor="w")

    btn_f = tk.Frame(card, bg=cor_card)
    btn_f.pack(side="right", padx=12, pady=8)

    if ja_tem:
        tk.Label(btn_f, text="✅ Adquirido",
                 font=("Arial", 12, "bold"), bg=cor_card, fg="#2D7A2D").pack()
    else:
        tk.Label(btn_f, text=f"💰 {item['preco']} moedas",
                 font=("Arial", 12, "bold"), bg=cor_card, fg="#B8860B").pack(pady=(0, 4))
        pode_comprar = app.jogadora.moedas >= item["preco"]
        tk.Button(
            btn_f,
            text="Comprar",
            font=("Arial", 11, "bold"),
            bg=PEACH if pode_comprar else "#CCCCCC",
            fg=DARK_TEXT,
            width=10,
            state="normal" if pode_comprar else "disabled",
            command=lambda i=item: app.comprar_item(i),
        ).pack()
