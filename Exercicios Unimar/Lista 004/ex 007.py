'''7. Imprimir os números de 1 a 100 que são divisíveis por 3 usando um
loop'''

for number in range(1, 101):
    if number % 3 == 0:  # Verifica se o número é divisível por 3
        print(number)