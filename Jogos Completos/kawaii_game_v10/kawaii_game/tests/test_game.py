"""
tests/test_game.py — Testes automatizados com pytest.

Cobre:
    - FileManager  (ler, gravar, apagar, existe)
    - Carta        (estados: virar, esconder, combinar)
    - Jogadora     (XP, nível, moedas, loja, conquistas, histórico)
    - GerenciadorDePerfis (CRUD de perfis)
    - Ranking      (inserção, ordenação, limite, reset)
    - Lógica da loja (compra, saldo insuficiente, item duplicado)
    - Constantes   (títulos, dificuldades)
"""

import json
import os
import sys
import tempfile
import pytest

# garante que o pacote 'game' seja importável mesmo rodando de dentro de tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from game.file_manager import FileManager
from game.models import Carta, Jogadora, GerenciadorDePerfis, Ranking
from game.constants import (
    titulo_para_nivel, Dificuldade, GRADE_DIFICULDADE,
    XP_POR_NIVEL, CATALOGO_LOJA, TEMAS_BASE,
)


# ══════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════

@pytest.fixture
def tmp_arquivo(tmp_path):
    """Caminho temporário para um arquivo JSON."""
    return str(tmp_path / "teste.json")


@pytest.fixture
def jogadora():
    return Jogadora("Carol")


@pytest.fixture
def gerenciador(tmp_path, monkeypatch):
    """GerenciadorDePerfis usando arquivo temporário."""
    arquivo = str(tmp_path / "perfis.json")
    monkeypatch.setattr("game.constants.PERFIS_FILE", arquivo)
    monkeypatch.setattr("game.models.PERFIS_FILE", arquivo)
    return GerenciadorDePerfis()


@pytest.fixture
def ranking(tmp_path, monkeypatch):
    """Ranking usando arquivo temporário."""
    arquivo = str(tmp_path / "ranking.json")
    monkeypatch.setattr("game.constants.RANK_FILE", arquivo)
    monkeypatch.setattr("game.models.RANK_FILE", arquivo)
    return Ranking()


# ══════════════════════════════════════════════════════
# FILE MANAGER
# ══════════════════════════════════════════════════════

class TestFileManager:

    def test_gravar_e_ler(self, tmp_arquivo):
        dados = {"nome": "Carol", "xp": 200}
        assert FileManager.gravar(tmp_arquivo, dados) is True
        assert FileManager.ler(tmp_arquivo) == dados

    def test_ler_arquivo_inexistente_retorna_padrao(self, tmp_arquivo):
        resultado = FileManager.ler(tmp_arquivo, padrao=[])
        assert resultado == []

    def test_ler_arquivo_corrompido_retorna_padrao(self, tmp_arquivo):
        with open(tmp_arquivo, "w") as f:
            f.write("isso não é json {{{")
        assert FileManager.ler(tmp_arquivo, padrao=None) is None

    def test_apagar_arquivo_existente(self, tmp_arquivo):
        FileManager.gravar(tmp_arquivo, {})
        assert FileManager.apagar(tmp_arquivo) is True
        assert not os.path.exists(tmp_arquivo)

    def test_apagar_arquivo_inexistente_retorna_false(self, tmp_arquivo):
        assert FileManager.apagar(tmp_arquivo) is False

    def test_existe(self, tmp_arquivo):
        assert FileManager.existe(tmp_arquivo) is False
        FileManager.gravar(tmp_arquivo, {})
        assert FileManager.existe(tmp_arquivo) is True


# ══════════════════════════════════════════════════════
# CARTA
# ══════════════════════════════════════════════════════

class TestCarta:

    def test_estado_inicial(self):
        c = Carta(0, "🌸")
        assert c.indice == 0
        assert c.valor == "🌸"
        assert c.virada is False
        assert c.combinada is False

    def test_virar(self):
        c = Carta(1, "🎀")
        c.virar()
        assert c.virada is True
        assert c.combinada is False

    def test_esconder(self):
        c = Carta(2, "🧸")
        c.virar()
        c.esconder()
        assert c.virada is False

    def test_marcar_combinada(self):
        c = Carta(3, "🦋")
        c.marcar_combinada()
        assert c.combinada is True
        assert c.virada is True  # combinada implica virada

    def test_repr(self):
        c = Carta(0, "⭐")
        assert "Carta" in repr(c)


# ══════════════════════════════════════════════════════
# JOGADORA — XP E NÍVEL
# ══════════════════════════════════════════════════════

