import random
import time
from colorama import init, Fore, Style

init(autoreset=True)

# ── CORES ──────────────────────────────────────────────
AZUL     = Fore.CYAN + Style.BRIGHT
VERDE    = Fore.GREEN + Style.BRIGHT
VERMELHO = Fore.RED + Style.BRIGHT
AMARELO  = Fore.YELLOW + Style.BRIGHT
ROXO     = Fore.MAGENTA + Style.BRIGHT
BRANCO   = Fore.WHITE + Style.BRIGHT
CINZA    = Fore.WHITE + Style.DIM
RESET    = Style.RESET_ALL


def digitar(texto, delay=0.03):
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def linha(char="─", n=58, cor=AZUL):
    print(cor + char * n + RESET)


def espaco():
    print()


def pedir_vf(prompt):
    while True:
        r = input(prompt).strip().upper()
        if r in ("V", "F"):
            return r
        print(VERMELHO + "  ⚠  Digite apenas V ou F." + RESET)


def colorir_vf(letra):
    return (VERDE + "V" + RESET) if letra == "V" else (VERMELHO + "F" + RESET)


# ══════════════════════════════════════════════════════
#  ABERTURA
# ══════════════════════════════════════════════════════
espaco()
linha("═", 58, ROXO)
print(ROXO + "  ██╗      ██████╗  ██████╗ ██╗ ██████╗  █████╗ " + RESET)
print(ROXO + "  ██║     ██╔═══██╗██╔════╝ ██║██╔════╝ ██╔══██╗" + RESET)
print(ROXO + "  ██║     ██║   ██║██║  ███╗██║██║      ███████║" + RESET)
print(ROXO + "  ██║     ██║   ██║██║   ██║██║██║      ██╔══██║" + RESET)
print(ROXO + "  ███████╗╚██████╔╝╚██████╔╝██║╚██████╗ ██║  ██║" + RESET)
print(ROXO + "  ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝ ╚═╝  ╚═╝" + RESET)
linha("═", 58, ROXO)
print(AZUL + "        🧠  JOGO DA TABELA VERDADE  🧠" + RESET)
linha("═", 58, ROXO)
espaco()

print(CINZA + "  Conectivos:" + RESET)
print(CINZA + "  ¬p       — negação      (inverte o valor)" + RESET)
print(CINZA + "  p ∧ q    — conjunção E  (V só se os dois V)" + RESET)
print(CINZA + "  p ∨ q    — disjunção OU (F só se os dois F)" + RESET)
print(CINZA + "  p → q    — condicional  (F só em V→F)" + RESET)
print(CINZA + "  p ↔ q    — bicondicional (V quando valores iguais)" + RESET)
espaco()

time.sleep(0.4)
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


# ══════════════════════════════════════════════════════
#  FASE 1 — V ou F?  (inclui bicondicional ↔)
# ══════════════════════════════════════════════════════
espaco()
linha("═", 58, AZUL)
print(AZUL + "  🔵  FASE 1 — Verdadeiro ou Falso?" + RESET)
linha("═", 58, AZUL)
print(CINZA + "  Avalie a expressão e responda V ou F." + RESET)
espaco()

DICAS = {
    "neg": "¬p inverte: V vira F, F vira V.",
    "and": "∧ (E): só V quando os dois são V.",
    "or":  "∨ (OU): só F quando os dois são F.",
    "imp": "→ (SE...ENTÃO): só F em V → F.",
    "bic": "↔ (SE E SOMENTE SE): V quando os dois têm o mesmo valor.",
}

TIPOS_F1 = [
    ("neg",  lambda p, q: not p,          lambda p, q: f"¬{_l(p)}"),
    ("neg2", lambda p, q: not q,          lambda p, q: f"¬{_l(q)}"),
    ("and",  lambda p, q: p and q,        lambda p, q: f"{_l(p)} ∧ {_l(q)}"),
    ("or",   lambda p, q: p or q,         lambda p, q: f"{_l(p)} ∨ {_l(q)}"),
    ("imp",  lambda p, q: (not p) or q,   lambda p, q: f"{_l(p)} → {_l(q)}"),
    ("bic",  lambda p, q: p == q,         lambda p, q: f"{_l(p)} ↔ {_l(q)}"),
    ("nand", lambda p, q: not (p and q),  lambda p, q: f"¬({_l(p)} ∧ {_l(q)})"),
    ("nor",  lambda p, q: not (p or q),   lambda p, q: f"¬({_l(p)} ∨ {_l(q)})"),
]

