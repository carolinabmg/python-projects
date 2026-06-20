import random

numero_secreto = random.randint(1, 20)

while True:
    palpite = int(input("Digite um número entre 1 e 20: "))

    if palpite == numero_secreto:
        print("🎉 Parabéns! Você acertou!")
        break

    elif palpite < numero_secreto:
        print("📈 O número secreto é MAIOR!")

    else:
        print("📉 O número secreto é MENOR!")