class TestJogadoraXP:

    def test_xp_inicial(self, jogadora):
        assert jogadora.xp == 0
        assert jogadora.level == 1

    def test_ganhar_xp_sem_subir_nivel(self, jogadora):
        subiu = jogadora.ganhar_xp(50)
        assert subiu is False
        assert jogadora.xp == 50
        assert jogadora.level == 1

    def test_subir_nivel(self, jogadora):
        subiu = jogadora.ganhar_xp(XP_POR_NIVEL)
        assert subiu is True
        assert jogadora.level == 2

    def test_multiplos_niveis(self, jogadora):
        jogadora.ganhar_xp(XP_POR_NIVEL * 5)
        assert jogadora.level == 6

    def test_xp_no_nivel_atual(self, jogadora):
        jogadora.ganhar_xp(150)
        assert jogadora.xp_no_nivel_atual() == 50

    def test_xp_para_proximo(self, jogadora):
        assert jogadora.xp_para_proximo() == XP_POR_NIVEL


# ══════════════════════════════════════════════════════
# JOGADORA — MOEDAS
# ══════════════════════════════════════════════════════

class TestJogadoraMoedas:

    def test_ganhar_moedas(self, jogadora):
        jogadora.ganhar_moedas(100)
        assert jogadora.moedas == 100

    def test_gastar_moedas_com_saldo(self, jogadora):
        jogadora.ganhar_moedas(50)
        resultado = jogadora.gastar_moedas(30)
        assert resultado is True
        assert jogadora.moedas == 20

    def test_gastar_moedas_sem_saldo(self, jogadora):
        resultado = jogadora.gastar_moedas(10)
        assert resultado is False
        assert jogadora.moedas == 0

    def test_gastar_exato(self, jogadora):
        jogadora.ganhar_moedas(30)
        assert jogadora.gastar_moedas(30) is True
        assert jogadora.moedas == 0


# ══════════════════════════════════════════════════════
# JOGADORA — LOJA
# ══════════════════════════════════════════════════════

class TestLoja:

    def test_tema_base_disponivel_sem_compra(self, jogadora):
        for tema in TEMAS_BASE:
            assert jogadora.tema_disponivel(tema) is True

    def test_tema_premium_indisponivel_sem_compra(self, jogadora):
        assert jogadora.tema_disponivel("Comida 🍕") is False

    def test_comprar_item_com_saldo(self, jogadora):
        jogadora.ganhar_moedas(100)
        item = CATALOGO_LOJA[0]  # Comida 🍕 — 30 moedas
        resultado = jogadora.comprar_item(item["id"], item["preco"])
        assert resultado is True
        assert jogadora.possui_item(item["id"])
        assert jogadora.moedas == 100 - item["preco"]

    def test_comprar_item_sem_saldo(self, jogadora):
        item = CATALOGO_LOJA[0]
        resultado = jogadora.comprar_item(item["id"], item["preco"])
        assert resultado is False
        assert not jogadora.possui_item(item["id"])

    def test_comprar_item_duplicado(self, jogadora):
        jogadora.ganhar_moedas(200)
        item = CATALOGO_LOJA[0]
        jogadora.comprar_item(item["id"], item["preco"])
        resultado = jogadora.comprar_item(item["id"], item["preco"])
        assert resultado is False  # já possui

    def test_tema_disponivel_apos_compra(self, jogadora):
        jogadora.ganhar_moedas(100)
        item = next(i for i in CATALOGO_LOJA if i["chave"] == "Comida 🍕")
        jogadora.comprar_item(item["id"], item["preco"])
        assert jogadora.tema_disponivel("Comida 🍕") is True


# ══════════════════════════════════════════════════════
# JOGADORA — CONQUISTAS
# ══════════════════════════════════════════════════════

class TestConquistas:

    def test_desbloquear_nova(self, jogadora):
        resultado = jogadora.desbloquear_conquista("Primeira Vitória 🏆")
        assert resultado is True
        assert "Primeira Vitória 🏆" in jogadora.achievements

    def test_desbloquear_duplicada(self, jogadora):
        jogadora.desbloquear_conquista("Primeira Vitória 🏆")
        resultado = jogadora.desbloquear_conquista("Primeira Vitória 🏆")
        assert resultado is False
        assert jogadora.achievements.count("Primeira Vitória 🏆") == 1


# ══════════════════════════════════════════════════════
# JOGADORA — HISTÓRICO
# ══════════════════════════════════════════════════════

class TestHistorico:

    def test_registrar_partida(self, jogadora):
        jogadora.registrar_partida(45, "Fácil", vitoria=True)
        assert len(jogadora.historico) == 1
        assert jogadora.historico[0]["vitoria"] is True
        assert jogadora.historico[0]["dificuldade"] == "Fácil"

    def test_limite_historico(self, jogadora):
        from game.constants import MAX_HISTORICO
        for i in range(MAX_HISTORICO + 3):
            jogadora.registrar_partida(i * 10, "Fácil", True)
        assert len(jogadora.historico) == MAX_HISTORICO

    def test_ordem_mais_recente_primeiro(self, jogadora):
        jogadora.registrar_partida(10, "Fácil", True)
        jogadora.registrar_partida(20, "Médio", False)
        assert jogadora.historico[0]["tempo"] == 20  # mais recente