DICA_TIPO = {
    "neg": "neg", "neg2": "neg",
    "and": "and", "nand": "and",
    "or": "or",   "nor": "or",
    "imp": "imp", "bic": "bic",
}


def _l(b):
    return "V" if b else "F"


pontos = 0
vidas = 6
usados = []

pool = random.sample(TIPOS_F1, len(TIPOS_F1))

for i in range(6):
    if vidas == 0:
        break

    t = pool[i % len(pool)]
    tipo_nome, fn, texto_fn = t
    p = random.choice([True, False])
    q = random.choice([True, False])
    pergunta = texto_fn(p, q)
    resposta = fn(p, q)

    coracoes = "❤️ " * vidas + "🖤 " * (6 - vidas)
    espaco()
    linha("─", 58, CINZA)
    print(AMARELO + f"  Pergunta {i+1}/6" + RESET + "  " + coracoes + AMARELO + f"  🏆 {pontos} pts" + RESET)
    linha("─", 58, CINZA)
    espaco()
    print(BRANCO + f"       {pergunta}" + RESET)
    espaco()

    resp_jogador = pedir_vf(AMARELO + "  ➤ Sua resposta (V/F): " + RESET)

    espaco()
    correto_str = "V" if resposta else "F"
    if resp_jogador == correto_str:
        print(VERDE + "  ╔══════════════════════╗")
        print(VERDE + "  ║   ✅  ACERTOU!  +1   ║")
        print(VERDE + "  ╚══════════════════════╝" + RESET)
        pontos += 1
    else:
        print(VERMELHO + "  ╔══════════════════════════════╗")
        print(VERMELHO + f"  ║  ❌  ERROU! Correto: {correto_str}      ║")
        print(VERMELHO + "  ╚══════════════════════════════╝" + RESET)
        dica_chave = DICA_TIPO.get(tipo_nome)
        if dica_chave:
            print(CINZA + f"  💡 Dica: {DICAS[dica_chave]}" + RESET)
        vidas -= 1

    time.sleep(0.5)

espaco()
linha("═", 58, AZUL)
print(AZUL + "  🔵  RESULTADO — FASE 1" + RESET)
linha("═", 58, AZUL)
print(BRANCO + f"  Pontos: {pontos}/6   Vidas restantes: {vidas}" + RESET)
linha("═", 58, AZUL)
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


# ══════════════════════════════════════════════════════
#  FASE 2 — MONTE A TABELA VERDADE
# ══════════════════════════════════════════════════════
espaco()
linha("═", 58, ROXO)
print(ROXO + "  🟣  FASE 2 — Monte a Tabela Verdade!" + RESET)
linha("═", 58, ROXO)
espaco()
digitar(BRANCO + "  Para cada combinação mostrada, calcule o resultado" + RESET, delay=0.02)
digitar(BRANCO + "  da fórmula e responda V ou F." + RESET, delay=0.02)
digitar(BRANCO + "  Depois classifique a fórmula inteira." + RESET, delay=0.02)
espaco()
print(VERDE    + "  🟢 T = TAUTOLOGIA    → sempre Verdadeira" + RESET)
print(VERMELHO + "  🔴 C = CONTRADIÇÃO   → sempre Falsa" + RESET)
print(AMARELO  + "  🟡 G = CONTINGÊNCIA  → mistura de V e F" + RESET)
espaco()

