"""
Exercício
Peça ao usuário para digitar seu nome
Peça ao usuário para digitar sua idade
Se nome e idade forem digitados:
    Exiba:
        Seu nome é {nome}
        Seu nome invertido é {nome invertido}
        Seu nome contém (ou não) espaços
        Seu nome tem {n} letras
        A primeira letra do seu nome é {letra}
        A última letra do seu nome é {letra}
Se nada for digitado em nome ou idade: 
    exiba "Desculpe, você deixou campos vazios."
"""
# nome = input('Qual seu nome?')
# idade = int(input('Qual sua idade?'))
# if nome and idade :
#    print(f'Seu nome é {nome}')
#    print(f'Seu nome invertido é {nome[::-1]}')
#    if ' ' and nome:
#       print('seu nome contém espaço')
#    else:
#       print('seu nome NÃO contem espaço')
#    print(' Seu nome tem {len(nome)} letras')
#    print(f'A primeira letra do seu nome é {nome[0]}')
#    print(f'A última letra do seu nome é {nome[-1]}')
# else: 
#    print("Desculpe, você deixou campos vazios.")

# nome = input('Digite seu nome:')
# idade = input(int('Digite sua idade:'))
# invertido = nome[::-1]
# letras = len(nome)

# if nome and idade:
#     print(f'Seu nome é {nome})
#     print(f'Seu nome invertido é {invertido})
#     if ' ' in nome:
#         print('Seu nome contém espaços')
#     else:
#         print('Seu nome não contém espaços')
#     print(f'Seu nome tem {letras} letras')
#     print(f'A primeira letra do seu nome é {nome[0]}')
#     print(f'A última letra do seu nome é {invertido[0]}')
# else:
#     print('Desculpe, você deixou campos vazios.')
"""
Exercício
Peça ao usuário para digitar seu nome
Peça ao usuário para digitar sua idade
Se nome e idade forem digitados:
    Exiba:
        Seu nome é {nome}
        Seu nome invertido é {nome invertido}
        Seu nome contém (ou não) espaços
        Seu nome tem {n} letras
        A primeira letra do seu nome é {letra}
        A última letra do seu nome é {letra}
Se nada for digitado em nome ou idade: 
    exiba "Desculpe, você deixou campos vazios."
"""

nome = input('Digite seu nome: ')
idade = int(input('Digite sua idade: '))

invertido = nome[::-1]
letras = len(nome)

if nome and idade:
    print(f'Seu nome é {nome}')
    print(f'Seu nome invertido é {invertido}')

    if ' ' in nome:
        print('Seu nome contém espaços')
    else:
        print('Seu nome não contém espaços')

    print(f'Seu nome tem {letras} letras')
    print(f'A primeira letra do seu nome é {nome[0]}')
    print(f'A última letra do seu nome é {invertido[0]}')
else:
    print('Desculpe, você deixou campos vazios.')