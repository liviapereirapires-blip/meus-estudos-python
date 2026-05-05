# peso = float(input('Qual seu peso?'))
# altura = float(input('Qual sua altura'))
# imc = peso / altura ** 2

# if imc <= 18.5:
#     print('abaixo')
# elif 18.5 <= imc <= 24.9:
#     print('normal')
# elif 25.0 <= imc <= 29.9:
#     print('sobrepeso')
# else:
#     print('obeso')

print (' vamos calcular ')
n1 = float(input('escolha o primeiro numero'))
n2 = float(input(' escolha o segundo numero'))
operacao = input('escolha uma operaçao: +, -, /, x')

match operacao:
    case "+":
        print(f'a soma é {n1 + n2}')
    case "-":
        print(f'a subitraçao da {n1-n2}')
    case "x":
        print(f'a multiplicaçao é {n1*n2}')
    case "/":
        print(f'a divisao{n1/n2}')
    case _:
        print('essa operaçao nao tem na calculadora')

