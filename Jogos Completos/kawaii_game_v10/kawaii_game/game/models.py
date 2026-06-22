"""
models.py — Modelos de dados do jogo (sem dependência de UI).

Classes:
    Carta               — uma carta do tabuleiro
    Jogadora            — perfil completo de uma jogadora
    GerenciadorDePerfis — armário de todas as jogadoras
    Ranking             — top 10 resultados
"""

from datetime import datetime
from .constants import (
    XP_POR_NIVEL, titulo_para_nivel,
    MAX_HISTORICO, TEMAS_BASE,
    RANK_FILE, PERFIS_FILE,
)
from .file_manager import FileManager


# ══════════════════════════════════════════════════════
# CARTA
# ══════════════════════════════════════════════════════
class Carta:
    """Representa uma carta individual do tabuleiro."""

    def __init__(self, indice: int, valor: str):
        self.indice    = indice
        self.valor     = valor
        self.virada    = False
        self.combinada = False

    def virar(self):
        self.virada = True

    def esconder(self):
        self.virada = False

    def marcar_combinada(self):
        self.combinada = True
        self.virada    = True

    def __repr__(self) -> str:
        estado = "✓" if self.combinada else ("↑" if self.virada else "↓")
        return f"Carta({self.indice}, {self.valor}, {estado})"


# ══════════════════════════════════════════════════════
# JOGADORA
# ══════════════════════════════════════════════════════
class Jogadora:
    """Perfil completo de uma jogadora: XP, nível, moedas, conquistas, loja e histórico."""

    def __init__(self, nome: str = "Convidada"):
        self.nome         = nome
        self.xp           = 0
        self.level        = 1
        self.moedas       = 0
        self.achievements: list[str] = []
        self.itens_loja:   list[str] = []   # ids dos itens comprados
        self.historico:    list[dict] = []
        self.stats: dict = {
            "games_played": 0,
            "games_won":    0,
            "total_time":   0,
            "best_time":    None,
        }

    # ── serialização ──────────────────────────────────
    def para_dicionario(self) -> dict:
        return {
            "xp":           self.xp,
            "level":        self.level,
            "moedas":       self.moedas,
            "achievements": self.achievements,
            "itens_loja":   self.itens_loja,
            "historico":    self.historico,
            "stats":        self.stats,
        }

    def carregar_de(self, dados: dict):
        self.xp           = dados.get("xp", 0)
        self.level        = dados.get("level", 1)
        self.moedas       = dados.get("moedas", 0)
        self.achievements = dados.get("achievements", [])
        self.itens_loja   = dados.get("itens_loja", [])
        self.historico    = dados.get("historico", [])
        self.stats        = dados.get("stats", self.stats)

    # ── XP e nível ────────────────────────────────────
    def ganhar_xp(self, quantidade: int) -> bool:
        """Soma XP e recalcula nível. Devolve True se subiu de nível."""
        nivel_antes = self.level
        self.xp    += quantidade
        self.level  = self.xp // XP_POR_NIVEL + 1
        return self.level > nivel_antes

    def xp_no_nivel_atual(self) -> int:
        return self.xp % XP_POR_NIVEL

    def xp_para_proximo(self) -> int:
        return XP_POR_NIVEL

    # ── moedas ────────────────────────────────────────
    def ganhar_moedas(self, quantidade: int):
        self.moedas += quantidade

    def gastar_moedas(self, quantidade: int) -> bool:
        """Tenta gastar moedas. Devolve True se havia saldo suficiente."""
        if self.moedas >= quantidade:
            self.moedas -= quantidade
            return True
        return False

    # ── conquistas ────────────────────────────────────
    def desbloquear_conquista(self, texto: str) -> bool:
        """Adiciona conquista nova. Devolve True se era inédita."""
        if texto not in self.achievements:
            self.achievements.append(texto)
            return True
        return False

    # ── loja ──────────────────────────────────────────
    def possui_item(self, item_id: str) -> bool:
        return item_id in self.itens_loja

    def tema_disponivel(self, chave_tema: str) -> bool:
        """Verifica se a jogadora pode usar esse tema (base ou comprado)."""
        if chave_tema in TEMAS_BASE:
            return True
        # procura pelo campo 'chave' no catálogo
        from .constants import CATALOGO_LOJA
        for item in CATALOGO_LOJA:
            if item["chave"] == chave_tema and item["id"] in self.itens_loja:
                return True
        return False

    def comprar_item(self, item_id: str, preco: int) -> bool:
        """Compra um item da loja. Devolve True se a compra foi bem-sucedida."""
        if self.possui_item(item_id):
            return False
        if self.gastar_moedas(preco):
            self.itens_loja.append(item_id)
            return True
        return False

    # ── título ────────────────────────────────────────
    def titulo(self) -> str:
        return titulo_para_nivel(self.level)

    # ── histórico ─────────────────────────────────────
    def registrar_partida(self, tempo: int, dificuldade: str, vitoria: bool):
        entrada = {
            "data":        datetime.now().strftime("%d/%m/%Y %H:%M"),
            "tempo":       tempo,
            "dificuldade": dificuldade,
            "vitoria":     vitoria,
        }
        self.historico.insert(0, entrada)
        self.historico = self.historico[:MAX_HISTORICO]

    def __repr__(self) -> str:
        return f"Jogadora({self.nome!r}, level={self.level}, xp={self.xp}, moedas={self.moedas})"


# ══════════════════════════════════════════════════════
# GERENCIADOR DE PERFIS
# ══════════════════════════════════════════════════════
class GerenciadorDePerfis:
    """Cuida de todos os perfis salvos em disco."""

    def __init__(self):
        self.perfis: dict = {}
        self.carregar()

    def carregar(self):
        self.perfis = FileManager.ler(PERFIS_FILE, padrao={})

    def salvar(self):
        FileManager.gravar(PERFIS_FILE, self.perfis)

    def nomes(self) -> list[str]:
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


# ══════════════════════════════════════════════════════
# RANKING
# ══════════════════════════════════════════════════════
class Ranking:
    """Top 10 resultados persistidos em disco."""

    def __init__(self):
        self.lista: list[dict] = []
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
