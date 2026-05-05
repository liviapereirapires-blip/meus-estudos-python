# import random

# # ── INÍCIO ──
# print("🎮 Jogo da Tabela Verdade!")
# print("Responda com V ou F")

# nome = input("Qual seu nome? ")
# pronto = input("Preparado? (sim/não): ")

# if pronto != "sim":
#     print("Volte quando estiver pronto!")
#     exit()

# # ── FASE 1 ──
# print("\n── FASE 1 ──")
# print("Diga se a expressão é Verdadeira (V) ou Falsa (F)")

# pontos = 0
# vidas = 6
# perguntas_usadas = []

# for i in range(6):
#     if vidas == 0:
#         break

#     # sorteia uma pergunta nova
#     while True:
#         p = random.choice([True, False])
#         q = random.choice([True, False])
#         tipo = random.choice(["not", "and", "or", "implica"])

#         if tipo == "not":
#             pergunta = f"¬{p}"
#             resposta = not p
#         elif tipo == "and":
#             pergunta = f"{p} ∧ {q}"
#             resposta = p and q
#         elif tipo == "or":
#             pergunta = f"{p} ∨ {q}"
#             resposta = p or q
#         else:
#             pergunta = f"{p} → {q}"
#             resposta = (not p) or q

#         if pergunta not in perguntas_usadas:
#             perguntas_usadas.append(pergunta)
#             break

#     print(f"\nPergunta {i+1}: {pergunta}")
#     print(f"❤️ Vidas: {vidas}  🏆 Pontos: {pontos}")
#     resposta_jogador = input("V ou F: ").strip().upper()

#     if (resposta_jogador == "V" and resposta == True) or (resposta_jogador == "F" and resposta == False):
#         print("✅ Acertou!")
#         pontos += 1
#     else:
#         print("❌ Errou!")
#         vidas -= 1

# print(f"\nFase 1 terminada! Pontos: {pontos}/6  Vidas: {vidas}")

# if vidas == 0 or pontos <= 3:
#     print(f"💀 Game Over, {nome}!")
#     exit()

# print(f"✅ Você passou para a Fase 2, {nome}!")

# # ── FASE 2 ──
# print("\n── FASE 2 – Tautologia, Contradição ou Contingência ──")
# print("""
# 🟢 TAUTOLOGIA   = sempre Verdadeira (todo V na tabela)
# 🔴 CONTRADIÇÃO  = sempre Falsa     (todo F na tabela)
# 🟡 CONTINGÊNCIA = mistura de V e F

# Digite: T, C ou G
# """)

# pontos2 = 0
# vidas2 = 5
# formulas_usadas = []

# # lista de fórmulas possíveis
# formulas = [
#     ("P ∧ Q",    "and"),
#     ("P ∨ Q",    "or"),
#     ("P → Q",    "implica"),
#     ("¬(P ∧ Q)", "nand"),
#     ("¬(P ∨ Q)", "nor"),
#     ("P ↔ Q",    "bicondicional"),
# ]

# random.shuffle(formulas)

# for i in range(min(6, len(formulas))):
#     if vidas2 == 0:
#         break

#     nome_formula, tipo = formulas[i]

#     # calcula resultado para todas as combinações de P e Q
#     resultados = []
#     for p in [True, False]:
#         for q in [True, False]:
#             if tipo == "and":
#                 resultados.append(p and q)
#             elif tipo == "or":
#                 resultados.append(p or q)
#             elif tipo == "implica":
#                 resultados.append((not p) or q)
#             elif tipo == "nand":
#                 resultados.append(not (p and q))
#             elif tipo == "nor":
#                 resultados.append(not (p or q))
#             elif tipo == "bicondicional":
#                 resultados.append(p == q)

#     if all(resultados):
#         classificacao = "Tautologia"
#     elif not any(resultados):
#         classificacao = "Contradição"
#     else:
#         classificacao = "Contingência"

#     print(f"\nFórmula {i+1}: {nome_formula}")
#     print(f"❤️ Vidas: {vidas2}  🏆 Pontos: {pontos2}")

