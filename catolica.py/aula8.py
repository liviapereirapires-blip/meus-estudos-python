# def calcular_area(base, altura):
#     area = (base * altura) / 2
#     return area
            
# # Chamando a função
# triangulo = calcular_area(5, 3)
# print(triangulo)  # Saída: 7.5

# Definição da função
# def dobrar_numero(numero):
#     resultado = numero * 2
#     return resultado

# # Três formas diferentes de chamar a mesma função
# valor1 = dobrar_numero(5)        # Guardando o retorno em uma variável
# print(dobrar_numero(10))         # Usando o retorno diretamente
# x = 15
# valor3 = dobrar_numero(x)        # Passando uma variável como argumento

# def potencia(base, expoente):
#     return base ** expoente
            
# # Chamada: ordem dos argumentos importa
# resultado = potencia(2, 3)  # 2³ = 8


# def cadastrar(nome, idade, cidade):
#     print(f"{nome}, {idade} anos, {cidade}")
 
# # A ordem não importa quando nomeamos
# cadastrar(cidade="Recife", nome="Ana", idade=25)

def verificar_idade(idade):
    if idade >= 18:
        return "Maior de idade"
    else:
        return "Menor de idade"
 
idade = input('Qual sua idade?')
status = verificar_idade(idade)
print(status) # "Menor de idade"


