# import random
# pontos1 = 0
# ultima_pergunta = ""
# vidas = 6

# print("🎮 Jogo da Tabela Verdade!")
# print(" Bem vindo a primeira fase do jogo")
# print("Responda com V (verdadeiro) ou F (falso)")
# nome = input(" Qual seu nome? ")
# preparação = input("praparados, sim/não? ")
# if preparação == "sim":
#     print(" Então vamos começar o jogo")
# else:
#     print(" volte quando estiver mais preprado")
#     exit()
# print(F"❤️  vidas: {vidas} | 🏆 pontos: {pontos1}")
# for i in range(6):

#     while True:
#         p = random.choice([True, False])
#         q = random.choice([True, False])
#         conectivo = random.choice(["not", "and", "or", "implica"])

#         if conectivo == "and":
#             pergunta = f"{p} ∧ {q}"
#             resposta = p and q

#         elif conectivo == "or":
#             pergunta = f"{p} ∨ {q}"
#             resposta = p or q

#         elif conectivo == "implica":
#             pergunta = f"{p} → {q}"
#             resposta = (not p) or q

#         else:
#             pergunta = f"¬{p}"
#             resposta = not p

#         # evita repetir pergunta
#         if pergunta != ultima_pergunta:
#             ultima_pergunta == pergunta
#             break

#     print("Pergunta:", pergunta)
#     user = input("Resposta (V/F): ").strip().upper()

#     if (user == "V" and resposta == True) or (user == "F" and resposta == False):
#         pontos1 += 1
#         print("✅ Acertou!")
#     else:
#         print("❌ Errou!")
#         vidas -= 1
# print(f"voce acabou o jogo com {vidas} vidas    ❤️")

# if pontos1 == 6:
#     print(f"muito bem!,{nome} você vai avançar para o proximo nivel")
# elif pontos1 > 3:
#     print(F" Quase que nao passa em {nome}, você ira para a segunda fase, mas lembre de estudar mais")
# else:
#     print(" Gamer over irmão 💀")             
#                                 #segunda fase


# import random 
# ultima_pergunta= " "
# pontos2 = 0 
# vidas2 = 6 
# print(f"🔥 BEM-VINDO À SEGUNDA FASE 🔥\n Aparti de agora as coisas ficam mais complicadas Sr(a){nome}...")

# #ramdon choices
# for i in range(3):
#     tautulogia = random.choice(["Ou está chovendo ou não está chovendo","Hoje é segunda-feira ou não é segunda-feira","Se eu estudo, então eu estudo"])
#     contingencia = random.choice(["Se chover, eu levo guarda-chuva","João estuda e passa na prova","Se fizer sol, vamos à praia"])
#     contradição = random.choice(["Está chovendo e não está chovendo ao mesmo tempo","Eu estou presente e não estou presente","A porta está aberta e fechada ao mesmo tempo"])
#     tipo = random.choice(["t","n","c"]).upper()
#     if tipo == "T":
#         pergunta = tautulogia
#         resposta = True
#     elif tipo == "N":
#         pergunta = contingencia
#         resposta = None
#     else:
#         pergunta = contradição
#         resposta = False       
#     if pergunta != ultima_pergunta:
#         ultima_pergunta = pergunta
#     else:        continue
#     print("Pergunta:", pergunta)                            
#     user = input("Resposta (T/N/C): ").strip().upper()
#     if (user == "T" and resposta == True) or (user == "N" and resposta == None) or (user == "C" and resposta == False):
#         pontos2 += 1
#         print("✅ Acertou!")
#     else:
#         print("❌ Errou!")
#         vidas2 -= 1                     
#         import random

# print(f"\n🚀 FASE 3: ALTA COMPLEXIDADE 🚀")
# print(f"Prepare-se {nome}, aqui a lógica testa seus limites!")
# print("Resolva a expressão composta (Responda V ou F):")

# pontos3 = 0
# # Usando as vidas que sobraram da fase anterior
# if 'vidas2' in locals():
#     vidas3 = vidas2
# else:
#     vidas3 = 6

# # Banco de questões complexas
# questoes_complexas = [
#     {"exp": "(True or False) and (not False)", "resp": True},
#     {"exp": "not (True and True) or (False)", "resp": False},
#     {"exp": "(10 > 5) and (not (2 < 1))", "resp": True},
#     {"exp": "(5 == 5) implies (3 > 10)", "resp": False}, # Se V então F = F
#     {"exp": "not ((True or False) and True)", "resp": False}
# ]

# random.shuffle(questoes_complexas)

# for i in range(3):
#     if vidas3 <= 0:
#         break
        
#     q = questoes_complexas[i]
#     print(f"\nQuestão {i+1}: {q['exp']}")
#     user = input("Resultado (V/F): ").strip().upper()
    
#     # Lógica de conversão V/F para True/False
#     user_bool = True if user == "V" else False
    
