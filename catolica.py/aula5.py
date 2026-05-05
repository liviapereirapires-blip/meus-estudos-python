# if condição:
    # bloco de código
    # executado se a condição for True
# if condição:
    # bloco executado se True
# else:
    # bloco executado se False
# if condição1:
# código se condição1 for True
# elif condição2:
# código se condição1 for False 
# e condição2 for True
# else:
# código se todas as condições
#  # anteriores forem False

# Vamos implementar um sistema simples de classificação de IMC (Índice de Massa Corporal)
# Categorias

# Abaixo de 18.5: Abaixo do peso

# 18.5 a 24.9: Peso normal

# 25.0 a 29.9: Sobrepeso

# 30.0 ou mais: Obesidade

peso = float(input(' Qual seu peso? '))
altura = float(input(' Qual sua altura? '))
imc = peso / (altura ** 2) 
if 18.5 > imc:
    print(' Você está abaixo do peso')
elif 18.5 >= imc <= 24.9:
    print(' Você tem peso normal ')
elif 25.0 >= imc <= 29.9:
    print( ' Você tem sobrepeso')
else:
    print(' Você tem obesidade') 


