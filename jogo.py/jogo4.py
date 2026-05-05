import random
import time
from colorama import init, Fore, Style

init(autoreset=True)

# ── CORES E ESTILOS ──
AZUL     = Fore.CYAN + Style.BRIGHT
VERDE    = Fore.GREEN + Style.BRIGHT
VERMELHO = Fore.RED + Style.BRIGHT
AMARELO  = Fore.YELLOW + Style.BRIGHT
ROXO     = Fore.MAGENTA + Style.BRIGHT
BRANCO   = Fore.WHITE + Style.BRIGHT
RESET    = Style.RESET_ALL
CINZA    = Fore.WHITE + Style.DIM

def digitar(texto, delay=0.03):
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def linha(char="─", n=54, cor=AZUL):
    print(cor + char * n + RESET)

def espaco():
    print()

def pedir_vf(prompt):
    """Pede V ou F, rejeitando entradas inválidas."""
    while True:
        r = input(prompt).strip().upper()
        if r in ("V", "F"):
            return r
        print(VERMELHO + "  ⚠  Digite apenas V ou F." + RESET)

def colorir_vf(letra):
    if letra == "V":
        return VERDE + "V" + RESET
    return VERMELHO + "F" + RESET

# ══════════════════════════════════════════════════
#  TELA DE ABERTURA
# ══════════════════════════════════════════════════
espaco()
linha("═", 54, ROXO)
print(ROXO + "  ██╗      ██████╗  ██████╗ ██╗ ██████╗  █████╗ " + RESET)
print(ROXO + "  ██║     ██╔═══██╗██╔════╝ ██║██╔════╝ ██╔══██╗" + RESET)
print(ROXO + "  ██║     ██║   ██║██║  ███╗██║██║      ███████║" + RESET)
print(ROXO + "  ██║     ██║   ██║██║   ██║██║██║      ██╔══██║" + RESET)
print(ROXO + "  ███████╗╚██████╔╝╚██████╔╝██║╚██████╗ ██║  ██║" + RESET)
print(ROXO + "  ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝ ╚═╝  ╚═╝" + RESET)
linha("═", 54, ROXO)
print(AZUL + "        🧠  JOGO DA TABELA VERDADE  🧠" + RESET)
linha("═", 54, ROXO)
espaco()

time.sleep(0.5)
digitar(BRANCO + "  Bem-vindo ao desafio de Lógica Proposicional!" + RESET)
espaco()

nome = input(AMARELO + "  👤 Qual seu nome? " + RESET).strip() or "Jogador"
espaco()
pronto = input(AMARELO + f"  {nome}, você está preparado(a)? (sim/não): " + RESET).strip().lower()

if pronto != "sim":
    espaco()
    digitar(VERMELHO + f"  Tudo bem! Volte quando estiver pronto, {nome}. 📖" + RESET)
    espaco()
    exit()

espaco()
digitar(VERDE + f"  Ótimo, {nome}! Vamos começar... 🚀" + RESET, delay=0.04)
time.sleep(0.8)
print("")
# ══════════════════════════════════════════════════
#  FASE 1 – TABELA VERDADE
# ══════════════════════════════════════════════════
espaco()
linha("═", 54, AZUL)
print(AZUL + "  🔵  FASE 1 — Verdadeiro ou Falso?" + RESET)
linha("═", 54, AZUL)
print(CINZA + "  Avalie a expressão e responda V ou F." + RESET)
espaco()

pontos = 0
vidas = 6
perguntas_usadas = []

