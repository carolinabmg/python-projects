# habit_quest/models.py
# Classes principais do Habit Quest

import json
import os
from datetime import date, datetime
from enum import Enum


# ── ENUMS ──────────────────────────────────────────────

class Frequencia(Enum):
    DIARIO = "diario"
    SEMANAL = "semanal"


class NivelPersonagem(Enum):
    DORMINHOCA   = (1,  0,    "😴 dorminhoca")
    ACORDANDO    = (2,  100,  "🥱 acordando")
    ANIMADA      = (3,  300,  "😊 animada")
    FOCADA       = (4,  600,  "🎯 focada")
    BRILHANTE    = (5,  1000, "✨ brilhante")
    LENDARIA     = (6,  1500, "🌟 lendária")

    def __init__(self, nivel, xp_necessario, descricao):
        self.nivel = nivel
        self.xp_necessario = xp_necessario
        self.descricao = descricao


# ── HABITO ─────────────────────────────────────────────

class Habito:
    def __init__(self, nome: str, icone: str = "⭐",
                 frequencia: Frequencia = Frequencia.DIARIO,
                 xp_recompensa: int = 20,
                 moedas_recompensa: int = 5):
        self.nome = nome
        self.icone = icone
        self.frequencia = frequencia
        self.xp_recompensa = xp_recompensa
        self.moedas_recompensa = moedas_recompensa
        self.streak_atual = 0
        self.maior_streak = 0
        self.historico: list[str] = []  # datas ISO completadas
        self.criado_em = date.today().isoformat()

    def completar_hoje(self) -> tuple[int, int]:
        """Marca o hábito como completo hoje. Retorna (xp, moedas) ganhos."""
        hoje = date.today().isoformat()
        if hoje in self.historico:
            return 0, 0  # já completado hoje

        self.historico.append(hoje)
        self._atualizar_streak()
        return self.xp_recompensa, self.moedas_recompensa

    def foi_completado_hoje(self) -> bool:
        return date.today().isoformat() in self.historico

    def _atualizar_streak(self):
        if len(self.historico) < 2:
            self.streak_atual = 1
        else:
            ontem = (date.today().toordinal() - 1)
            datas_ordinal = [date.fromisoformat(d).toordinal() for d in self.historico]
            if ontem in datas_ordinal:
                self.streak_atual += 1
            else:
                self.streak_atual = 1

        if self.streak_atual > self.maior_streak:
            self.maior_streak = self.streak_atual

    def para_dict(self) -> dict:
        return {
            "nome": self.nome,
            "icone": self.icone,
            "frequencia": self.frequencia.value,
            "xp_recompensa": self.xp_recompensa,
            "moedas_recompensa": self.moedas_recompensa,
            "streak_atual": self.streak_atual,
            "maior_streak": self.maior_streak,
            "historico": self.historico,
            "criado_em": self.criado_em
        }

    @classmethod
    def de_dict(cls, d: dict) -> "Habito":
        h = cls(
            nome=d["nome"],
            icone=d.get("icone", "⭐"),
            frequencia=Frequencia(d.get("frequencia", "diario")),
            xp_recompensa=d.get("xp_recompensa", 20),
            moedas_recompensa=d.get("moedas_recompensa", 5)
        )
        h.streak_atual = d.get("streak_atual", 0)
        h.maior_streak = d.get("maior_streak", 0)
        h.historico = d.get("historico", [])
        h.criado_em = d.get("criado_em", date.today().isoformat())
        return h


# ── MISSAO ─────────────────────────────────────────────

class Missao:
    """
    Uma missão é como um hábito, mas com prazo e recompensa maior.
    Pode ter prazo (data limite) ou ser sem prazo (None).
    Exemplo: "📚 Estudar Python 30 min" com prazo hoje e +50 XP de recompensa.
    """

    def __init__(self, nome: str, icone: str = "🗡️",
                 xp_recompensa: int = 50,
                 moedas_recompensa: int = 15,
                 prazo: str | None = None):   # prazo = data ISO ou None
        self.nome = nome
        self.icone = icone
        self.xp_recompensa = xp_recompensa
        self.moedas_recompensa = moedas_recompensa
        self.prazo = prazo                     # ex: "2026-06-25" ou None
        self.concluida = False
        self.concluida_em: str | None = None
        self.criada_em = date.today().isoformat()

    # ── verifica se passou do prazo sem concluir ──
    def esta_expirada(self) -> bool:
        if self.concluida or self.prazo is None:
            return False
        return date.today().isoformat() > self.prazo

    # ── conclui a missão e retorna (xp, moedas) ──
    def concluir(self) -> tuple[int, int]:
        if self.concluida:
            return 0, 0          # já concluída, não dá recompensa de novo
        if self.esta_expirada():
            return 0, 0          # passou do prazo, sem recompensa
        self.concluida = True
        self.concluida_em = date.today().isoformat()
        return self.xp_recompensa, self.moedas_recompensa

    # ── texto bonito do prazo para mostrar na tela ──
    def prazo_texto(self) -> str:
        if self.prazo is None:
            return "sem prazo"
        if self.prazo == date.today().isoformat():
            return "hoje!"
        if self.esta_expirada():
            return "⚠️ expirou"
        return f"até {self.prazo}"

    # ── salvar/carregar ──
    def para_dict(self) -> dict:
        return {
            "nome": self.nome,
            "icone": self.icone,
            "xp_recompensa": self.xp_recompensa,
            "moedas_recompensa": self.moedas_recompensa,
            "prazo": self.prazo,
            "concluida": self.concluida,
            "concluida_em": self.concluida_em,
            "criada_em": self.criada_em,
        }

    @classmethod
    def de_dict(cls, d: dict) -> "Missao":
        m = cls(
            nome=d["nome"],
            icone=d.get("icone", "🗡️"),
            xp_recompensa=d.get("xp_recompensa", 50),
            moedas_recompensa=d.get("moedas_recompensa", 15),
            prazo=d.get("prazo", None),
        )
        m.concluida = d.get("concluida", False)
        m.concluida_em = d.get("concluida_em", None)
        m.criada_em = d.get("criada_em", date.today().isoformat())
        return m


