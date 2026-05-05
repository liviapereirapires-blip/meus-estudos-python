# Validação de entrada
# senha_correta = "Livia"
# tentativa = ""

# while tentativa != senha_correta:
#     tentativa = input("Digite a senha: ")
    
#     if tentativa != senha_correta:
#         print("Senha incorreta. Tente novamente.")
    
# print("Acesso permitido!")

# Calcular média de notas
# soma_notas = 0
# quantidade = 0

# while True:
#     nota = float(input("Digite uma nota (-1 para sair): "))
    
#     if nota == -1:
#         break
    
#     soma_notas += nota
#     quantidade += 1

# if quantidade > 0:
#     media = soma_notas / quantidade
#     print(f"Média das {quantidade} notas: {media:.2f}")
# else:
#     print("Nenhuma nota foi inserida.")

# Estrutura do programa:

# Gere um número aleatório

# Use um laço while para permitir múltiplos palpites

# Dê feedback após cada tentativa

# Conte o número de tentativas

# Finalize quando o usuário acertar

# Dica: use a biblioteca random para gerar o número (import random)



# numero = 18

# while True:
#     adivinhar = int(input('Adivinhe o número (1 a 100): '))
    
#     if adivinhar == numero:
#         print('Você acertou!')
#         break
#     elif adivinhar < numero:
#         print('Muito baixo!')
#     else:
#         print('Muito alto!')

import random

# Gerar número aleatório entre 1 e 100
numero_secreto = random.randint(1, 100)
tentativas = 0
acertou = False

print("Bem-vindo ao jogo de adivinhação!")
print("Estou pensando em um número entre 1 e 100.")

while not acertou:
    palpite = int(input("Qual é o seu palpite? "))
    tentativas += 1
    
    if palpite < numero_secreto:
        print("Tente um número MAIOR!")
    elif palpite > numero_secreto:
        print("Tente um número MENOR!")
    else:
        acertou = True
        print(f"Parabéns! Você acertou em {tentativas} tentativas.")


