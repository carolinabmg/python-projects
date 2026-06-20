"""
app.py — Classe principal KawaiiMemoryApp.

Responsabilidades:
  - Criar a janela tkinter
  - Guardar estado global (jogadora ativa, ranking, etc.)
  - Orquestrar a navegação entre telas
  - Delegar a renderização a screens.py e game_screen.py
"""

import tkinter as tk
from tkinter import messagebox

from .constants import (
    BG, SAVE_GAME_FILE, Dificuldade, GRADE_DIFICULDADE,
    CATALOGO_LOJA,
)
from .models import GerenciadorDePerfis, Jogadora, Ranking
from .file_manager import FileManager
from . import sound
from . import screens
from .game_screen import GameScreen


class KawaiiMemoryApp:
    """Ponto de entrada do jogo. Cria a janela e gerencia o estado global."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎀 Memory Game Deluxe Kawaii RPG v10.0")
        self.root.geometry("1200x960")
        self.root.configure(bg=BG)

        # dados persistentes
        self.gerenciador = GerenciadorDePerfis()
        self.ranking     = Ranking()
        self.jogadora: Jogadora | None = None

        # variáveis de controle da UI
        self.diff        = tk.StringVar(value=Dificuldade.FACIL.value)
        self.tema_atual  = tk.StringVar(value="Kawaii 🎀")
        self.novo_perfil = tk.StringVar()

        # referência ao arquivo de save
        self.save_file = SAVE_GAME_FILE

        self.tela_perfis()

    # ── utilitários ──────────────────────────────────────────
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _dificuldade_atual(self) -> Dificuldade:
        for d in Dificuldade:
            if d.value == self.diff.get():
                return d
        return Dificuldade.FACIL

    # ── XP e conquistas (atalhos usados por GameScreen) ──────
    def _desbloquear(self, texto: str):
        if self.jogadora and self.jogadora.desbloquear_conquista(texto):
            self.gerenciador.salvar_jogadora(self.jogadora)
            messagebox.showinfo("🏆 CONQUISTA!", texto)

    # ── navegação: telas simples ──────────────────────────────
    def tela_perfis(self):
        screens.build_tela_perfis(self)

    def tela_comparar(self):
        screens.build_tela_comparar(self)

    def home(self):
        screens.build_home(self)

    def tela_perfil_detalhe(self):
        screens.build_tela_perfil_detalhe(self)

    def tela_ranking(self):
        screens.build_tela_ranking(self)

    def tela_conquistas(self):
        screens.build_tela_conquistas(self)

    def tela_historico(self):
        screens.build_tela_historico(self)

    def tela_loja(self):
        screens.build_tela_loja(self)

    # ── perfis ───────────────────────────────────────────────
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

    # ── loja ─────────────────────────────────────────────────
    def comprar_item(self, item: dict):
        """Processa a compra de um item da loja."""
        if self.jogadora.comprar_item(item["id"], item["preco"]):
            self.gerenciador.salvar_jogadora(self.jogadora)
            sound.compra()
            messagebox.showinfo(
                "🎉 Compra realizada!",
                f"Você adquiriu: {item['nome']}!\n"
                f"Saldo restante: 💰 {self.jogadora.moedas} moedas",
            )
            self.tela_loja()   # recarrega pra atualizar botões
        else:
            messagebox.showinfo(
                "💸 Saldo insuficiente",
                f"Você precisa de 💰 {item['preco']} moedas.\n"
                f"Seu saldo: 💰 {self.jogadora.moedas}",
            )

    # ── reset / sair ─────────────────────────────────────────
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
                               "Apagar todo o ranking?\nOs perfis continuam intactos."):
            self.ranking.resetar()
            messagebox.showinfo("✨ Pronto!", "Ranking zerado! Nova disputa começa agora. 🌸")
            self.tela_ranking()

    def sair_do_jogo(self):
        if messagebox.askyesno("Sair", "Quer mesmo fechar a Academia de Magia? 🌙✨"):
            self.root.destroy()

    # ── jogo ─────────────────────────────────────────────────
    def new_game(self):
        GameScreen(self, estado_salvo=None)

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
        GameScreen(self, estado_salvo=estado)

    def voltar_da_partida(self):
        if messagebox.askyesno("Voltar",
                               "Se voltar agora, perde a partida (salve antes).\nQuer mesmo voltar? 🌙"):
            self.home()

    def reiniciar_partida(self):
        if messagebox.askyesno("Novo jogo",
                               "Recomeçar vai perder a partida atual. Tem certeza? 🔄"):
            self.new_game()
