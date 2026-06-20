# 🎀 Memory Game Deluxe Kawaii RPG — v10.0

Jogo da memória com progressão RPG, loja de skins, sistema de moedas e conquistas.

---

## 📁 Estrutura do projeto

```
kawaii_game/
├── main.py                  ← ponto de entrada
├── requirements.txt
├── README.md
├── game/
│   ├── __init__.py
│   ├── constants.py         ← constantes, enums, temas, catálogo da loja
│   ├── file_manager.py      ← acesso centralizado a disco (JSON)
│   ├── models.py            ← Carta, Jogadora, GerenciadorDePerfis, Ranking
│   ├── sound.py             ← sons sintéticos via pygame (opcional)
│   ├── widgets.py           ← componentes de UI reutilizáveis
│   ├── screens.py           ← telas de navegação (perfis, home, loja, etc.)
│   ├── game_screen.py       ← lógica e UI da partida ativa
│   └── app.py               ← KawaiiMemoryApp (orquestrador)
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_game.py         ← testes pytest (FileManager, modelos, loja, etc.)
```

---

## ▶️ Como jogar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

> **pygame** é opcional — sem ele o jogo roda normalmente, só sem sons.

### 2. Executar

```bash
cd kawaii_game
python main.py
```

---

## 🧪 Rodar os testes

```bash
cd kawaii_game
pytest tests/ -v
```

Saída esperada: todos os testes passando em verde. ✅

---

## 💰 Sistema de moedas e loja

| Dificuldade | Moedas por vitória |
|-------------|-------------------|
| Fácil       | 10                |
| Médio       | 20                |
| Difícil     | 35                |
| Streak bônus | +5 a cada x3    |

**Temas disponíveis na loja:**

| Tema         | Preço |
|--------------|-------|
| Comida 🍕    | 30    |
| Espaço 🚀    | 30    |
| Halloween 🎃 | 50    |
| Natal 🎄     | 50    |

---

## 📦 Gerar o `.exe` (Windows)

### 1. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 2. Gerar o executável

```bash
cd kawaii_game
pyinstaller --onefile --windowed --name "MemoryKawaii" main.py
```

### 3. Localizar o arquivo

O `.exe` estará em:

```
kawaii_game/dist/MemoryKawaii.exe
```

### Opções do comando explicadas

| Opção         | O que faz                                          |
|---------------|----------------------------------------------------|
| `--onefile`   | Gera um único `.exe` (sem pasta de dependências)   |
| `--windowed`  | Não abre o terminal preto junto com o jogo         |
| `--name`      | Nome do executável gerado                          |

> **Atenção:** o `.exe` gerado funciona apenas em Windows.  
> Os arquivos de save (`.json`) ficam na mesma pasta do executável.

---

## 🏗️ Decisões de arquitetura

| Princípio       | Como foi aplicado |
|-----------------|-------------------|
| Responsabilidade única | Cada módulo tem uma função clara |
| Sem "números mágicos" | Tudo em `constants.py` |
| Sem acesso direto a disco | Toda I/O passa por `FileManager` |
| UI separada da lógica | `models.py` não importa tkinter |
| Testabilidade | Classes de lógica independentes de UI |

---

## 🧙‍♀️ Feito com 💜 para portfólio ADS/Fatec