for i in range(6):
    if vidas == 0:
        break

    while True:
        p = random.choice([True, False])
        q = random.choice([True, False])
        tipo = random.choice(["not", "and", "or", "implica"])

        if tipo == "not":
            pergunta = f"¬{p}"
            resposta = not p
        elif tipo == "and":
            pergunta = f"{p} ∧ {q}"
            resposta = p and q
        elif tipo == "or":
            pergunta = f"{p} ∨ {q}"
            resposta = p or q
        else:
            pergunta = f"{p} → {q}"
            resposta = (not p) or q

        if pergunta not in perguntas_usadas:
            perguntas_usadas.append(pergunta)
            break

    coracoes = "❤️ " * vidas + "🖤 " * (6 - vidas)
    espaco()
    linha("─", 54, CINZA)
    print(AMARELO + f"  Pergunta {i+1}/6" + RESET + "  " + coracoes + AMARELO + f"  🏆 {pontos} pts" + RESET)
    linha("─", 54, CINZA)
    espaco()
    print(BRANCO + f"       {pergunta}" + RESET)
    espaco()

    resposta_jogador = pedir_vf(AMARELO + "  ➤ Sua resposta (V/F): " + RESET)

    espaco()
    if (resposta_jogador == "V" and resposta is True) or (resposta_jogador == "F" and resposta is False):
        print(VERDE + "  ╔══════════════════════╗")
        print(VERDE + "  ║   ✅  ACERTOU!  +1   ║")
        print(VERDE + "  ╚══════════════════════╝" + RESET)
        pontos += 1
    else:
        correto = "V" if resposta else "F"
        print(VERMELHO + "  ╔══════════════════════════════╗")
        print(VERMELHO + f"  ║  ❌  ERROU! Correto: {correto}      ║")
        print(VERMELHO + "  ╚══════════════════════════════╝" + RESET)
        vidas -= 1

    time.sleep(0.5)

espaco()
linha("═", 54, AZUL)
print(AZUL + "  🔵  RESULTADO — FASE 1" + RESET)
linha("═", 54, AZUL)
print(BRANCO + f"  Pontos: {pontos}/6   Vidas restantes: {vidas}" + RESET)
linha("═", 54, AZUL)
espaco()

if vidas == 0 or pontos < 3:
    digitar(VERMELHO + f"  💀 Game Over, {nome}! Pontuação insuficiente." + RESET)
    espaco()
    exit()

digitar(VERDE + f"  🎉 Você passou para a Fase 2, {nome}!" + RESET)
espaco()
time.sleep(0.5)

continuar = input(AMARELO + "  Pronto para a Fase 2? (sim/não): " + RESET).strip().lower()
if continuar != "sim":
    digitar(AMARELO + f"\n  Tudo bem! Volte quando quiser, {nome}. 👋" + RESET)
    exit()

# ══════════════════════════════════════════════════
#  FASE 2 – MONTAR A TABELA + CLASSIFICAR
# ══════════════════════════════════════════════════
espaco()
linha("═", 54, ROXO)
print(ROXO + "  🟣  FASE 2 — Monte a Tabela Verdade!" + RESET)
linha("═", 54, ROXO)
espaco()
digitar(BRANCO + "  Agora é você quem preenche a tabela!" + RESET, delay=0.02)
espaco()
digitar(CINZA  + "  Para cada combinação de P e Q mostrada," + RESET, delay=0.02)
digitar(CINZA  + "  calcule o resultado da fórmula e responda V ou F." + RESET, delay=0.02)
digitar(CINZA  + "  Depois classifique a fórmula inteira." + RESET, delay=0.02)
espaco()
print(VERDE    + "  🟢 T = TAUTOLOGIA   → sempre Verdadeira" + RESET)
print(VERMELHO + "  🔴 C = CONTRADIÇÃO  → sempre Falsa" + RESET)
print(AMARELO  + "  🟡 G = CONTINGÊNCIA → mistura de V e F" + RESET)
espaco()
time.sleep(0.8)

# ── POOL DE FÓRMULAS ──────────────────────────────────────────────────────
formulas = [
    # ── Tautologias (sempre V — fáceis de perceber) ───────────────────────
    ("P ∨ ¬q",    lambda p, : p or not p,    "Tautologia"),   # lei do terceiro excluído
    ("¬P ∨ P",    lambda p, q: not p or p,    "Tautologia"),   # idem, ordem trocada
    ("P → P",     lambda p, q: (not p) or p,  "Tautologia"),   # qualquer coisa implica ela mesma

    # ── Contradições (sempre F — fáceis de perceber) ─────────────────────
    ("P ∧ ¬P",    lambda p, q: p and not p,   "Contradição"),  # P e não-P ao mesmo tempo
    ("¬P ∧ P",    lambda p, q: not p and p,   "Contradição"),  # idem, ordem trocada
    ("¬(P ∨ ¬P)", lambda p, q: not(p or not p), "Contradição"),# negação de tautologia

    # ── Contingências (mistura — operadores básicos com 1 ou 2 variáveis) ─
    ("P ∧ Q",     lambda p, q: p and q,        "Contingência"), # E
    ("P ∨ Q",     lambda p, q: p or q,         "Contingência"), # OU
    ("¬P ∧ Q",    lambda p, q: not p and q,    "Contingência"), # não-P e Q
    ("P ∧ ¬Q",    lambda p, q: p and not q,    "Contingência"), # P e não-Q
    ("¬P ∨ Q",    lambda p, q: not p or q,     "Contingência"), # não-P ou Q
    ("¬P ∨ ¬Q",   lambda p, q: not p or not q, "Contingência"), # não-P ou não-Q
]

