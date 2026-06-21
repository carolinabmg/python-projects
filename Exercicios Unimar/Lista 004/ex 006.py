'''Suponha que você tenha uma lista de números inteiros e queira imprimir
o índice e o número correspondente apenas para os números ímpares.
Escreva um programa que percorra a lista de números e imprima o
índice e o número para cada número ímpar utilizando a função
enumerate().
Utilizar a lista: [2, 5, 8, 11, 14]
'''


numbers = [2, 5, 8, 11, 14]

for index, number in enumerate(numbers):
    if number % 2 != 0:  # Verifica se o número é ímpar
        print(f"Índice: {index}, Número: {number}")