#     if user_bool == q['resp']:
#         print("✅ Lógica impecável! Você previu o comportamento do processador.")
#         pontos3 += 1
#     else:
#         print("❌ Curto-circuito! A expressão resultou em algo diferente.")
#         vidas3 -= 1

# if vidas3 > 0:
#     print(f"\n🌟 INCRÍVEL! Você completou o desafio com {vidas3} vidas!")
#     print(f"Sua pontuação final nesta fase: {pontos3}/3")
# else:
#     print("\n💀 Suas defesas falharam. O sistema foi invadido. Game Over.") 

import random

# ── CONFIGURAÇÕES ──────────────────────────────────────────────
FASE1_RODADAS = 6
FASE1_VIDAS   = 6
FASE1_MINIMO  = 4

FASE2_RODADAS = 6
FASE2_VIDAS   = 6
FASE2_MINIMO  = 3

FASE3_RODADAS = 5
# (fase 3 herda as vidas da fase 2)

# ── BANCOS DE QUESTÕES ─────────────────────────────────────────
TAUTOLOGIAS = [
    "Ou está chovendo ou não está chovendo",
    "Hoje é segunda-feira ou não é segunda-feira",
    "Se eu estudo, então eu estudo",
    "P ou (não P)",
    "Se P então P",
]

CONTINGENCIAS = [
    "Se chover, eu levo guarda-chuva",
    "João estuda e passa na prova",
    "Se fizer sol, vamos à praia",
    "P e Q",
    "Se P então Q",
]

CONTRADICOES = [
    "Está chovendo e não está chovendo ao mesmo tempo",
    "Eu estou presente e não estou presente",
    "A porta está aberta e fechada ao mesmo tempo",
    "P e (não P)",
    "Verdadeiro e Falso",
]

QUESTOES_FASE3 = [
    {"exp": "(True ou False) e (não False)",        "resp": True},
    {"exp": "não (True e True) ou False",           "resp": False},
    {"exp": "(10 > 5) e (não (2 < 1))",             "resp": True},
    {"exp": "não (True ou False) e True",           "resp": False},
    {"exp": "(True → False) e (False → True)",      "resp": False},
    {"exp": "não (False e False)",                  "resp": True},
    {"exp": "(True ↔ True) e (False ↔ False)",      "resp": True},
    {"exp": "(True e False) ou (False e True)",     "resp": False},
]


# ── LÓGICA PROPOSICIONAL ───────────────────────────────────────
def gerar_expressao() -> tuple[str, bool]:
    """Gera uma expressão aleatória de fase 1 e retorna (texto, resposta)."""
    p = random.choice([True, False])
    q = random.choice([True, False])
    tipo = random.choice(["not", "and", "or", "implica"])

    match tipo:
        case "not":     return f"¬{p}", not p
        case "and":     return f"{p} ∧ {q}", p and q
        case "or":      return f"{p} ∨ {q}", p or q
        case "implica": return f"{p} → {q}", (not p) or q


# ── ENTRADA VALIDADA ───────────────────────────────────────────
def pedir(prompt: str, opcoes: set[str]) -> str:
    while True:
        r = input(prompt).strip().upper()
        if r in opcoes:
            return r
        print(f"  ⚠️  Digite apenas: {'/'.join(sorted(opcoes))}")


# ── EXIBIÇÃO ───────────────────────────────────────────────────
def status(vidas: int, pontos: int) -> None:
    print(f"  ❤️  Vidas: {vidas}  |  🏆 Pontos: {pontos}")


def separador(titulo: str) -> None:
    print(f"\n{'─' * 45}")
    print(f"  {titulo}")
    print(f"{'─' * 45}")


# ── FASES ──────────────────────────────────────────────────────
def fase1() -> tuple[int, int]:
    separador("FASE 1 – Verdadeiro ou Falso?")
    print("  Diga se cada expressão é Verdadeira (V) ou Falsa (F).\n")

    pontos, vidas = 0, FASE1_VIDAS
    usadas: set[str] = set()

    for i in range(FASE1_RODADAS):
        if vidas == 0:
            break

        # Gera expressão sem repetição (limite de tentativas para evitar loop infinito)
        for _ in range(50):
            expr, resp = gerar_expressao()
            if expr not in usadas:
                usadas.add(expr)
                break

        print(f"\n  Pergunta {i + 1}: {expr}")
        status(vidas, pontos)

        acerto = pedir("  Resposta (V/F): ", {"V", "F"})
        correto = (acerto == "V") == resp

        if correto:
            print("  ✅ Acertou!")
            pontos += 1
        else:
            resp_str = "V" if resp else "F"
            print(f"  ❌ Errou! A resposta correta era {resp_str}.")
            vidas -= 1

    print(f"\n  Resultado da Fase 1: {pontos}/{FASE1_RODADAS} pontos | {vidas} vidas restantes")
    return pontos, vidas


