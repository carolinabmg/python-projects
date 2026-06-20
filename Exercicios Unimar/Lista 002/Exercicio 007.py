'''Você foi contratado pela Unimar para ajudar na reforma dos blocos, o
seu papel é apoiar e facilitar as tomadas de decisões. Você vai ajudar a
otimizar os gastos para pintura, crie um programa para uma loja de
tintas. O programa deverá pedir o tamanho em metros quadrados da
área a ser pintada. Considere que a cobertura da tinta é de 1 litro para
cada 3 metros quadrados e que a tinta é vendida em latas de 18 litros,
que custam R$ 80,00. Informe ao usuário a quantidades de latas de tinta
a serem compradas e o preço total. (2 pontos)'''

# Entrada de dados
area_pintar = float(input("Qual o tamanho em metros quadrados da área a ser pintada? "))
if area_pintar < 0:
    print("Valor inválido. Por favor, insira um valor positivo.")   
else:
    # Cálculo da quantidade de tinta necessária
    litros_necessarios = area_pintar / 3

    # Cálculo da quantidade de latas necessárias
    latas_necessarias = litros_necessarios / 18

    # Arredondamento para cima, pois não é possível comprar uma fração de lata
    latas_comprar = int(latas_necessarias) + (1 if latas_necessarias % 1 > 0 else 0)

    # Cálculo do preço total
    preco_total = latas_comprar * 80

    # Apresentação dos resultados
    print(f"Quantidade de latas de tinta a serem compradas: {latas_comprar}")
    print(f"Preço total: R$ {preco_total:.2f}")