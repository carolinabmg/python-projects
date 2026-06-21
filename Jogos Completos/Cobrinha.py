'''Snake Game - Jogo da Cobrinha
Desenvolvido por: Carolina Bueno
Data: 2026-06-21'''

import pygame
import random
import sys

# Inicialização
pygame.init()

# Configurações da tela
LARGURA = 600
ALTURA = 400
TAMANHO = 20

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🐍 Jogo da Cobrinha")

relogio = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 35)

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Posição inicial da cobra
cobra = [[100, 100]]
direcao = "DIREITA"

# Comida
comida_x = random.randrange(0, LARGURA, TAMANHO)
comida_y = random.randrange(0, ALTURA, TAMANHO)

pontuacao = 0
rodando = True

while rodando:

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_UP and direcao != "BAIXO":
                direcao = "CIMA"

            elif evento.key == pygame.K_DOWN and direcao != "CIMA":
                direcao = "BAIXO"

            elif evento.key == pygame.K_LEFT and direcao != "DIREITA":
                direcao = "ESQUERDA"

            elif evento.key == pygame.K_RIGHT and direcao != "ESQUERDA":
                direcao = "DIREITA"

    # Pega a cabeça
    x = cobra[0][0]
    y = cobra[0][1]

    # Movimento
    if direcao == "CIMA":
        y -= TAMANHO

    elif direcao == "BAIXO":
        y += TAMANHO

    elif direcao == "ESQUERDA":
        x -= TAMANHO

    elif direcao == "DIREITA":
        x += TAMANHO

    nova_cabeca = [x, y]
    cobra.insert(0, nova_cabeca)

    # Comeu a comida?
    if x == comida_x and y == comida_y:
        pontuacao += 1

        comida_x = random.randrange(0, LARGURA, TAMANHO)
        comida_y = random.randrange(0, ALTURA, TAMANHO)

    else:
        cobra.pop()

    # Colisão com parede
    if (
        x < 0
        or x >= LARGURA
        or y < 0
        or y >= ALTURA
    ):
        rodando = False

    # Colisão consigo mesma
    if nova_cabeca in cobra[1:]:
        rodando = False

    # Desenhar
    tela.fill(PRETO)

    # Cobra
    for parte in cobra:
        pygame.draw.rect(
            tela,
            VERDE,
            (parte[0], parte[1], TAMANHO, TAMANHO)
        )

    # Comida
    pygame.draw.rect(
        tela,
        VERMELHO,
        (comida_x, comida_y, TAMANHO, TAMANHO)
    )

    # Pontuação
    texto = fonte.render(
        f"Pontos: {pontuacao}",
        True,
        BRANCO
    )

    tela.blit(texto, (10, 10))

    pygame.display.update()
    relogio.tick(10)

# Tela de Game Over
tela.fill(PRETO)

fim = fonte.render(
    f"Game Over! Pontos: {pontuacao}",
    True,
    BRANCO
)

tela.blit(fim, (150, 180))
pygame.display.update()

pygame.time.wait(3000)

pygame.quit()