# ── POOL DE FÓRMULAS ──────────────────────────────────
#    Inclui bicondicional e fórmulas com 3 variáveis
FORMULAS = [
    # ── Tautologias ──────────────────────────────────
    ("P ∨ ¬P",       lambda p, q, r: p or not p,          "Tautologia",  "neg"),
    ("¬P ∨ P",       lambda p, q, r: not p or p,          "Tautologia",  "neg"),
    ("P → P",        lambda p, q, r: (not p) or p,        "Tautologia",  "imp"),
    ("(P∧Q) → P",    lambda p, q, r: not (p and q) or p,  "Tautologia",  "imp"),
    ("P ↔ P",        lambda p, q, r: True,                "Tautologia",  "bic"),

    # ── Contradições ─────────────────────────────────
    ("P ∧ ¬P",       lambda p, q, r: p and not p,         "Contradição", "neg"),
    ("¬P ∧ P",       lambda p, q, r: not p and p,         "Contradição", "neg"),
    ("¬(P ∨ ¬P)",    lambda p, q, r: not (p or not p),    "Contradição", "neg"),
    ("(P→Q)∧¬(P→Q)", lambda p, q, r: False,               "Contradição", "imp"),

    # ── Contingências (2 variáveis) ───────────────────
    ("P ∧ Q",        lambda p, q, r: p and q,             "Contingência","and"),
    ("P ∨ Q",        lambda p, q, r: p or q,              "Contingência","or"),
    ("P → Q",        lambda p, q, r: (not p) or q,        "Contingência","imp"),
    ("P ↔ Q",        lambda p, q, r: p == q,              "Contingência","bic"),
    ("¬P ∧ Q",       lambda p, q, r: not p and q,         "Contingência","and"),
    ("¬P ∨ ¬Q",      lambda p, q, r: not p or not q,      "Contingência","or"),
    ("¬(P ↔ Q)",     lambda p, q, r: not (p == q),        "Contingência","bic"),

    # ── Contingências (3 variáveis — 8 linhas) ────────
    ("P ∧ (Q ∨ R)",  lambda p, q, r: p and (q or r),      "Contingência","and"),
    ("(P → Q) ∧ R",  lambda p, q, r: ((not p) or q) and r,"Contingência","imp"),
    ("P ∨ (Q ∧ R)",  lambda p, q, r: p or (q and r),      "Contingência","or"),
]

def tem_3_vars(nome_formula):
    return "R" in nome_formula

# Garante ao menos 1 de cada categoria
por_cat = {c: [f for f in FORMULAS if f[2] == c] for c in ["Tautologia", "Contradição", "Contingência"]}
for v in por_cat.values():
    random.shuffle(v)

selecionadas = [por_cat[c].pop() for c in ["Tautologia", "Contradição", "Contingência"]]
restantes = [f for f in FORMULAS if f not in selecionadas]
random.shuffle(restantes)
selecionadas += restantes[:3]
random.shuffle(selecionadas)

COMBOS2 = [(True, True), (True, False), (False, True), (False, False)]
COMBOS3 = [
    (True,  True,  True),  (True,  True,  False),
    (True,  False, True),  (True,  False, False),
    (False, True,  True),  (False, True,  False),
    (False, False, True),  (False, False, False),
]

pontos2 = 0
vidas2  = 5

