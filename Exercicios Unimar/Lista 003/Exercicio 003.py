'''
Faça um programa que receba um número e diga se ele é positivo,
negativo ou zero.
'''
num = float(input('Digite um número: '))

if num > 0: # Se o número for maior que zero, ele é positivo.
    print('O número é positivo.') 
elif num < 0: # Se o número for menor que zero, ele é negativo.
    print('O número é negativo.')
else: # Se o número não for maior nem menor que zero, ele é igual a zero.
    print('O número é zero.')