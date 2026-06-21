'''9. Neste exercício, você deverá criar um cadastro de uma lista de compras
de um supermercado contendo pelo menos 10 itens. Em seguida, crie
um laço que irá executar enquanto ainda houver itens na lista de
compras. Dentro desse laço, o programa deverá exibir o número do item
na lista juntamente com o seu nome.
O usuário deverá informar qual produto está comprando e, em seguida,
o programa deverá remover este item da lista de compras. O processo
deve continuar até que não restem mais itens na lista.
Certifique-se de fornecer instruções claras para o usuário e validar as
entradas fornecidas pelo usuário, garantindo que o item informado
realmente esteja presente na lista de compras.
'''

shopping_list = [
    "Arroz",
    "Feijão",
    "Macarrão",
    "Leite",
    "Pão",
    "Ovos",
    "Frango",
    "Carne",
    "Verduras",
    "Frutas"
]

while shopping_list:  # Enquanto houver itens na lista
    print("\nLista de Compras:")
    for index, item in enumerate(shopping_list):
        print(f"{index}. {item}")

    item_to_remove = input("Digite o nome do produto que você está comprando: ")

    if item_to_remove in shopping_list:
        shopping_list.remove(item_to_remove)
        print(f"{item_to_remove} foi removido da lista de compras.")
    else:
        print(f"{item_to_remove} não está na lista de compras. Por favor, tente novamente.")