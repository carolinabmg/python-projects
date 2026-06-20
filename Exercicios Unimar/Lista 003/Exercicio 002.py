'''
Faça um programa que receba uma temperatura em Celsius e converta
para Fahrenheit ou Kelvin, de acordo com a escolha do usuário.
Faça um programa que receba uma temperatura em Celsius e converta
para Fahrenheit ou Kelvin, de acordo com a escolha do usuário.
'''

# Entrada de dados
temperatura_celsius = float(input("Digite a temperatura em Celsius: "))

# Menu de opções
print("Escolha a unidade para conversão:")
print("1. Fahrenheit")
print("2. Kelvin")

opcao = int(input("Digite a opção desejada: "))

# Conversão de temperatura
if opcao == 1:
    temperatura_convertida = (temperatura_celsius * 9/5) + 32
    print(f"A temperatura em Fahrenheit é: {temperatura_convertida:.2f}°F")
elif opcao == 2:
    temperatura_convertida = temperatura_celsius + 273.15
    print(f"A temperatura em Kelvin é: {temperatura_convertida:.2f}K")
else:
    print("Opção inválida. Por favor, escolha 1 ou 2.")