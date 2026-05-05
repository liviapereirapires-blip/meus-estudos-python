# Estrutura básica
# match variavel:
#     case padrão_1:
#         # código se padrão_1 corresponder
#     case padrão_2:
#         # código se padrão_2 corresponder
#     case _:
#         # código padrão (similar ao else)

# 
# dia = "segunda"

# if dia == "segunda":
#     print("Início da semana")
# elif dia == "quarta":
#     print("Meio da semana")
# elif dia == "sexta":
#     print("Quase fim de semana")
# elif dia == "sábado" or dia == "domingo":
#     print("Fim de semana!")
# else:
#     print("Dia comum") 

# dia = "segunda"

# match dia:
#     case "segunda":
#         print("Início da semana")
#     case "quarta":
#         print("Meio da semana")
#     case "sexta":
#         print("Quase fim de semana")
#     case "sábado" | "domingo":
#         print("Fim de semana!")
#     case _:
#         print("Dia comum")

# Exemplo Prático: Menu de Opções

# match comando.lower().split():
#     case ["ajuda"]:
#         return "Comandos disponíveis: ajuda, sair, calcular, sobre"
#     case ["sair"]:
#         return "Saindo do programa..."
#     case ["sobre"]:
#         return "Programa de demonstração do match/case - v1.0"
#     case ["calcular", operação, a, b] if operação in ["+", "-", "*", "/"]:
#         try:
#             a, b = float(a), float(b)
#             match operação:
#                 case "+": return f"Resultado: {a + b}"
#                 case "-": return f"Resultado: {a - b}"
#                 case "*": return f"Resultado: {a * b}"
#                 case "/": return f"Resultado: {a / b}"
#         except ValueError:
#             return "Erro: Valores inválidos"
#     case _:
#         return "Comando desconhecido. Digite 'ajuda' para ver os comandos."

# exercicio1: Crie uma função que use match/case para identificar e descrever diferentes tipos de dados.
# idade = int(input('Quantos anos você tem? '))

# match idade:
#     case _ if idade < 18:
#         print('Você é menor de idade')
#         print('Ainda não pode tirar a carteira de motorista')
#     case 18:
#         print('Você tem a idade exata para tirar a carteira de motorista')
#     case _:
#         print('Já passou da hora de tirar a carteira de motorista')


#Exercício 2: Calculadora
n1 = float(input(' escolha um numero:'))
n2 = float(input(' escolha outro:'))
operacao = input('escolha uma operacao: ( + ou x)')
match operacao: 
    case '+':
        print(f'a soma de {n1} + {n2} = {n1+n2}')
    case 'x' :
        print(f'a multiplicacao de {n1} x {n2}= {n1*n2}')
    case _:
        print('essa operacao nao tem aqui')    

  



    
