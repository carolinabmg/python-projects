import random

opcoes = ["pedra", "papel", "tesoura"]

# 🏆 Placar — caixinhas que começam zeradas
vitorias = 0
derrotas = 0
empates = 0

jogando = True
while jogando:
    computador = random.choice(opcoes)
    jogador = input("Escolha pedra, papel ou tesoura: ").lower()

    print(f"Você escolheu: {jogador}")
    print(f"Computador escolheu: {computador}")

    if jogador == computador:
        print("Empate!")
        empates += 1          # +1 na caixinha de empates
    elif (jogador == "pedra" and computador == "tesoura") or \
         (jogador == "papel" and computador == "pedra") or \
         (jogador == "tesoura" and computador == "papel"):
        print("Você ganhou! 🎉")
        vitorias += 1         # +1 nas vitórias
    else:
        print("Computador ganhou! 🤖")
        derrotas += 1         # +1 nas derrotas

    # Mostra o placar depois de cada rodada
    print(f"📊 Placar → 🏆 {vitorias}  💀 {derrotas}  🤝 {empates}")

    # Pergunta se quer continuar (com a sua validação de s/n 💖)
    while True:
        resposta = input("Deseja jogar novamente? (s/n): ").lower()
        if resposta == "s":
            break             # sai dessa perguntinha e joga de novo
        elif resposta == "n":
            jogando = False   # avisa o loop grande pra parar
            break
        else:
            print("❌ Digite apenas s ou n.")

print(f"👋 Obrigado por jogar! Placar final → 🏆 {vitorias}  💀 {derrotas}  🤝 {empates}")
computador = random.choice(opcoes) #random.choice() é uma função da biblioteca random que seleciona aleatoriamente um elemento de uma sequência (como uma lista). Neste caso, ela escolhe aleatoriamente entre "pedra", "papel" e "tesoura" para o computador.

jogador = input("Escolha pedra, papel ou tesoura: ").lower() #.lower() para garantir que a entrada do usuário seja tratada como minúscula, independentemente de como ele digite.

print(f"Você escolheu: {jogador}")
print(f"Computador escolheu: {computador}")

if jogador == computador:
    print("Empate!")
elif (jogador == "pedra" and computador == "tesoura") or \
     (jogador == "papel" and computador == "pedra") or \
     (jogador == "tesoura" and computador == "papel"):  
    print("Você ganhou!")
else:    print("Computador ganhou!")

while True:
    jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower()

    if jogar_novamente == "s":
        computador = random.choice(opcoes)
        jogador = input("Escolha pedra, papel ou tesoura: ").lower()

        print(f"Você escolheu: {jogador}")
        print(f"Computador escolheu: {computador}")

        if jogador == computador:
            print("Empate!")
        elif (jogador == "pedra" and computador == "tesoura") or \
             (jogador == "papel" and computador == "pedra") or \
             (jogador == "tesoura" and computador == "papel"):
            print("Você ganhou!")
        else:
            print("Computador ganhou!")

    elif jogar_novamente == "n":
        print("👋 Obrigado por jogar!")
        break

    else:
        print("❌ Digite apenas s ou n.")