#     # mostra a tabela verdade
#     print("P  | Q  | Resultado")
#     print("---|----|-----------")
#     for p in [True, False]:
#         for q in [True, False]:
#             if tipo == "and":
#                 res = p and q
#             elif tipo == "or":
#                 res = p or q
#             elif tipo == "implica":
#                 res = (not p) or q
#             elif tipo == "nand":
#                 res = not (p and q)
#             elif tipo == "nor":
#                 res = not (p or q)
#             elif tipo == "bicondicional":
#                 res = p == q

#             pv = "V" if p else "F"
#             qv = "V" if q else "F"
#             rv = "V" if res else "F"
#             print(f"{pv}  | {qv}  | {rv}")

#     resposta_jogador = input("\nT (Tautologia), C (Contradição) ou G (Contingência)? ").strip().upper()

#     mapa = {"T": "Tautologia", "C": "Contradição", "G": "Contingência"}
#     resposta_texto = mapa.get(resposta_jogador, "")

#     if resposta_texto == classificacao:
#         print(f"✅ Correto! É uma {classificacao}.")
#         pontos2 += 1
#     else:
#         print(f"❌ Errado! Era: {classificacao}.")
#         vidas2 -= 1

# # resultado final
# print(f"\n── FIM DO JOGO ──")
# print(f"Fase 1: {pontos}/6 pontos")
# print(f"Fase 2: {pontos2}/6 pontos")

# if vidas2 == 0:
#     print(f"💀 Game Over, {nome}! Sem vidas na Fase 2.")
# elif pontos2 >= 5:
#     print(f"🏆 Parabéns, {nome}! Você domina lógica proposicional!")
# elif pontos2 >= 3:
#     print(f"👏 Bom trabalho, {nome}! Continue estudando!")
# else:
#     print(f"😬 Pontuação baixa, {nome}. Revise o conteúdo!") 

import random

# ── CONFIGURAÇÕES ──────────────────────────────────────────────
FASE1_PERGUNTAS = 6
FASE1_VIDAS     = 6
FASE1_MINIMO    = 4  # pontos mínimos para passar

FASE2_PERGUNTAS = 6
FASE2_VIDAS     = 5

FORMULAS = [
    ("P ∧ Q",    "and"),
    ("P ∨ Q",    "or"),
    ("P → Q",    "implica"),
    ("¬(P ∧ Q)", "nand"),
    ("¬(P ∨ Q)", "nor"),
    ("P ↔ Q",    "bicondicional"),
]


# ── LÓGICA ─────────────────────────────────────────────────────
def avaliar(tipo: str, p: bool, q: bool) -> bool:
    match tipo:
        case "and":           return p and q
        case "or":            return p or q
        case "implica":       return (not p) or q
        case "nand":          return not (p and q)
        case "nor":           return not (p or q)
        case "bicondicional": return p == q
        case "not":           return not p
    raise ValueError(f"Tipo desconhecido: {tipo}")


def classificar(tipo: str) -> str:
    resultados = [avaliar(tipo, p, q) for p in (True, False) for q in (True, False)]
    if all(resultados):   return "Tautologia"
    if not any(resultados): return "Contradição"
    return "Contingência"


def gerar_pergunta_fase1() -> tuple[str, bool]:
    """Retorna (expressão_texto, resposta_correta)."""
    p = random.choice([True, False])
    q = random.choice([True, False])
    tipo = random.choice(["not", "and", "or", "implica"])

    match tipo:
        case "not":    return f"¬{p}", not p
        case "and":    return f"{p} ∧ {q}", p and q
        case "or":     return f"{p} ∨ {q}", p or q
        case "implica":return f"{p} → {q}", (not p) or q


def mostrar_tabela(tipo: str) -> None:
    print("P  | Q  | Resultado")
    print("---|----|-----------")
    for p in (True, False):
        for q in (True, False):
            res = avaliar(tipo, p, q)
            pv, qv, rv = ("V" if x else "F" for x in (p, q, res))
            print(f"{pv}  | {qv}  | {rv}")


# ── ENTRADA DO JOGADOR ─────────────────────────────────────────
def pedir_vf() -> bool:
    while True:
        r = input("V ou F: ").strip().upper()
        if r in ("V", "F"):
            return r == "V"
        print("Digite apenas V ou F.")


