nome = 'Luiz Otávio'
altura = 1.80
peso = 95
imc = peso / altura ** 2

"f-strings"                                        
linha_1 = f'{nome} tem {altura:.2f} de altura,' #esse f' é para não precisar ficar potanto '' e , so bote {} 
linha_2 = f'pesa {peso} quilos e seu imc é'
linha_3 = f'{imc:.2f}'   # :.2f esse 2 f indica a quantidade de casas desimais do imc 

print(linha_1)
print(linha_2)
print(linha_3)

# Luiz Otávio tem 1.80 de altura,      # fiz o exercico na pagina exercicio2 
# pesa 95 quilos e seu IMC é
# 29.320987654320987  isso é sem os :.2f
#29.32 isso é com :.2f 