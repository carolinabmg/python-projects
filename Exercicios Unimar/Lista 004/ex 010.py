'''10. Crie 3 listas (jogo, preço e avaliação (nota de 1 a 10)) e faça o cadastro
dessas 3 listas. As listagens devem seguir o padrão:
Nome: FIFA 23, Preço: 59.90, Nota: 9.7
Nome: GTA V, Preço: 49.90, Nota: 9.5
Nome: Call of Duty, Preço: 69.90, Nota: 8.5
● Exiba o jogo melhor avaliado.
● Exiba o jogo pior avaliado.
● Exiba o jogo mais caro.
● Exiba o jogo mais barato.
● Exiba todos os jogos.'''

games = []
prices = []
ratings = []
for i in range(3):
    game = input(f"Digite o nome do jogo {i + 1}: ")
    price = float(input(f"Digite o preço do jogo {i + 1}: "))
    rating = float(input(f"Digite a nota do jogo {i + 1} (de 1 a 10): "))

    games.append(game)
    prices.append(price)
    ratings.append(rating)

# Encontrar o jogo melhor avaliado
best_rating_index = ratings.index(max(ratings))
print(f"Jogo melhor avaliado: {games[best_rating_index]}, Nota: {ratings[best_rating_index]}")

# Encontrar o jogo pior avaliado
worst_rating_index = ratings.index(min(ratings))
print(f"Jogo pior avaliado: {games[worst_rating_index]}, Nota: {ratings[worst_rating_index]}")

# Encontrar o jogo mais caro
most_expensive_index = prices.index(max(prices))
print(f"Jogo mais caro: {games[most_expensive_index]}, Preço: {prices[most_expensive_index]}")

# Encontrar o jogo mais barato
least_expensive_index = prices.index(min(prices))
print(f"Jogo mais barato: {games[least_expensive_index]}, Preço: {prices[least_expensive_index]}")

# Exibir todos os jogos
print("\nTodos os jogos:")
for i in range(3):
    print(f"Nome: {games[i]}, Preço: {prices[i]}, Nota: {ratings[i]}")