def fase2(vidas_iniciais: int) -> tuple[int, int]:
    separador("FASE 2 – Tautologia, Contradição ou Contingência?")
    print("""  🟢 TAUTOLOGIA   (T) = sempre verdadeira
  🔴 CONTRADIÇÃO  (C) = sempre falsa
  🟡 CONTINGÊNCIA (N) = pode ser V ou F\n""")

    nomes = {"T": "Tautologia", "C": "Contradição", "N": "Contingência"}

    banco = (
        [("T", p) for p in TAUTOLOGIAS] +
        [("C", p) for p in CONTRADICOES] +
        [("N", p) for p in CONTINGENCIAS]
    )
    random.shuffle(banco)

    pontos, vidas = 0, vidas_iniciais

    for i, (gabarito, pergunta) in enumerate(banco[:FASE2_RODADAS]):
        if vidas == 0:
            break

        print(f"\n  Frase {i + 1}: \"{pergunta}\"")
        status(vidas, pontos)

        resposta = pedir("  T, C ou N? ", {"T", "C", "N"})

        if resposta == gabarito:
            print(f"  ✅ Correto! É uma {nomes[gabarito]}.")
            pontos += 1
        else:
            print(f"  ❌ Errado! Era: {nomes[gabarito]}.")
            vidas -= 1

    print(f"\n  Resultado da Fase 2: {pontos}/{FASE2_RODADAS} pontos | {vidas} vidas restantes")
    return pontos, vidas


def fase3(vidas_iniciais: int) -> tuple[int, int]:
    separador("FASE 3 – Expressões Compostas")
    print("  Avalie cada expressão lógica e responda V ou F.\n")

    questoes = QUESTOES_FASE3[:]
    random.shuffle(questoes)

    pontos, vidas = 0, vidas_iniciais

    for i, q in enumerate(questoes[:FASE3_RODADAS]):
        if vidas == 0:
            break

        print(f"\n  Questão {i + 1}: {q['exp']}")
        status(vidas, pontos)

        resposta = pedir("  Resultado (V/F): ", {"V", "F"})
        correto = (resposta == "V") == q["resp"]

        if correto:
            print("  ✅ Lógica impecável!")
            pontos += 1
        else:
            esperado = "V" if q["resp"] else "F"
            print(f"  ❌ Errou! O resultado correto era {esperado}.")
            vidas -= 1

    print(f"\n  Resultado da Fase 3: {pontos}/{FASE3_RODADAS} pontos | {vidas} vidas restantes")
    return pontos, vidas


# ── MAIN ───────────────────────────────────────────────────────
def main() -> None:
    separador("🎮 JOGO DA TABELA VERDADE")
    print("  Teste seus conhecimentos de lógica proposicional!\n")

    nome = input("  Qual seu nome? ").strip() or "Jogador"

    if pedir("  Preparado? (S/N): ", {"S", "N"}) != "S":
        print("  Volte quando estiver pronto. Até mais!")
        return

    # Fase 1
    p1, v1 = fase1()

    if v1 == 0 or p1 < FASE1_MINIMO:
        print(f"\n  💀 Game Over, {nome}. Você não passou da Fase 1.")
        print("     Dica: revise os conectivos ∧  ∨  →  ¬ e tente novamente!")
        return

    print(f"\n  ✅ Parabéns, {nome}! Avançando para a Fase 2...")

    # Fase 2 (herda as vidas da fase 1)
    p2, v2 = fase2(v1)

    if v2 == 0 or p2 < FASE2_MINIMO:
        print(f"\n  💀 Game Over, {nome}. Você não passou da Fase 2.")
        print("     Dica: revise tautologia, contradição e contingência!")
        return

    print(f"\n  🔥 Uau! Avançando para a Fase 3, {nome}...")

    # Fase 3 (herda as vidas da fase 2)
    p3, v3 = fase3(v2)

    # Placar final
    separador("PLACAR FINAL")
    total = p1 + p2 + p3
    maximo = FASE1_RODADAS + FASE2_RODADAS + FASE3_RODADAS
    print(f"  Fase 1: {p1}/{FASE1_RODADAS}")
    print(f"  Fase 2: {p2}/{FASE2_RODADAS}")
    print(f"  Fase 3: {p3}/{FASE3_RODADAS}")
    print(f"  Total:  {total}/{maximo} pontos\n")

    if v3 == 0:
        print(f"  💀 Game Over, {nome}! Sem vidas na Fase 3.")
    elif total >= maximo - 2:
        print(f"  🏆 PERFEITO, {nome}! Você domina lógica proposicional!")
    elif total >= maximo // 2:
        print(f"  👏 Bom trabalho, {nome}! Continue praticando.")
    else:
        print(f"  😬 Pontuação baixa, {nome}. Revise o conteúdo e tente de novo!")


if __name__ == "__main__":
    main()