# Garante ao menos 1 de cada categoria nas 6 questões
pool_por_cat = {cat: [f for f in formulas if f[2] == cat] for cat in ["Tautologia", "Contradição", "Contingência"]}
for v in pool_por_cat.values():
    random.shuffle(v)

selecionadas = [pool_por_cat[c].pop() for c in ["Tautologia", "Contradição", "Contingência"]]
restantes = [f for f in formulas if f not in selecionadas]
random.shuffle(restantes)
selecionadas += restantes[:3]
random.shuffle(selecionadas)

combinacoes = [(True, True), (True, False), (False, True), (False, False)]
label = {True: "V", False: "F"}

pontos2 = 0
vidas2  = 5

for i, (nome_formula, fn, classificacao) in enumerate(selecionadas):
    if vidas2 == 0:
        break

    coracoes2 = "❤️ " * vidas2 + "🖤 " * (5 - vidas2)
    espaco()
    linha("─", 54, CINZA)
    print(AMARELO + f"  Fórmula {i+1}/6" + RESET + "  " + coracoes2 + AMARELO + f"  🏆 {pontos2} pts" + RESET)
    linha("─", 54, CINZA)
    espaco()
    print(ROXO + f"  Fórmula:  {nome_formula}" + RESET)
    espaco()
    print(CINZA + "  Preencha o resultado de cada linha (V ou F):" + RESET)
    espaco()

    # ── Cabeçalho ─────────────────────────────────────────────────────────
    print(CINZA + "  ┌─────┬─────┬──────────────────────┐")
    print(CINZA + "  │  P  │  Q  │  Resultado           │")
    print(CINZA + "  ├─────┼─────┼──────────────────────┤" + RESET)

    # ── Jogador preenche linha por linha ──────────────────────────────────
    respostas_jogador  = []
    respostas_corretas = []

    for p, q in combinacoes:
        correto_bool = fn(p, q)
        correto_str  = "V" if correto_bool else "F"
        respostas_corretas.append(correto_str)

        pv = colorir_vf(label[p])
        qv = colorir_vf(label[q])

        print(f"  {CINZA}│{RESET}  {pv}  {CINZA}│{RESET}  {qv}  {CINZA}│{RESET}  ", end="")
        resp = pedir_vf(AMARELO + "? " + RESET)
        respostas_jogador.append(resp)

    print(CINZA + "  └─────┴─────┴──────────────────────┘" + RESET)
    espaco()

    # ── Gabarito da tabela ────────────────────────────────────────────────
    acertos_tabela = sum(r == c for r, c in zip(respostas_jogador, respostas_corretas))

    print(CINZA + "  ── Gabarito ──────────────────────────────────" + RESET)
    print(CINZA + "  ┌─────┬─────┬──────────┬──────────┐")
    print(CINZA + "  │  P  │  Q  │  Você    │ Correto  │")
    print(CINZA + "  ├─────┼─────┼──────────┼──────────┤" + RESET)

    for (p, q), rj, rc in zip(combinacoes, respostas_jogador, respostas_corretas):
        pv   = colorir_vf(label[p])
        qv   = colorir_vf(label[q])
        rjv  = colorir_vf(rj)
        rcv  = colorir_vf(rc)
        icone = VERDE + "✔" + RESET if rj == rc else VERMELHO + "✘" + RESET
        print(f"  {CINZA}│{RESET}  {pv}  {CINZA}│{RESET}  {qv}  {CINZA}│{RESET}  {rjv}  {icone}   {CINZA}│{RESET}    {rcv}    {CINZA}│{RESET}")

    print(CINZA + "  └─────┴─────┴──────────┴──────────┘" + RESET)
    espaco()

    if acertos_tabela == 4:
        print(VERDE + f"  ✅ Tabela perfeita! 4/4 linhas corretas." + RESET)
    else:
        print(AMARELO + f"  ⚠  {acertos_tabela}/4 linhas corretas na tabela." + RESET)

    espaco()

    # ── Classificação ─────────────────────────────────────────────────────
    print(BRANCO + "  Agora classifique a fórmula:" + RESET)
    print(CINZA  + "  T = Tautologia  |  C = Contradição  |  G = Contingência" + RESET)
    espaco()

    while True:
        classe_resp = input(AMARELO + "  ➤ T, C ou G? " + RESET).strip().upper()
        if classe_resp in ("T", "C", "G"):
            break
        print(VERMELHO + "  ⚠  Digite apenas T, C ou G." + RESET)

    mapa        = {"T": "Tautologia", "C": "Contradição", "G": "Contingência"}
    classe_texto = mapa[classe_resp]

    espaco()

    # ── Pontuação: tabela = 1pt, classificação = 1pt ──────────────────────
    ganhou_tabela = acertos_tabela == 4
    ganhou_classe = classe_texto == classificacao
    pontos2      += int(ganhou_tabela) + int(ganhou_classe)

    if ganhou_tabela and ganhou_classe:
        print(VERDE + "  ╔══════════════════════════════════════════╗")
        print(VERDE + "  ║  🏆  PERFEITO! Tabela + Classe   +2 pts ║")
        print(VERDE + "  ╚══════════════════════════════════════════╝" + RESET)
    elif ganhou_tabela and not ganhou_classe:
        print(AMARELO + "  ╔══════════════════════════════════════════╗")
        print(AMARELO + "  ║  ✅ Tabela certa  ❌ Classe errada  +1  ║")
        print(AMARELO + f"  ║  Correto: {classificacao:<30}║")
        print(AMARELO + "  ╚══════════════════════════════════════════╝" + RESET)
        vidas2 -= 1
    elif not ganhou_tabela and ganhou_classe:
        print(AMARELO + "  ╔══════════════════════════════════════════╗")
        print(AMARELO + "  ║  ❌ Tabela errada  ✅ Classe certa  +1  ║")
        print(AMARELO + "  ╚══════════════════════════════════════════╝" + RESET)
        vidas2 -= 1
    else:
        print(VERMELHO + "  ╔══════════════════════════════════════════╗")
        print(VERMELHO + "  ║  ❌ Tabela errada  ❌ Classe errada  +0  ║")
        print(VERMELHO + f"  ║  Classe correta: {classificacao:<22}║")
        print(VERMELHO + "  ╚══════════════════════════════════════════╝" + RESET)
        vidas2 -= 1

    time.sleep(0.6)

