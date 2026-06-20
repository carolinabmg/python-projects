'''
Faça um programa que receba a idade de uma pessoa e informe se ela
pode votar nas eleições ou não.
'''

idade = int(input('Digite a sua idade: '))
if idade >= 16: # Se a idade for maior ou igual a 16, a pessoa pode votar.
    print('Você pode votar nas eleições.')
else: # Se a idade for menor que 16, a pessoa não pode votar.
    print('Você não pode votar nas eleições.')
