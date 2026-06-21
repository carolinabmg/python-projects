# 🎀 Memory Game Deluxe Kawaii RPG — v10.0

> *"Que a magia da memória esteja com você, feiticeira! ✨"*

Um jogo da memória com progressão RPG, loja de cosméticos, múltiplos temas visuais e sistema de perfis — feito inteiramente em Python com `tkinter`.

---

## 🖼️ Temas Visuais

| Kawaii 🎀 | Dark 🌙 | Harry Potter ⚡ | RGB 🌈 |
|-----------|---------|----------------|--------|
| Rosa pastel | Azul escuro | Dourado e bordô | Neon colorido |

---

## ✨ Funcionalidades

- 👥 **Perfis múltiplos** — crie e alterne entre feiticeiras
- ⭐ **XP, níveis e títulos** — de Aprendiz 🌱 até Deusa da Memória 💫
- 🪙 **Sistema de moedas** — ganhe jogando, gaste na loja
- 🛍️ **Loja** — avatares, cosméticos e temas visuais desbloqueáveis
- 🎨 **4 temas visuais** — Kawaii, Dark, Harry Potter e RGB
- 🦋 **Avatares equipáveis** — 8 opções para personalizar seu perfil
- 🔥 **4 dificuldades** — Fácil (4×4), Médio (4×5), Difícil (6×6) e Mestre (8×8)
- 🃏 **6 temas de cartas** — Kawaii, Natureza, Comida, Espaço, Harry Potter e Animais
- 🏆 **Ranking por dificuldade** — top 10 separado para cada modo
- 📊 **Estatísticas avançadas** — acurácia, média de tempo, melhor tempo
- 💾 **Salvamento automático** — salva silenciosamente a cada par encontrado
- 🔊 **Sons sintéticos** — via `pygame` (opcional, fallback silencioso)
- 🎯 **14 conquistas** desbloqueáveis
- 📜 **Histórico** das últimas 10 partidas por perfil

---

## 🚀 Como rodar

### 1. Pré-requisitos

- Python **3.10 ou superior**
- `tkinter` — já vem incluso na maioria das instalações Python

```bash
# No Linux, se não tiver tkinter:
sudo apt install python3-tk
```

### 2. Dependências opcionais (sons)

```bash
pip install pygame numpy
```

> Sem elas o jogo funciona normalmente, apenas sem efeitos sonoros.

### 3. Executar

```bash
python memory_kawaii_v10.py
```

---

## 🗂️ Arquivos gerados automaticamente

O jogo cria os seguintes arquivos na mesma pasta ao rodar:

| Arquivo | Conteúdo |
|---|---|
| `perfis_v10.json` | Dados de todos os perfis (XP, moedas, conquistas…) |
| `ranking_v10.json` | Top 10 por dificuldade |
| `jogo_salvo_v10.json` | Partida em andamento (auto-save) |
| `config_v10.json` | Tema visual e dificuldade preferidos |

---

## 🎮 Como jogar

1. **Crie um perfil** com seu nome de feiticeira
2. **Escolha a dificuldade** e o tema das cartas
3. Clique em **🎮 JOGAR**
4. Memorize as cartas durante a contagem regressiva (5 segundos)
5. Vire duas cartas por vez tentando encontrar os pares
6. A cada **3 acertos seguidos** você ativa o **Streak Bonus 🔥**
7. Ao vencer, ganhe **XP + moedas** e suba de nível!

---

## 🪙 Sistema de moedas

| Ação | Moedas ganhas |
|---|---|
| Par acertado | 🪙 +2 |
| Streak (a cada 3 acertos) | 🪙 +10 |
| Vitória | 🪙 +30 |
| Level Up | 🪙 +20 |
| Boas-vindas (novo perfil) | 🪙 +50 |

---

## 🏆 Conquistas

| Conquista | Como desbloquear |
|---|---|
| Primeira Vitória 🏆 | Vencer qualquer partida |
| Velocista ⚡ | Vencer em menos de 60 segundos |
| Speedrun Master ⚡⚡⚡ | Vencer em menos de 30 segundos |
| Streak Master 🔥🔥🔥 | Ativar um streak de 3 |
| Campeã Fácil 🌸 | Vencer no modo Fácil |
| Campeã Médio 💜 | Vencer no modo Médio |
| Campeã Difícil 🔥 | Vencer no modo Difícil |
| Campeã Mestre 🔥🔥 | Vencer no modo Mestre (8×8) |
| Mestre da Memória 🧙‍♀️ | Vencer no Mestre |
| 10 Vitórias 🎉 | Acumular 10 vitórias |
| Nível 10 👑 | Chegar ao nível 10 |
| Multimilionária 🪙 | Acumular 1000 moedas |
| Colecionadora 🛍️ | Desbloquear 3 cosméticos |

---

## 🧱 Estrutura do código

```
memory_kawaii_v10.py
│
├── TEMAS_VISUAIS        # paletas de cor para cada tema
├── TEMAS_CARTAS         # emojis por categoria
├── AVATARES / COSMETICOS_LOJA / TEMAS_LOJA
│
├── class FileManager    # todo acesso a disco centralizado
├── class Carta          # representa uma carta do tabuleiro
├── class Som            # sons sintéticos via pygame/numpy
├── class Jogadora       # perfil, XP, moedas, conquistas, histórico
├── class GerenciadorDePerfis
├── class Ranking        # top 10 separado por dificuldade
├── class Config         # configurações persistentes
└── class KawaiiMemoryGame  # lógica principal + toda a UI tkinter
```

---

## 🛠️ Tecnologias

- **Python 3.10+**
- **tkinter** — interface gráfica (stdlib)
- **json** — persistência de dados (stdlib)
- **pygame** *(opcional)* — sons
- **numpy** *(opcional)* — síntese de áudio

---

## 👩‍💻 Autora

Feito com 🩷 pela **feiticeira do código**
Projeto desenvolvido durante o curso de **Análise e Desenvolvimento de Sistemas (ADS)**

---

## 📝 Licença

Este projeto é de uso livre para fins educacionais e pessoais.
