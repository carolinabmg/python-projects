'''8. Faça um cadastro que grave nomes em uma lista (min. 10) e após isso
imprima cada nome junto com sua posição na lista. Exemplo de saída:
0. Henrique
1. Fernando Diniz.
2. Abel Braga.
3. Sofyan Amrabat.
4. Cristiano Messi.
5. Neymar Jr.
6. Vinicius Jr.
7. Rodrygo Goes.
8. Lucas Paquetá.
9. Casemiro.
'''

names = [] 
for i in range(10): 
    name = input(f"Digite o nome {i + 1}: ")
    names.append(name)

for index, name in enumerate(names): 
    print(f"{index}. {name}")