def pedir_classificacao() -> str:
    mapa = {"T": "Tautologia", "C": "Contradição", "G": "Contingência"}
    while True:
        r = input("T (Tautologia), C (Contradição) ou G (Contingência)? ").strip().upper()
        if r in mapa:
            return mapa[r]
        print("Digite apenas T, C ou G.")


# ── FASES ──────────────────────────────────────────────────────
def fase1() -> tuple[int, int]:
    print("\n── FASE 1 ──")
    print("Diga se a expressão é Verdadeira (V) ou Falsa (F)\n")

    pontos, vidas = 0, FASE1_VIDAS
    usadas: list[str] = []

    for i in range(FASE1_PERGUNTAS):
        if vidas == 0:
            break

        # sorteia sem repetir
        while True:
            expressao, resposta = gerar_pergunta_fase1()
            if expressao not in usadas:
                usadas.append(expressao)
                break

        print(f"Pergunta {i + 1}: {expressao}")
        print(f"❤️  Vidas: {vidas}  🏆 Pontos: {pontos}")

        if pedir_vf() == resposta:
            print("✅ Acertou!")
            pontos += 1
        else:
            print("❌ Errou!")
            vidas -= 1

    print(f"\nFase 1 encerrada — Pontos: {pontos}/{FASE1_PERGUNTAS}  Vidas: {vidas}")
    return pontos, vidas


def fase2() -> tuple[int, int]:
    print("\n── FASE 2 – Tautologia, Contradição ou Contingência ──")
    print("""
🟢 TAUTOLOGIA   = sempre Verdadeira (todo V na tabela)
🔴 CONTRADIÇÃO  = sempre Falsa     (todo F na tabela)
🟡 CONTINGÊNCIA = mistura de V e F

Digite: T, C ou G
""")

    formulas = FORMULAS[:]
    random.shuffle(formulas)

    pontos, vidas = 0, FASE2_VIDAS

    for i, (nome_formula, tipo) in enumerate(formulas[:FASE2_PERGUNTAS]):
        if vidas == 0:
            break

        gabarito = classificar(tipo)

        print(f"\nFórmula {i + 1}: {nome_formula}")
        print(f"❤️  Vidas: {vidas}  🏆 Pontos: {pontos}")
        mostrar_tabela(tipo)

        if pedir_classificacao() == gabarito:
            print(f"✅ Correto! É uma {gabarito}.")
            pontos += 1
        else:
            print(f"❌ Errado! Era: {gabarito}.")
            vidas -= 1

    print(f"\nFase 2 encerrada — Pontos: {pontos}/{FASE2_PERGUNTAS}  Vidas: {vidas}")
    return pontos, vidas


# ── MAIN ───────────────────────────────────────────────────────
def main() -> None:
    print("🎮 Jogo da Tabela Verdade!")
    print("Responda com V ou F\n")

    nome = input("Qual seu nome? ")

    if input("Preparado? (sim/não): ").strip().lower() != "sim":
        print("Volte quando estiver pronto!")
        return

    # Fase 1
    pontos1, vidas1 = fase1()

    if vidas1 == 0 or pontos1 < FASE1_MINIMO:
        print(f"💀 Game Over, {nome}! Você não passou da Fase 1.")
        return

    print(f"✅ Você passou para a Fase 2, {nome}!")

    # Fase 2
    pontos2, vidas2 = fase2()

    # Resultado final
    print("\n── FIM DO JOGO ──")
    print(f"Fase 1: {pontos1}/{FASE1_PERGUNTAS} pontos")
    print(f"Fase 2: {pontos2}/{FASE2_PERGUNTAS} pontos")

    if vidas2 == 0:
        print(f"💀 Game Over, {nome}! Sem vidas na Fase 2.")
    elif pontos2 >= 5:
        print(f"🏆 Parabéns, {nome}! Você domina lógica proposicional!")
    elif pontos2 >= 3:
        print(f"👏 Bom trabalho, {nome}! Continue estudando!")
    else:
        print(f"😬 Pontuação baixa, {nome}. Revise o conteúdo!")


if __name__ == "__main__":
    main()