# ══════════════════════════════════════════════════════
# JOGADORA — SERIALIZAÇÃO
# ══════════════════════════════════════════════════════

class TestSerializacao:

    def test_para_dicionario_e_carregar_de(self, jogadora):
        jogadora.ganhar_xp(250)
        jogadora.ganhar_moedas(80)
        jogadora.desbloquear_conquista("Velocista ⚡")
        jogadora.registrar_partida(30, "Difícil", True)

        dados = jogadora.para_dicionario()

        nova = Jogadora("Carol")
        nova.carregar_de(dados)

        assert nova.xp == jogadora.xp
        assert nova.level == jogadora.level
        assert nova.moedas == jogadora.moedas
        assert nova.achievements == jogadora.achievements
        assert len(nova.historico) == 1


# ══════════════════════════════════════════════════════
# GERENCIADOR DE PERFIS
# ══════════════════════════════════════════════════════

class TestGerenciadorDePerfis:

    def test_criar_e_carregar(self, gerenciador):
        jog = Jogadora("Ana")
        jog.ganhar_xp(100)
        gerenciador.salvar_jogadora(jog)

        carregada = gerenciador.carregar_jogadora("Ana")
        assert carregada.xp == 100

    def test_existe(self, gerenciador):
        assert gerenciador.existe("Ana") is False
        gerenciador.salvar_jogadora(Jogadora("Ana"))
        assert gerenciador.existe("Ana") is True

    def test_apagar(self, gerenciador):
        gerenciador.salvar_jogadora(Jogadora("Ana"))
        gerenciador.apagar("Ana")
        assert gerenciador.existe("Ana") is False

    def test_nomes(self, gerenciador):
        gerenciador.salvar_jogadora(Jogadora("Ana"))
        gerenciador.salvar_jogadora(Jogadora("Bea"))
        assert set(gerenciador.nomes()) == {"Ana", "Bea"}

    def test_resetar_todos(self, gerenciador):
        gerenciador.salvar_jogadora(Jogadora("Ana"))
        gerenciador.resetar_todos()
        assert gerenciador.nomes() == []


# ══════════════════════════════════════════════════════
# RANKING
# ══════════════════════════════════════════════════════

class TestRanking:

    def test_adicionar_entrada(self, ranking):
        ranking.adicionar("Carol", 300, 45, 3)
        assert len(ranking.lista) == 1
        assert ranking.lista[0]["name"] == "Carol"

    def test_ordenacao_por_score(self, ranking):
        ranking.adicionar("Ana",   200, 60, 2)
        ranking.adicionar("Carol", 500, 30, 5)
        ranking.adicionar("Bea",   350, 45, 3)
        assert ranking.lista[0]["name"] == "Carol"

    def test_limite_top_10(self, ranking):
        for i in range(15):
            ranking.adicionar(f"Player{i}", i * 10, 60, 1)
        assert len(ranking.lista) == 10

    def test_esta_vazio(self, ranking):
        assert ranking.esta_vazio() is True
        ranking.adicionar("Carol", 100, 30, 1)
        assert ranking.esta_vazio() is False

    def test_resetar(self, ranking):
        ranking.adicionar("Carol", 100, 30, 1)
        ranking.resetar()
        assert ranking.esta_vazio() is True


# ══════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════

class TestConstantes:

    def test_titulo_nivel_1(self):
        assert titulo_para_nivel(1) == "Aprendiz 🌱"

    def test_titulo_nivel_3(self):
        assert titulo_para_nivel(3) == "Maga do Código 🔮"

    def test_titulo_nivel_6(self):
        assert titulo_para_nivel(6) == "Arquimaga 👑"

    def test_titulo_nivel_10(self):
        assert titulo_para_nivel(10) == "Lenda Kawaii ✨"

    def test_titulo_nivel_intermediario(self):
        # nível 5 deve pegar o título do limiar 3
        assert titulo_para_nivel(5) == "Maga do Código 🔮"

    def test_grade_dificuldade(self):
        assert GRADE_DIFICULDADE[Dificuldade.FACIL]   == (4, 4)
        assert GRADE_DIFICULDADE[Dificuldade.MEDIO]   == (4, 5)
        assert GRADE_DIFICULDADE[Dificuldade.DIFICIL] == (6, 6)

    def test_catalogo_loja_tem_campos_obrigatorios(self):
        campos = {"id", "nome", "descricao", "preco", "tipo", "chave", "preview"}
        for item in CATALOGO_LOJA:
            assert campos.issubset(item.keys()), f"Item {item} faltando campos"

    def test_precos_positivos(self):
        for item in CATALOGO_LOJA:
            assert item["preco"] > 0
