import random
pontos1 = 0
ultima_pergunta = ""
vidas = 6

print("🎮 Jogo da Tabela Verdade!")
print(" Bem vindo a primeira fase do jogo")
print("Responda com V (verdadeiro) ou F (falso)")
nome = input(" Qual seu nome? ")
preparação = input("praparados, sim/não? ")
if preparação == "sim":
    print(" Então vamos começar o jogo")
else:
    print(" volte quando estiver mais preprado")
    exit()
print(F"❤️  vidas: {vidas} | 🏆 pontos: {pontos1}")
for i in range(6):

    while True:
        p = random.choice([True, False])
        q = random.choice([True, False])
        conectivo = random.choice(["not", "and", "or", "implica"])

        if conectivo == "and":
            pergunta = f"{p} ∧ {q}"
            resposta = p and q

        elif conectivo == "or":
            pergunta = f"{p} ∨ {q}"
            resposta = p or q

        elif conectivo == "implica":
            pergunta = f"{p} → {q}"
            resposta = (not p) or q

        else:
            pergunta = f"¬{p}"
            resposta = not p

        # evita repetir pergunta
        if pergunta != ultima_pergunta:
            ultima_pergunta == pergunta
            break

    print("Pergunta:", pergunta)
    user = input("Resposta (V/F): ").strip().upper()

    if (user == "V" and resposta == True) or (user == "F" and resposta == False):
        pontos1 += 1
        print("✅ Acertou!")
    else:
        print("❌ Errou!")
        vidas -= 1
print(f"voce acabou o jogo com {vidas} vidas    ❤️")

if pontos1 == 6:
    print(f"muito bem!,{nome} você vai avançar para o proximo nivel")
elif pontos1 > 3:
    print(F" Quase que nao passa em {nome}, você ira para a segunda fase, mas lembre de estudar mais")
else:
    print(" Gamer over irmão 💀")             
                                #segunda fase


import random 
ultima_pergunta= " "
pontos2 = 0 
vidas2 = 6 
print(f"🔥 BEM-VINDO À SEGUNDA FASE 🔥\n Aparti de agora as coisas ficam mais complicadas Sr(a){nome}...")

#ramdon choices
for i in range(3):
    tautulogia = random.choice(["Ou está chovendo ou não está chovendo","Hoje é segunda-feira ou não é segunda-feira","Se eu estudo, então eu estudo"])
    contingencia = random.choice(["Se chover, eu levo guarda-chuva","João estuda e passa na prova","Se fizer sol, vamos à praia"])
    contradição = random.choice(["Está chovendo e não está chovendo ao mesmo tempo","Eu estou presente e não estou presente","A porta está aberta e fechada ao mesmo tempo"])
    tipo = random.choice(["t","n","c"]).upper()
    if tipo == "T":
        pergunta = tautulogia
        resposta = True
    elif tipo == "N":
        pergunta = contingencia
        resposta = None
    else:
        pergunta = contradição
        resposta = False       
    if pergunta != ultima_pergunta:
        ultima_pergunta = pergunta
    else:        continue
    print("Pergunta:", pergunta)                            
    user = input("Resposta (T/N/C): ").strip().upper()
    if (user == "T" and resposta == True) or (user == "N" and resposta == None) or (user == "C" and resposta == False):
        pontos2 += 1
        print("✅ Acertou!")
    else:
        print("❌ Errou!")
        vidas2 -= 1                     
        import random

print(f"\n🚀 FASE 3: ALTA COMPLEXIDADE 🚀")
print(f"Prepare-se {nome}, aqui a lógica testa seus limites!")
print("Resolva a expressão composta (Responda V ou F):")

pontos3 = 0
# Usando as vidas que sobraram da fase anterior
if 'vidas2' in locals():
    vidas3 = vidas2
else:
    vidas3 = 6

# Banco de questões complexas
questoes_complexas = [
    {"exp": "(True or False) and (not False)", "resp": True},
    {"exp": "not (True and True) or (False)", "resp": False},
    {"exp": "(10 > 5) and (not (2 < 1))", "resp": True},
    {"exp": "(5 == 5) implies (3 > 10)", "resp": False}, # Se V então F = F
    {"exp": "not ((True or False) and True)", "resp": False}
]

random.shuffle(questoes_complexas)

for i in range(3):
    if vidas3 <= 0:
        break
        
    q = questoes_complexas[i]
    print(f"\nQuestão {i+1}: {q['exp']}")
    user = input("Resultado (V/F): ").strip().upper()
    
    # Lógica de conversão V/F para True/False
    user_bool = True if user == "V" else False
    
    if user_bool == q['resp']:
        print("✅ Lógica impecável! Você previu o comportamento do processador.")
        pontos3 += 1
    else:
        print("❌ Curto-circuito! A expressão resultou em algo diferente.")
        vidas3 -= 1

if vidas3 > 0:
    print(f"\n🌟 INCRÍVEL! Você completou o desafio com {vidas3} vidas!")
    print(f"Sua pontuação final nesta fase: {pontos3}/3")
else:
    print("\n💀 Suas defesas falharam. O sistema foi invadido. Game Over.")
