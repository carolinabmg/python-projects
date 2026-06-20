'''7. Faça um programa que receba um número e diga se ele é par ou ímpar.'''

num = int(input('Digite um número: '))
if num % 2 == 0: # Se o número for divisível por 2, ele é par.
    print('O número é par.')
else: # Se o número não for divisível por 2, ele é ímpar.
    print('O número é ímpar.')
