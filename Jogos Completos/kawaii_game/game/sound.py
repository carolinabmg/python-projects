"""
sound.py — Sons sintéticos via pygame.
Se pygame não estiver instalado, todos os métodos ficam em silêncio.
"""

import math
import time

try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    _PYGAME_OK = True
except Exception:
    _PYGAME_OK = False


def _tocar(freq: float, duracao: float, volume: float = 0.3):
    """Gera e reproduz uma onda senoidal simples."""
    if not _PYGAME_OK:
        return
    try:
        taxa   = 44100
        frames = int(taxa * duracao)
        onda   = bytearray()
        for i in range(frames):
            t      = i / taxa
            amostra = int(32767 * volume * math.sin(2 * math.pi * freq * t))
            onda   += amostra.to_bytes(2, byteorder="little", signed=True)
        som = pygame.mixer.Sound(buffer=bytes(onda))
        som.play()
    except Exception:
        pass


def acerto():
    _tocar(880, 0.12)


def erro():
    _tocar(220, 0.18)


def streak():
    _tocar(1046, 0.20)


def vitoria():
    for freq in [523, 659, 784, 1046]:
        _tocar(freq, 0.10)
        time.sleep(0.08)


def compra():
    _tocar(660, 0.10)
    time.sleep(0.05)
    _tocar(880, 0.10)
