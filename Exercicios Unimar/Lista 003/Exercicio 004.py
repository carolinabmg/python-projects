'''Faça um programa que receba o peso e a altura de uma pessoa, calcule
o seu índice de massa corporal (IMC). Em seguida, diga em qual
categoria de peso ela se encontra (abaixo do peso, peso normal,
sobrepeso, obesidade grau 1, obesidade grau 2 ou obesidade grau 3).
O IMC é calculado pela fórmula: IMC = peso / (altura * altura)'''

peso = float(input('Digite o seu peso (em kg): '))
altura = float(input('Digite a sua altura (em metros): '))
imc = peso / (altura * altura)
print(f'O seu IMC é: {imc:.2f}')
if imc < 18.5: # Se o IMC for menor que 18.5, a pessoa está abaixo do peso.
    print('Você está abaixo do peso.')
elif imc < 25: # Se o IMC for menor que 25, a pessoa está com peso normal.
    print('Você está com peso normal.')
elif imc < 30: # Se o IMC for menor que 30, a pessoa está com sobrepeso.
    print('Você está com sobrepeso.')
elif imc < 35: # Se o IMC for menor que 35, a pessoa está com obesidade grau 1.
    print('Você está com obesidade grau 1.')
elif imc < 40: # Se o IMC for menor que 40, a pessoa está com obesidade grau 2.
    print('Você está com obesidade grau 2.')
else: # Se o IMC for maior ou igual a 40, a pessoa está com obesidade grau 3.
    print('Você está com obesidade grau 3.')