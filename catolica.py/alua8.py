# Simula elementos sendo fornecidos um a um
# (e.g., de um arquivo, sensor, ou entrada do usuário)

# nome_procurado = "Carla"
# encontrado = False
# elementos_simulados = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda"] # Apenas para simular a ordem

# for i in range(len(elementos_simulados)):
#     elemento_atual = elementos_simulados[i] # Acesso simulado, sem array predefinido
#     if elemento_atual == nome_procurado:
#         print(f"'{nome_procurado}' foi encontrado no índice {i}!")
#         encontrado = True
#         break  # Interrompe a busca

# if not encontrado:
#     print(f"'{nome_procurado}' não foi encontrado na sequência.")     
# 
#  
    
# Simula números sendo fornecidos um a um
# (e.g., de um gerador, sensor, ou entrada do usuário)



# print("Números ímpares:")
# for num in range(1, 11): # Simula números de 1 a 10
#     if num % 2 == 0:
#         continue  # Pula para a próxima iteração
#     print(num, end=" ") # Imprime diretamente o número ímpar

# # Saída: Números ímpares: 1 3 5 7 9

# Imprimindo uma estrutura 3x3 sem usar uma matriz explícita
# linhas = 3
# colunas = 3

# numero_atual = 1
# for i in range(linhas): # Laço externo para as "linhas"
#     for j in range(colunas): # Laço interno para as "colunas" 
#         print(numero_atual, end=" ")
#         numero_atual += 1
#     print() # Nova linha após cada "linha" simulada

# Saída:
# 1 2 3
# 4 5 6
# 7 8 9
# frutas = ["maçã", "banana", "laranja"]
# for fruta in frutas:
#     print(fruta)
 
# for letra in "Python":
#     print(letra)
# # Saída: P, y, t, h, o, n

# for num in [1, 2, 3]:
#     print(num * 2)
# # Saída: 2, 4, 6

# for x in (10, 20, 30):
#     print(x // 10)
# # Saída: 1, 2, 3

nome_procurado = "Carla"
encontrado = False
elementos_simulados = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda"] # Apenas para simular a ordem

for i in range(len(elementos_simulados)):
    elemento_atual = elementos_simulados[i] # Acesso simulado, sem array predefinido
    if elemento_atual == nome_procurado:
        print(f"'{nome_procurado}' foi encontrado no índice {i}!")
        encontrado = True 
        break  # Interrompe a busca

if not encontrado:
    print(f"'{nome_procurado}' não foi encontrado na sequência.")
