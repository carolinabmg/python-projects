"""
main.py — Ponto de entrada do Memory Game Kawaii RPG.

Executar:
    python main.py
"""

import tkinter as tk
from game.app import KawaiiMemoryApp


def main():
    root = tk.Tk()
    KawaiiMemoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
