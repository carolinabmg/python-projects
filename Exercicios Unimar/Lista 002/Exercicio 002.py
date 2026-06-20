#Crie um algoritmo que pergunte quanto você ganha por hora e o número de horas que você trabalha por mês, o algoritmo deve calcular e mostrar qual seu salário naquele mês. (1 ponto)

ganho_hora = float(input("Quanto você ganha por hora? "))
horas_trabalhadas = float(input("Quantas horas você trabalha por mês? "))
salario_mensal = ganho_hora * horas_trabalhadas
print("Seu salário mensal é:", salario_mensal)
