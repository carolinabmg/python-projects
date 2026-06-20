'''
. Crie um algoritmo que receba quanto você ganha por hora e quantas
horas trabalhou no mês. O algoritmo deve calcular e mostrar o seu
salário no referido mês, sabendo que serão descontados 11% do
Imposto de Renda (IR) e mais 8% do INSS. No final o algoritmo deve
apresentar: (2 pontos)
a. Salário bruto
b. Valor do imposto de renda
c. Valor do INSS
d. Salário líquido (líquido = bruto – impostos)

'''

# Entrada de dados
ganho_hora = float(input("Quanto você ganha por hora? "))
horas_trabalhadas = float(input("Quantas horas você trabalhou no mês? "))
if ganho_hora < 0 or horas_trabalhadas < 0:
    print("Valor inválido. Por favor, insira valores positivos.")  
else:
    # Cálculo do salário bruto
    salario_bruto = ganho_hora * horas_trabalhadas

    # Cálculo dos impostos
    imposto_renda = salario_bruto * 0.11
    inss = salario_bruto * 0.08

    # Cálculo do salário líquido
    salario_liquido = salario_bruto - imposto_renda - inss

    # Apresentação dos resultados
    print(f"Salário bruto: R$ {salario_bruto:.2f}")
    print(f"Valor do imposto de renda: R$ {imposto_renda:.2f}")
    print(f"Valor do INSS: R$ {inss:.2f}")
    print(f"Salário líquido: R$ {salario_liquido:.2f}")