'''Zé Papo-de-Pescador, homem de bem, comprou um microcomputador
para controlar o rendimento diário de seu trabalho. Toda vez que ele traz
um peso de peixes maior que o estabelecido pelo regulamento de pesca
do estado de São Paulo (30 quilos) deve pagar uma multa de R$ 3,00
por quilo excedente. Zé precisa que você faça um algoritmo que leia a
variável peso (peso de peixes) e calcule o excesso. Gravar na variável
excesso a quantidade de quilos além do limite e na variável multa o valor
da multa que Zé deverá pagar. Imprima os dados do algoritmo com as
mensagens adequadas. (2 pontos)'''

peso = float(input("Digite o peso dos peixes em quilos: "))
limite = 30.0
excesso = 0.0
multa = 0.0
if peso > limite:
    excesso = peso - limite
    multa = excesso * 3.0
    print("Excesso de peso:", excesso, "quilos")
    print("Valor da multa: R$", multa)  
else:
    print("Peso dentro do limite. Sem multa.")