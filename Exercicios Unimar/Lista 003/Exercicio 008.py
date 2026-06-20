'''
Faça um programa que receba o salário de um funcionário e calcule o
seu aumento de acordo com as seguintes regras: se o salário for menor
ou igual a R$1.500,00, o aumento será de 15%; caso contrário, o
aumento é de 10%
'''

salario = float(input('Digite o seu salário: '))
if salario <= 1500: # Se o salário for menor ou igual a 1500, o aumento será de 15%.
    aumento = salario * 0.15
    novo_salario = salario + aumento
    print(f'O seu novo salário é: R${novo_salario:.2f}')
else: # Se o salário for maior que 1500, o aumento será de 10%.
    aumento = salario * 0.10
    novo_salario = salario + aumento
    print(f'O seu novo salário é: R${novo_salario:.2f}')
