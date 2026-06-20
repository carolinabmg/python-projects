'''Faça um programa que receba o ano de nascimento de uma pessoa e
diga qual é a sua faixa etária (criança, adolescente, adulto ou idoso).
● 0 a 12 anos: criança;
● 13 a 17 anos: adolescente;
● 18 a 59 anos: adulto;
● Acima de 59 anos: idoso.
'''
from datetime import date
ano_nascimento = int(input('Digite o seu ano de nascimento: '))
ano_atual = date.today().year
idade = ano_atual - ano_nascimento
print(f'Você tem {idade} anos.')
if idade <= 12: # Se a idade for menor ou igual a 12, a pessoa é criança.
    print('Você é uma criança.')
elif idade <= 17: # Se a idade for menor ou igual a 17, a pessoa é adolescente.
    print('Você é um adolescente.')
elif idade <= 59: # Se a idade for menor ou igual a 59, a pessoa é adulta.
    print('Você é um adulto.')
else: # Se a idade for maior que 59, a pessoa é idosa.
    print('Você é um idoso.')