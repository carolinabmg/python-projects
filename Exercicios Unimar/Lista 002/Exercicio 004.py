#Crie um algoritmo que receba a altura e o peso de uma pessoa e mostre
#seu Índice de Massa Corporal (IMC), utilizando a seguinte fórmula: (1
#ponto)

altura = float(input("Digite sua altura em metros: "))
peso = float(input("Digite seu peso em kg: "))
if altura > 0:
    imc = peso / (altura ** 2)
    print("Seu Índice de Massa Corporal (IMC) é:", "{imc:.2f}".format(imc=imc))
    print("Classificação do IMC:")
    if imc < 18.5:
        print("Abaixo do peso")
    elif 18.5 <= imc < 25:
        print("Peso normal")
    elif 25 <= imc < 30:
        print("Sobrepeso")
    else:
        print("Obesidade")
else:
    print("Altura inválida. Por favor, digite um valor positivo.")