n1 = input("Digite o primeiro binário: ")
n2 = input("Digite o segundo binário: ")
op = input("Escolha (+, -, *, /): ")

num1 = int(n1, 2)
num2 = int(n2, 2)

if op == '+':
    resultado = num1 + num2
elif op == '-':
    resultado = num1 - num2
elif op == '*':
    resultado = num1 * num2
elif op == '/':
    if num2 != 0:
        resultado = num1 // num2
    else:
        print("Erro: divisão por zero")
        exit()
else:
    print("Operação inválida")
    exit()

print("Resultado em binário:", bin(resultado)[2:])