# ── PERSONAGEM ─────────────────────────────────────────

class Personagem:
    def __init__(self, nome: str = "Carol"):
        self.nome = nome
        self.xp_total = 0
        self.moedas = 0
        self.nivel_atual = NivelPersonagem.DORMINHOCA
        self.conquistas: list[str] = []

    def ganhar_xp(self, quantidade: int) -> bool:
        """Adiciona XP e retorna True se subiu de nível."""
        self.xp_total += quantidade
        nivel_anterior = self.nivel_atual
        self._verificar_nivel()
        return self.nivel_atual != nivel_anterior

    def ganhar_moedas(self, quantidade: int):
        self.moedas += quantidade

    def gastar_moedas(self, quantidade: int) -> bool:
        """Retorna True se tinha saldo suficiente."""
        if self.moedas >= quantidade:
            self.moedas -= quantidade
            return True
        return False

    def _verificar_nivel(self):
        for nivel in reversed(NivelPersonagem):
            if self.xp_total >= nivel.xp_necessario:
                self.nivel_atual = nivel
                break

    def xp_para_proximo_nivel(self) -> int | None:
        niveis = list(NivelPersonagem)
        idx = niveis.index(self.nivel_atual)
        if idx + 1 < len(niveis):
            return niveis[idx + 1].xp_necessario - self.xp_total
        return None

    def para_dict(self) -> dict:
        return {
            "nome": self.nome,
            "xp_total": self.xp_total,
            "moedas": self.moedas,
            "nivel_atual": self.nivel_atual.name,
            "conquistas": self.conquistas
        }

    @classmethod
    def de_dict(cls, d: dict) -> "Personagem":
        p = cls(nome=d.get("nome", "Carol"))
        p.xp_total = d.get("xp_total", 0)
        p.moedas = d.get("moedas", 0)
        p.nivel_atual = NivelPersonagem[d.get("nivel_atual", "DORMINHOCA")]
        p.conquistas = d.get("conquistas", [])
        return p


# ── SISTEMA DE RECOMPENSAS ─────────────────────────────

class SistemaDeRecompensas:
    CONQUISTAS = {
        "primeiro_habito":   ("🌱 Primeiro Passo",     "Complete seu primeiro hábito"),
        "streak_7":          ("🔥 Semana Perfeita",     "7 dias seguidos no mesmo hábito"),
        "streak_30":         ("💎 Mês Imparável",       "30 dias seguidos no mesmo hábito"),
        "nivel_3":           ("✨ Ficando Animada",     "Alcance o nível Animada"),
        "nivel_6":           ("🌟 Lendária",            "Alcance o nível Lendária"),
        "100_habitos":       ("💯 Centenária",          "Complete 100 hábitos no total"),
        "primeira_missao":   ("⚔️ Aventureira",         "Conclua sua primeira missão"),
        "10_missoes":        ("🏅 Caçadora de Missões", "Conclua 10 missões"),
    }

    def verificar(self, personagem: Personagem,
                  habitos: list[Habito],
                  missoes: list["Missao"] | None = None) -> list[str]:
        """Retorna lista de novas conquistas desbloqueadas."""
        novas = []
        missoes = missoes or []

        total_completos = sum(len(h.historico) for h in habitos)
        max_streak = max((h.streak_atual for h in habitos), default=0)
        total_missoes = sum(1 for m in missoes if m.concluida)

        checks = {
            "primeiro_habito": total_completos >= 1,
            "streak_7":        max_streak >= 7,
            "streak_30":       max_streak >= 30,
            "nivel_3":         personagem.nivel_atual.nivel >= 3,
            "nivel_6":         personagem.nivel_atual.nivel >= 6,
            "100_habitos":     total_completos >= 100,
            "primeira_missao": total_missoes >= 1,
            "10_missoes":      total_missoes >= 10,
        }

        for chave, condição in checks.items():
            if condição and chave not in personagem.conquistas:
                personagem.conquistas.append(chave)
                novas.append(chave)

        return novas


# ── SAVE MANAGER ───────────────────────────────────────

class SaveManager:
    ARQUIVO = "save.json"

    def salvar(self, personagem: Personagem,
               habitos: list[Habito],
               missoes: list[Missao] | None = None):
        dados = {
            "personagem": personagem.para_dict(),
            "habitos": [h.para_dict() for h in habitos],
            "missoes": [m.para_dict() for m in (missoes or [])],
            "salvo_em": datetime.now().isoformat()
        }
        with open(self.ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def carregar(self) -> tuple[Personagem, list[Habito], list[Missao]]:
        if not os.path.exists(self.ARQUIVO):
            return Personagem(), [], []
        with open(self.ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        personagem = Personagem.de_dict(dados.get("personagem", {}))
        habitos = [Habito.de_dict(h) for h in dados.get("habitos", [])]
        missoes = [Missao.de_dict(m) for m in dados.get("missoes", [])]
        return personagem, habitos, missoes