# ══════════════════════════════════════════════════
#  TELA FINAL
# ══════════════════════════════════════════════════
espaco()
linha("═", 54, ROXO)
print(ROXO + "  🏁  FIM DO JOGO" + RESET)
linha("═", 54, ROXO)
print(BRANCO + f"  Fase 1: {pontos}/6 pontos" + RESET)
print(BRANCO + f"  Fase 2: {pontos2}/12 pontos  (tabela + classificação)" + RESET)
linha("─", 54, CINZA)

total  = pontos + pontos2
maximo = 18

if vidas2 == 0:
    digitar(VERMELHO + f"\n  💀 Game Over, {nome}! Sem vidas na Fase 2." + RESET)
elif total >= 15:
    digitar(VERDE + f"\n  🏆 INCRÍVEL, {nome}! Você domina lógica proposicional!" + RESET)
elif total >= 10:
    digitar(AMARELO + f"\n  👏 Bom trabalho, {nome}! Continue estudando!" + RESET)
else:
    digitar(VERMELHO + f"\n  😬 Pontuação baixa, {nome}. Revise o conteúdo e tente de novo!" + RESET)

espaco()
print(CINZA + f"  Pontuação total: {total}/{maximo}" + RESET)
linha("═", 54, ROXO)
print(CINZA + "  Obrigado por jogar! 🎮" + RESET)
linha("═", 54, ROXO)
espaco()