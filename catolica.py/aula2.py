# num = int(input("Digite um número: "))

# if num % 2 == 0:
#     print(f"O número {num} é par.")
# else:
#     print(f"O número {num} é ímpar.")


# n1 = int(input("Digite o primeiro número: "))
# n2 = int(input("Digite o segundo número: "))
# n3 = int(input("Digite o terceiro número: ")) 

# maior_num = 0
# if maior_num < n1:
#     maior_num = n1
# if maior_num < n2:
#     maior_num = n2
# if maior_num < n3:
#     maior_num = n3

# print(f"O maior número é: {maior_num}")




n1 = int(input("Digite o primeiro número: "))
n2 = int(input("Digite o segundo número: "))
n3 = int(input("Digite o terceiro número: "))

maior = 0
menor = 100000000000
meio = 0

if maior < n1:
    maior = n1
if maior < n2:
    maior = n2
if maior < n3:
    maior = n3

if menor > n1:
    menor = n1
if menor > n2:
    menor = n2
if menor > n3:
    menor = n3

if n1 != maior and n1 != menor:
    meio = n1
if n2 != maior and n2 != menor:
    meio = n2
if n3 != maior and n3 != menor:
    meio = n3

print(f"Numeros em ordem crescente {menor}, {meio}, {maior}")