for i, (nome_formula, fn, classificacao, dica_chave) in enumerate(selecionadas):
    if vidas2 == 0:
        break

    usar3 = tem_3_vars(nome_formula)
    combos = COMBOS3 if usar3 else COMBOS2

    coracoes2 = "❤️ " * vidas2 + "🖤 " * (5 - vidas2)
    espaco()
    linha("─", 58, CINZA)
    print(AMARELO + f"  Fórmula {i+1}/6" + RESET + "  " + coracoes2 + AMARELO + f"  🏆 {pontos2} pts" + RESET)
    linha("─", 58, CINZA)
    espaco()
    print(ROXO + f"  Fórmula:  {nome_formula}" + RESET)
    n_vars = "3 variáveis — 8 linhas" if usar3 else "2 variáveis — 4 linhas"
    print(CINZA + f"  ({n_vars})" + RESET)
    espaco()
    print(CINZA + "  Preencha o resultado de cada linha (V ou F):" + RESET)
    espaco()

    # ── Cabeçalho da tabela ───────────────────────────
    if usar3:
        print(CINZA + "  ┌─────┬─────┬─────┬──────────────────────┐")
        print(CINZA + "  │  P  │  Q  │  R  │  Resultado           │")
        print(CINZA + "  ├─────┼─────┼─────┼──────────────────────┤" + RESET)
    else:
        print(CINZA + "  ┌─────┬─────┬──────────────────────┐")
        print(CINZA + "  │  P  │  Q  │  Resultado           │")
        print(CINZA + "  ├─────┼─────┼──────────────────────┤" + RESET)

    respostas_jogador  = []
    respostas_corretas = []

    for combo in combos:
        p, q = combo[0], combo[1]
        r = combo[2] if usar3 else None
        correto_bool = fn(p, q, r) if usar3 else fn(p, q, None)
        correto_str  = "V" if correto_bool else "F"
        respostas_corretas.append(correto_str)

        pv = colorir_vf(_l(p))
        qv = colorir_vf(_l(q))

        if usar3:
            rv = colorir_vf(_l(r))
            print(f"  {CINZA}│{RESET}  {pv}  {CINZA}│{RESET}  {qv}  {CINZA}│{RESET}  {rv}  {CINZA}│{RESET}  ", end="")
        else:
            print(f"  {CINZA}│{RESET}  {pv}  {CINZA}│{RESET}  {qv}  {CINZA}│{RESET}  ", end="")

        resp = pedir_vf(AMARELO + "? " + RESET)
        respostas_jogador.append(resp)

    if usar3:
        print(CINZA + "  └─────┴─────┴─────┴──────────────────────┘" + RESET)
    else:
        print(CINZA + "  └─────┴─────┴──────────────────────┘" + RESET)
    espaco()

    acertos_tab = sum(r == c for r, c in zip(respostas_jogador, respostas_corretas))
    total_linhas = len(combos)

    # ── Gabarito ──────────────────────────────────────
    print(CINZA + "  ── Gabarito ─────────────────────────────────────────" + RESET)
    if usar3:
        print(CINZA + "  ┌─────┬─────┬─────┬──────────┬──────────┐")
        print(CINZA + "  │  P  │  Q  │  R  │  Você    │ Correto  │")
        print(CINZA + "  ├─────┼─────┼─────┼──────────┼──────────┤" + RESET)
    else:
        print(CINZA + "  ┌─────┬─────┬──────────┬──────────┐")
        print(CINZA + "  │  P  │  Q  │  Você    │ Correto  │")
        print(CINZA + "  ├─────┼─────┼──────────┼──────────┤" + RESET)

    for j, combo in enumerate(combos):
        p, q = combo[0], combo[1]
        r = combo[2] if usar3 else None
        pv  = colorir_vf(_l(p))
        qv  = colorir_vf(_l(q))
        rj  = respostas_jogador[j]
        rc  = respostas_corretas[j]
        rjv = colorir_vf(rj)
        rcv = colorir_vf(rc)
        icone = VERDE + "✔" + RESET if rj == rc else VERMELHO + "✘" + RESET
        if usar3:
            rv = colorir_vf(_l(r))
            print(f"  {CINZA}│{RESET}  {pv}  {CINZA}│{RESET}  {qv}  {CINZA}│{RESET}  {rv}  {CINZA}│{RESET}  {rjv}  {icone}   {CINZA}│{RESET}    {rcv}    {CINZA}│{RESET}")
        else:
            print(f"  {CINZA}│{RESET}  {pv}  {CINZA}│{RESET}  {qv}  {CINZA}│{RESET}  {rjv}  {icone}   {CINZA}│{RESET}    {rcv}    {CINZA}│{RESET}")

    if usar3:
        print(CINZA + "  └─────┴─────┴─────┴──────────┴──────────┘" + RESET)
    else:
        print(CINZA + "  └─────┴─────┴──────────┴──────────┘" + RESET)
    espaco()

    if acertos_tab == total_linhas:
        print(VERDE + f"  ✅ Tabela perfeita! {total_linhas}/{total_linhas} linhas corretas." + RESET)
    else:
        print(AMARELO + f"  ⚠  {acertos_tab}/{total_linhas} linhas corretas na tabela." + RESET)
        print(CINZA + f"  💡 Dica: {DICAS[dica_chave]}" + RESET)

    espaco()

    # ── Classificação ─────────────────────────────────
    print(BRANCO + "  Agora classifique a fórmula:" + RESET)
    print(CINZA  + "  T = Tautologia  |  C = Contradição  |  G = Contingência" + RESET)
    espaco()

    while True:
        classe_resp = input(AMARELO + "  ➤ T, C ou G? " + RESET).strip().upper()
        if classe_resp in ("T", "C", "G"):
            break
        print(VERMELHO + "  ⚠  Digite apenas T, C ou G." + RESET)

    mapa = {"T": "Tautologia", "C": "Contradição", "G": "Contingência"}
    classe_texto = mapa[classe_resp]
    espaco()

    ganhou_tab   = acertos_tab == total_linhas
    ganhou_class = classe_texto == classificacao
    pontos2 += int(ganhou_tab) + int(ganhou_class)

    if ganhou_tab and ganhou_class:
        print(VERDE + "  ╔══════════════════════════════════════════════╗")
        print(VERDE + "  ║  🏆  PERFEITO! Tabela + Classe corretas +2  ║")
        print(VERDE + "  ╚══════════════════════════════════════════════╝" + RESET)
    elif ganhou_tab and not ganhou_class:
        print(AMARELO + "  ╔══════════════════════════════════════════════╗")
        print(AMARELO + "  ║  ✅ Tabela certa  ❌ Classe errada       +1  ║")
        print(AMARELO + f"  ║  Correto: {classificacao:<34}║")
        print(AMARELO + "  ╚══════════════════════════════════════════════╝" + RESET)
        vidas2 -= 1
    elif not ganhou_tab and ganhou_class:
        print(AMARELO + "  ╔══════════════════════════════════════════════╗")
        print(AMARELO + "  ║  ❌ Tabela errada  ✅ Classe certa       +1  ║")
        print(AMARELO + "  ╚══════════════════════════════════════════════╝" + RESET)
        vidas2 -= 1
    else:
        print(VERMELHO + "  ╔══════════════════════════════════════════════╗")
        print(VERMELHO + "  ║  ❌ Tabela errada  ❌ Classe errada      +0  ║")
        print(VERMELHO + f"  ║  Classe correta: {classificacao:<26}║")
        print(VERMELHO + "  ╚══════════════════════════════════════════════╝" + RESET)
        vidas2 -= 1

    time.sleep(0.6)


