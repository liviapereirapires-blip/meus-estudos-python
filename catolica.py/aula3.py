# # Meu primeiro programa
# nome = "lívia" # Variável
# idade = 18 # Variável numérica

# # Função print() mostra mensagem
# print("Olá, " + nome + "!")
# print("Você tem", idade, "anos.")

# if idade >= 18:
#  print("Você é maior de idade.")
# else:
#  print("Você é menor de idade.") 



# Exercicio 1 
 #Crie variáveis para armazenar seu nome, idade e altura. Depois, use print() para exibi-los com uma mensagem personalizada.
# nome = input(' qual seu nome? ')
# idade = int(input(' qual sua idade? '))
# altura = float(input(' qual sua altura? ')) 

# print(f' oi {nome}, você tem {idade} anos e tambem tem {altura} de altura')

# 💡 Dica importante
# Use input() para receber dados
# Use print() para mostrar dados
# Nunca coloque print() dentro de uma variável assim, a menos que você queira None

# Se quiser, 
# posso te mostrar um jeitinho de deixar a altura com duas casas decimais também 😉

# Exercicio 2
# Calcule a área de um retângulo. Crie variáveis para base e altura, faça o cálculo e mostre o resultado.
# base = float(input(' quanto é a base? '))
# altura = float(input( ' quanto é a altura? '))
# area_do_retangulo = (base * altura) 

# print(f' a area do retangulo é {area_do_retangulo} ') 

# Exercício 3
# Converta uma temperatura de Celsius para Fahrenheit usando a fórmula: F = C * 9/5 + 32
# celsius = float(input('Qual a temperatura em Celsius? '))
# resposta = (celsius * 9/5) + 32

# print(f'A resposta é {resposta}°F') 

# atencao
# resultado = 10 + 5 * 2
# print(resultado)  # 20 (não 30, pois * tem precedência sobre +)

# resultado = (10 + 5) * 2
# print(resultado)  # 30 (parênteses alteram a precedência)

# idade = 18
# altura = 1.75
# resultado = idade >= 18 and altura > 1.70
# print(resultado)  # True (primeiro avalia as comparações, depois o 'and')

# Calculando desconto com múltiplas condições
preco = 100
quantidade = 5
total = preco * quantidade

# Aplicando descontos
# if quantidade >= 10 and total > 1000:
#     desconto = 0.2  # 20% de desconto
# elif quantidade >= 5 or total > 500:
#     desconto = 0.1  # 10% de desconto
# else:
#     desconto = 0

# valor_final = total * (1 - desconto)
# print(f"Valor final: R$ {valor_final:.2f}")  # Valor final: R$ 450.00


#Desafio 1: Calcule a média ponderada de três notas, com pesos 2, 3 e 5.
# nota1 = float(input('Qual foi sua primeira nota? '))
# nota2 = float(input('Qual foi sua segunda nota? '))
# nota3 = float(input('Qual foi sua terceira nota? '))
# media = (nota1 * 2 + nota2 * 3 + nota3 * 5) / (2 + 3 + 5)

# print(f'sua media foi: {media}')  

# Desafio 2: Verifique se uma pessoa pode dirigir com base na idade e se possui habilitação.
idade = int(input(' Quantos anos você tem? '))
dirigir = bool(18>= idade)

print (f'você pode dirigir? {dirigir} pois você tem {idade} anos ')



