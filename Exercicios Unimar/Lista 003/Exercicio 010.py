'''
    Faça um programa que receba três notas de um aluno e calcule a
média aritmética dessas notas. Em seguida, verifique se a média é
maior ou igual a 7. Se for, exiba a mensagem “Aprovado”. Caso
contrário, verifique a média é maior ou igual a 5 e menor do que 7. Se
for, exiba a mensagem “Recuperação”. Caso contrário, exiba a
mensagem “Reprovado”
'''
notas = []
for i in range(3):
    nota = float(input(f'Digite a nota {i + 1}: '))
    notas.append(nota)
media = sum(notas) / len(notas)
if media >= 7: # Se a média for maior ou igual a 7, o aluno está aprovado.
    print('Aprovado')
elif media >= 5: # Se a média for maior ou igual a 5 e menor que 7, o aluno está em recuperação.
    print('Recuperação')
else: # Se a média for menor que 5, o aluno está reprovado.
    print('Reprovado')