# ══════════════════════════════════════════════════════
#  TELA FINAL
# ══════════════════════════════════════════════════════
espaco()
linha("═", 58, ROXO)
print(ROXO + "  🏁  FIM DO JOGO" + RESET)
linha("═", 58, ROXO)
print(BRANCO + f"  Fase 1: {pontos}/6 pontos" + RESET)
print(BRANCO + f"  Fase 2: {pontos2}/12 pontos  (tabela + classificação)" + RESET)
linha("─", 58, CINZA)

total  = pontos + pontos2
maximo = 18

if vidas2 == 0:
    digitar(VERMELHO + f"\n  💀 Game Over, {nome}! Sem vidas na Fase 2." + RESET)
elif total >= 15:
    digitar(VERDE + f"\n  🏆 INCRÍVEL, {nome}! Você domina lógica proposicional!" + RESET)
elif total >= 10:
    digitar(AMARELO + f"\n  👏 Bom trabalho, {nome}! Continue estudando!" + RESET)
else:
    digitar(VERMELHO + f"\n  😬 Pontuação baixa, {nome}. Revise as conectivas e tente de novo!" + RESET)

espaco()
print(CINZA + f"  Pontuação total: {total}/{maximo}" + RESET)
linha("═", 58, ROXO)
print(CINZA + "  Obrigado por jogar! 🎮" + RESET)
linha("═", 58, ROXO)
espaco()