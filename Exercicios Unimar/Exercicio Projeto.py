'''
Digamos que seja necessária a elaboração de um algoritmo para o desenvolvimento de um simples jogo do tipo quiz de perguntas e respostas com pontuação e avaliação de desempenho baseado nos critérios a seguir. 

 

* JOGO COM 5 PERGUNTAS SOBRE A DISCIPLINA CADA ACERTO VALE 10 OU 5 PONTOS.



10 PONTOS NA PRIMEIRA TENTATIVA

5 PONTOS NA SEGUNDA TENTATIVA

0 PONTOS SE ERRAR AS DUAS TENTATIVAS. 



* AO FINAL, EXIBIR A PONTUAÇÃO TOTAL . 

* EXIBIR MENSAGEM JUNTO A PONTUAÇÃO . 



"EXCELENTE" SE ATINGIR 50 PONTOS. 

"ÓTIMO" SE FIZER ENTRE 37 E 49 PONTOS. 

"BOM" SE FIZER ENTRE 25 E 36 PONTOS. 

"RUIM" SE FIZER MENOS DE 25 PONTOS. 



 

Elaborar um algoritmo capaz de permitir jogar este quiz de perguntas e respostas. 

É interessante observar que é possível utilizar uma versão testável na ferramenta Visual G, por exemplo, em função da maior complexidade do algoritmo. 

O mais importante na atividade é a lógica correta, avaliação de respostas e cálculo da pontuação, mas a aparência e uso de elementos especiais para melhoria da jogabilidade são desnecessários em termos de pontuação na atividade. 
'''

# Perguntas e respostas do quiz
pontuacao = 0

print("==============================================")
print(" QUIZ - ALGORITMO E LÓGICA DE PROGRAMAÇÃO")
print("==============================================")
print("Regras:")
print("10 pontos se acertar na primeira tentativa")
print("5 pontos se acertar na segunda tentativa")
print("0 pontos se errar as duas tentativas")
print("==============================================\n")

# Pergunta 1
print("1) Qual comando é usado para exibir uma mensagem na tela em Python?")
print("A) input")
print("B) print")
print("C) if")
print("D) while")
resposta = input("Digite a alternativa correta: ")

if resposta.upper() == "B":
    print("Resposta correta! Você ganhou 10 pontos.")
    pontuacao += 10
else:
    print("Resposta incorreta. Você tem mais uma tentativa.")
    resposta = input("Digite novamente a alternativa correta: ")

    if resposta.upper() == "B":
        print("Resposta correta na segunda tentativa! Você ganhou 5 pontos.")
        pontuacao += 5
    else:
        print("Resposta incorreta. Você ganhou 0 pontos nesta pergunta.")

print()

# Pergunta 2
print("2) Qual função é usada para receber dados digitados pelo usuário?")
print("A) print")
print("B) input")
print("C) else")
print("D) def")
resposta = input("Digite a alternativa correta: ")

if resposta.upper() == "B":
    print("Resposta correta! Você ganhou 10 pontos.")
    pontuacao += 10
else:
    print("Resposta incorreta. Você tem mais uma tentativa.")
    resposta = input("Digite novamente a alternativa correta: ")

    if resposta.upper() == "B":
        print("Resposta correta na segunda tentativa! Você ganhou 5 pontos.")
        pontuacao += 5
    else:
        print("Resposta incorreta. Você ganhou 0 pontos nesta pergunta.")

print()

# Pergunta 3
print("3) Qual estrutura é usada para tomar decisões em Python?")
print("A) if")
print("B) while")
print("C) for")
print("D) print")
resposta = input("Digite a alternativa correta: ")

if resposta.upper() == "A":
    print("Resposta correta! Você ganhou 10 pontos.")
    pontuacao += 10
else:
    print("Resposta incorreta. Você tem mais uma tentativa.")
    resposta = input("Digite novamente a alternativa correta: ")

    if resposta.upper() == "A":
        print("Resposta correta na segunda tentativa! Você ganhou 5 pontos.")
        pontuacao += 5
    else:
        print("Resposta incorreta. Você ganhou 0 pontos nesta pergunta.")

print()

# Pergunta 4
print("4) Qual operador é usado para verificar igualdade em Python?")
print("A) =")
print("B) ==")
print("C) >")
print("D) !=")
resposta = input("Digite a alternativa correta: ")

if resposta.upper() == "B":
    print("Resposta correta! Você ganhou 10 pontos.")
    pontuacao += 10
else:
    print("Resposta incorreta. Você tem mais uma tentativa.")
    resposta = input("Digite novamente a alternativa correta: ")

    if resposta.upper() == "B":
        print("Resposta correta na segunda tentativa! Você ganhou 5 pontos.")
        pontuacao += 5
    else:
        print("Resposta incorreta. Você ganhou 0 pontos nesta pergunta.")

print()

# Pergunta 5
print("5) Qual estrutura pode ser usada para repetir comandos várias vezes?")
print("A) else")
print("B) def")
print("C) while")
print("D) input")
resposta = input("Digite a alternativa correta: ")

if resposta.upper() == "C":
    print("Resposta correta! Você ganhou 10 pontos.")
    pontuacao += 10
else:
    print("Resposta incorreta. Você tem mais uma tentativa.")
    resposta = input("Digite novamente a alternativa correta: ")

    if resposta.upper() == "C":
        print("Resposta correta na segunda tentativa! Você ganhou 5 pontos.")
        pontuacao += 5
    else:
        print("Resposta incorreta. Você ganhou 0 pontos nesta pergunta.")

# Resultado final
print("\n==============================================")
print(f"PONTUAÇÃO FINAL: {pontuacao} pontos")

if pontuacao == 50:
    print("Mensagem: EXCELENTE")
elif 37 <= pontuacao <= 49:
    print("Mensagem: ÓTIMO")
elif 25 <= pontuacao <= 36:
    print("Mensagem: BOM")
else:
    print("Mensagem: RUIM")

print("==============================================")