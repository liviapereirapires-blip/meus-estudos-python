# print("Olá, turma!")
# print("Python é", "muito", "legal!")
# print("Resultado:", 10 + 5)
# print("Posso usar 'aspas simples' dentro de aspas duplas")
# print('Ou "aspas duplas" dentro de aspas simples')
# print("""Texto com múltiplas
# linhas usando aspas triplas""")


 # Formatação básica
# nome = "Maria"
# idade = 20
# print("Nome:", nome, "- Idade:", idade)

# # Concatenação com +
# print("Nome: " + nome + " - Idade: " + str(idade))

# # f-strings (Python 3.6+)
# print(f"Nome: {nome} - Idade: {idade}")

# # Controle de fim de linha
# print("Isso não termina a linha", end=" >>> ")
# print("Continuação na mesma linha")

# Lendo entrada do usuário
# nome = input("Digite seu nome: ")
# print(f"Olá, {nome}!")
# # Lendo e convertendo para número
# idade = int(input("Digite sua idade: "))
# ano_nascimento = 2026 - idade
# print(f"Você nasceu em {ano_nascimento}")

# Programa para calcular área de um retângulo
print("Calculadora de Área de Retângulo")
print("-" * 30)  # Linha decorativa

base = float(input("Digite a base do retângulo (cm): "))
altura = float(input("Digite a altura do retângulo (cm): "))

area = base * altura

print(f"A área do retângulo é {area} cm²")