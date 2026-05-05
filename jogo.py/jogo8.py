# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║        LÓGICA — O DESPERTAR DA RAZÃO  v2.0           ║
║   Jogo de Tabela Verdade | Lógica Proposicional      ║
╚══════════════════════════════════════════════════════╝
"""

import random
import time
import sys
import os
from colorama import init, Fore, Style

init(autoreset=True)

# ══════════════════════════════════════════════════
#  PALETA DE CORES
# ══════════════════════════════════════════════════
R  = Style.RESET_ALL
B  = Style.BRIGHT
D  = Style.DIM

ROXO   = Fore.MAGENTA  + B
AZUL   = Fore.CYAN     + B
VERDE  = Fore.GREEN    + B
VERM   = Fore.RED      + B
AMAR   = Fore.YELLOW   + B
BRAN   = Fore.WHITE    + B
CINZA  = Fore.WHITE    + D
GOLD   = Fore.YELLOW   + B
CYAN   = Fore.CYAN


# ══════════════════════════════════════════════════
#  UTILITÁRIOS
# ══════════════════════════════════════════════════
def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def digitar(texto, delay=0.025):
    """Imprime texto com efeito de digitação."""
    for ch in texto:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def linha(char="─", n=60, cor=AZUL):
    print(cor + char * n + R)

def espaco(n=1):
    print("\n" * (n - 1))

def cabecalho(titulo, subtitulo="", cor=ROXO):
    espaco()
    linha("═", 60, cor)
    print(cor + f"  {titulo}".center(60) + R)
    if subtitulo:
        print(CINZA + f"  {subtitulo}".center(60) + R)
    linha("═", 60, cor)
    espaco()

def pausar(seg=0.6):
    time.sleep(seg)

def pedir_vf(prompt="  ➤ Sua resposta (V/F): "):
    while True:
        r = input(AMAR + prompt + R).strip().upper()
        if r in ("V", "F"):
            return r
        print(VERM + "  ⚠  Digite apenas V ou F." + R)

def pedir_tcg(prompt="  ➤ T, C ou G? "):
    while True:
        r = input(AMAR + prompt + R).strip().upper()
        if r in ("T", "C", "G"):
            return r
        print(VERM + "  ⚠  Digite apenas T, C ou G." + R)

def pedir_sim_nao(prompt):
    while True:
        r = input(AMAR + prompt + R).strip().lower()
        if r in ("sim", "s", "não", "nao", "n"):
            return r in ("sim", "s")
        print(VERM + "  ⚠  Digite sim ou não." + R)

def colorir_vf(v):
    return (VERDE + "V" + R) if v == "V" else (VERM + "F" + R)

def barra_progresso(atual, total, largura=30, cor=ROXO):
    preenchido = int(largura * atual / total)
    barra = "█" * preenchido + "░" * (largura - preenchido)
    pct = int(atual / total * 100)
    print(cor + f"  [{barra}] {pct}%" + R)

def coracoes(vidas, maximo):
    return "❤️ " * vidas + "🖤 " * (maximo - vidas)

def banner_ascii():
    print(ROXO + """
  ██╗      ██████╗  ██████╗ ██╗ ██████╗  █████╗
  ██║     ██╔═══██╗██╔════╝ ██║██╔════╝ ██╔══██╗
  ██║     ██║   ██║██║  ███╗██║██║      ███████║
  ██║     ██║   ██║██║   ██║██║██║      ██╔══██║
  ███████╗╚██████╔╝╚██████╔╝██║╚██████╗ ██║  ██║
  ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝ ╚═╝  ╚═╝""" + R)
    print(GOLD + "        ✦  O  D E S P E R T A R  D A  R A Z Ã O  ✦" + R)


# ══════════════════════════════════════════════════
#  BANCO DE QUESTÕES
# ══════════════════════════════════════════════════
FASE1_POOL = [
    ("¬V",              False),
    ("¬F",              True),
    ("V ∧ V",           True),
    ("V ∧ F",           False),
    ("F ∧ V",           False),
    ("F ∧ F",           False),
    ("V ∨ V",           True),
    ("V ∨ F",           True),
    ("F ∨ F",           False),
    ("F ∨ V",           True),
    ("V → V",           True),
    ("V → F",           False),
    ("F → V",           True),
    ("F → F",           True),
    ("V ∧ (F ∨ V)",     True),
    ("F ∨ (V ∧ F)",     False),
    ("¬(V ∧ F)",        True),
    ("¬(V ∨ F)",        False),
    ("V → (F → V)",     True),
    ("(V ∧ V) → F",     False),
    ("¬(F → F)",        False),
    ("(F ∨ V) → F",     False),
    ("V ↔ V",           True),
    ("V ↔ F",           False),
]

FASE2_POOL = [
    # Tautologias
    ("P ∨ ¬P",              lambda p, q: p or not p,                        "Tautologia"),
    ("¬P ∨ P",              lambda p, q: not p or p,                        "Tautologia"),
    ("P → P",               lambda p, q: not p or p,                        "Tautologia"),
    ("(P ∧ Q) → P",         lambda p, q: not (p and q) or p,                "Tautologia"),
    ("P → (Q → P)",         lambda p, q: not p or (not q or p),             "Tautologia"),
    ("¬(P ∧ ¬P)",           lambda p, q: not (p and not p),                  "Tautologia"),
    # Contradições
    ("P ∧ ¬P",              lambda p, q: p and not p,                        "Contradição"),
    ("¬P ∧ P",              lambda p, q: not p and p,                        "Contradição"),
    ("¬(P ∨ ¬P)",           lambda p, q: not (p or not p),                   "Contradição"),
    ("P ∧ (¬P ∧ Q)",        lambda p, q: p and (not p and q),                "Contradição"),
    ("(P → Q) ∧ (P ∧ ¬Q)", lambda p, q: ((not p or q) and (p and not q)),   "Contradição"),
    ("(P ∨ Q) ∧ ¬(P ∨ Q)", lambda p, q: (p or q) and not (p or q),          "Contradição"),
    # Contingências
    ("P ∧ Q",               lambda p, q: p and q,                            "Contingência"),
    ("P ∨ Q",               lambda p, q: p or q,                             "Contingência"),
    ("P → Q",               lambda p, q: not p or q,                         "Contingência"),
    ("¬(P ∧ Q)",            lambda p, q: not (p and q),                      "Contingência"),
    ("¬(P ∨ Q)",            lambda p, q: not (p or q),                       "Contingência"),
    ("P ↔ Q",               lambda p, q: p == q,                             "Contingência"),
]

COMBOS = [(True, True), (True, False), (False, True), (False, False)]
LABEL  = {True: "V", False: "F"}
CAT_MAP = {"T": "Tautologia", "C": "Contradição", "G": "Contingência"}
CAT_COR = {"Tautologia": VERDE, "Contradição": VERM, "Contingência": AMAR}
CAT_ICO = {"Tautologia": "🟢", "Contradição": "🔴", "Contingência": "🟡"}


def montar_fase2():
    """Garante ao menos 1 de cada categoria nas 6 questões."""
    cats = ["Tautologia", "Contradição", "Contingência"]
    por_cat = {c: [f for f in FASE2_POOL if f[2] == c] for c in cats}
    for v in por_cat.values():
        random.shuffle(v)
    sel = [por_cat[c].pop() for c in cats]
    resto = [f for f in FASE2_POOL if f not in sel]
    random.shuffle(resto)
    sel += resto[:3]
    random.shuffle(sel)
    return sel


# ══════════════════════════════════════════════════
#  TELA DE ABERTURA
# ══════════════════════════════════════════════════
def tela_abertura():
    limpar()
    linha("═", 60, ROXO)
    banner_ascii()
    linha("═", 60, ROXO)
    espaco()

    pausar(0.4)
    digitar(BRAN + "  No ano de 3047, a humanidade descobriu que o universo" + R, 0.02)
    digitar(BRAN + "  é governado por uma força suprema: a Lógica Pura." + R, 0.02)
    espaco()
    digitar(CYAN + "  A Ordem dos Arquitetos mantém o equilíbrio dos mundos" + R, 0.02)
    digitar(CYAN + "  através de Tabelas Sagradas — fórmulas que definem o" + R, 0.02)
    digitar(CYAN + "  que é real e o que é ilusão." + R, 0.02)
    espaco()
    digitar(AMAR + "  Uma ruptura foi detectada. Um agente renegado corrompeu" + R, 0.02)
    digitar(AMAR + "  os registros da Ordem." + R, 0.02)
    espaco()
    digitar(GOLD + "  Apenas um Arquiteto treinado pode restaurar a verdade." + R, 0.025)
    digitar(GOLD + "  Esse Arquiteto… é você." + R, 0.025)
    espaco()
    linha("─", 60, CINZA)


# ══════════════════════════════════════════════════
#  FASE 1
# ══════════════════════════════════════════════════
def fase1(nome):
    limpar()
    cabecalho("⚡  FASE 1 — Julgamento do Oráculo", "Fase 01 de 02", AZUL)

    digitar(CINZA + "  O Oráculo lança proposições diante de você." + R, 0.02)
    digitar(CINZA + "  Julgue cada expressão: V (Verdadeiro) ou F (Falso)." + R, 0.02)
    digitar(CINZA + "  Seis questões. Mínimo de 4 acertos para avançar." + R, 0.02)
    espaco()
    input(CINZA + "  [ Pressione ENTER para começar ] " + R)

    pool = random.sample(FASE1_POOL, 6)
    pontos = 0
    vidas  = 6

    for i, (expr, gabarito) in enumerate(pool):
        if vidas == 0:
            break

        limpar()
        cabecalho("⚡  FASE 1 — Julgamento do Oráculo", "Fase 01 de 02", AZUL)

        # HUD
        print(f"  {AZUL}Questão {i+1}/6{R}  {coracoes(vidas, 6)}  {GOLD}⚡ {pontos} pts{R}")
        barra_progresso(i, 6, cor=AZUL)
        espaco()

        # Fórmula
        linha("─", 60, CINZA)
        print(BRAN + f"\n     Expressão:  {GOLD}{expr}{R}\n")
        linha("─", 60, CINZA)
        espaco()

        resp = pedir_vf()
        correto_str = "V" if gabarito else "F"
        espaco()

        if resp == correto_str:
            pontos += 1
            print(VERDE + "  ╔══════════════════════════╗")
            print(VERDE + "  ║   ✅  CORRETO!   +1 pt   ║")
            print(VERDE + "  ╚══════════════════════════╝" + R)
            digitar(CINZA + f"\n  A expressão é {colorir_vf(correto_str)}.", 0.02)
        else:
            vidas -= 1
            print(VERM + "  ╔══════════════════════════════════╗")
            print(VERM + f"  ║  ❌  ERROU!  Correto: {correto_str}          ║")
            print(VERM + "  ╚══════════════════════════════════╝" + R)
            if vidas == 0:
                digitar(VERM + "\n  💀 Sem vidas! Missão comprometida.", 0.02)

        pausar(1.2)

    # Resultado fase 1
    limpar()
    cabecalho("📊  RESULTADO — FASE 1", "", AZUL)
    print(BRAN + f"  Pontos: {pontos}/6   Vidas restantes: {vidas}" + R)
    barra_progresso(pontos, 6, cor=AZUL)
    espaco()

    if vidas == 0 or pontos < 4:
        digitar(VERM + f"  💀 Game Over, {nome}! Pontuação insuficiente para avançar." + R)
        digitar(CINZA + "\n  A Ordem dos Arquitetos chora sua derrota." + R, 0.02)
        digitar(CINZA + "  Os mundos caem no caos lógico. Estude e retorne." + R, 0.02)
        espaco()
        return pontos, False

    digitar(VERDE + f"  🎉 Excelente, {nome}! Você provou seu valor ao Oráculo!" + R)
    espaco()
    pausar(0.8)
    return pontos, True


# ══════════════════════════════════════════════════
#  ENTRE FASES — NARRAÇÃO
# ══════════════════════════════════════════════════
def narracao_entre_fases(nome, pts1):
    limpar()
    linha("═", 60, ROXO)
    print(ROXO + "  ◈  TRANSMISSÃO DA ORDEM DOS ARQUITETOS  ◈".center(60) + R)
    linha("═", 60, ROXO)
    espaco()

    digitar(GOLD  + f"  Impressionante, {nome}.", 0.03)
    espaco()
    digitar(BRAN  + "  Você provou que pode ler as proposições elementares.", 0.02)
    digitar(BRAN  + "  Mas o verdadeiro desafio aguarda.", 0.02)
    espaco()
    digitar(CYAN  + "  A Fase 2 exige que você construa as Tabelas Sagradas", 0.02)
    digitar(CYAN  + "  do zero — e classifique a natureza de cada fórmula.", 0.02)
    espaco()

    print(VERDE  + "  🟢  T = TAUTOLOGIA   → sempre Verdadeira" + R)
    print(VERM   + "  🔴  C = CONTRADIÇÃO  → sempre Falsa" + R)
    print(AMAR   + "  🟡  G = CONTINGÊNCIA → mistura de V e F" + R)
    espaco()

    digitar(GOLD  + "  O destino dos mundos está em suas mãos.", 0.03)
    espaco()
    print(CINZA  + f"  Pontuação atual: {pts1}/6 pts  — máximo possível: 18 pts" + R)
    espaco()
    input(CINZA + "  [ Pressione ENTER para a Fase 2 ] " + R)


# ══════════════════════════════════════════════════
#  FASE 2
# ══════════════════════════════════════════════════
def fase2(nome):
    limpar()
    cabecalho("⚔️  FASE 2 — As Tabelas Sagradas", "Fase 02 de 02", ROXO)

    digitar(CINZA + "  Para cada fórmula, preencha a tabela verdade (V ou F)" + R, 0.02)
    digitar(CINZA + "  e classifique a fórmula: T, C ou G." + R, 0.02)
    digitar(CINZA + "  Tabela correta = +1 pt  |  Classificação correta = +1 pt" + R, 0.02)
    espaco()
    input(CINZA + "  [ Pressione ENTER para começar ] " + R)

    formulas = montar_fase2()
    pontos = 0
    vidas  = 5

    for i, (nome_f, fn, cat) in enumerate(formulas):
        if vidas == 0:
            break

        limpar()
        cabecalho("⚔️  FASE 2 — As Tabelas Sagradas", "Fase 02 de 02", ROXO)

        # HUD
        print(f"  {ROXO}Fórmula {i+1}/6{R}  {coracoes(vidas, 5)}  {GOLD}⚡ {pontos} pts{R}")
        barra_progresso(i, 6, cor=ROXO)
        espaco()

        # Fórmula
        linha("─", 60, CINZA)
        print(BRAN + f"\n  Fórmula Sagrada:  {GOLD}{nome_f}{R}\n")
        linha("─", 60, CINZA)
        espaco()

        print(CINZA + "  Preencha o resultado para cada combinação de P e Q:" + R)
        espaco()

        # Cabeçalho da tabela
        print(CINZA + "  ┌──────┬──────┬──────────────────────────┐")
        print(CINZA + "  │  P   │  Q   │  Resultado               │")
        print(CINZA + "  ├──────┼──────┼──────────────────────────┤" + R)

        respostas_jogador  = []
        respostas_corretas = []

        for p, q in COMBOS:
            correto_bool = fn(p, q)
            correto_str  = "V" if correto_bool else "F"
            respostas_corretas.append(correto_str)

            pv = colorir_vf(LABEL[p])
            qv = colorir_vf(LABEL[q])

            print(f"  {CINZA}│{R}  {pv}   {CINZA}│{R}  {qv}   {CINZA}│{R}  ", end="")
            resp = pedir_vf("? ")
            respostas_jogador.append(resp)

        print(CINZA + "  └──────┴──────┴──────────────────────────┘" + R)
        espaco()

        # Gabarito
        acertos_tabela = sum(r == c for r, c in zip(respostas_jogador, respostas_corretas))

        print(CINZA + "  ── Gabarito ─────────────────────────────────────────" + R)
        print(CINZA + "  ┌──────┬──────┬──────────┬──────────┬────────┐")
        print(CINZA + "  │  P   │  Q   │  Você    │ Correto  │ Status │")
        print(CINZA + "  ├──────┼──────┼──────────┼──────────┼────────┤" + R)

        for (p, q), rj, rc in zip(COMBOS, respostas_jogador, respostas_corretas):
            pv   = colorir_vf(LABEL[p])
            qv   = colorir_vf(LABEL[q])
            rjv  = colorir_vf(rj)
            rcv  = colorir_vf(rc)
            icone = VERDE + "  ✔  " + R if rj == rc else VERM + "  ✘  " + R
            print(f"  {CINZA}│{R}  {pv}   {CINZA}│{R}  {qv}   {CINZA}│{R}   {rjv}    {CINZA}│{R}    {rcv}    {CINZA}│{R} {icone}{CINZA}│{R}")

        print(CINZA + "  └──────┴──────┴──────────┴──────────┴────────┘" + R)
        espaco()

        if acertos_tabela == 4:
            print(VERDE + f"  ✅  Tabela perfeita! 4/4 linhas corretas." + R)
        else:
            print(AMAR  + f"  ⚠   {acertos_tabela}/4 linhas corretas na tabela." + R)
        espaco()

        # Classificação
        linha("─", 60, CINZA)
        print(BRAN + "  Classifique a fórmula:" + R)
        print(VERDE + "  T = Tautologia" + R + "  │  " +
              VERM  + "C = Contradição"  + R + "  │  " +
              AMAR  + "G = Contingência" + R)
        espaco()

        classe_resp  = pedir_tcg()
        classe_texto = CAT_MAP[classe_resp]
        espaco()

        # Pontuação
        ganhou_tabela = (acertos_tabela == 4)
        ganhou_classe = (classe_texto == cat)
        ganho = int(ganhou_tabela) + int(ganhou_classe)
        pontos += ganho

        cat_cor = CAT_COR[cat]
        cat_ico = CAT_ICO[cat]

        if ganhou_tabela and ganhou_classe:
            print(VERDE + "  ╔══════════════════════════════════════════════╗")
            print(VERDE + f"  ║  🏆  PERFEITO! Tabela + Classe correta  +2  ║")
            print(VERDE + f"  ║  {cat_ico} A fórmula é {cat:<28}║")
            print(VERDE + "  ╚══════════════════════════════════════════════╝" + R)
        elif ganhou_tabela and not ganhou_classe:
            print(AMAR  + "  ╔══════════════════════════════════════════════╗")
            print(AMAR  + "  ║  ✅ Tabela certa   ❌ Classe errada     +1   ║")
            print(AMAR  + f"  ║  {cat_ico} Correto: {cat:<33}║")
            print(AMAR  + "  ╚══════════════════════════════════════════════╝" + R)
            vidas -= 1
        elif not ganhou_tabela and ganhou_classe:
            print(AMAR  + "  ╔══════════════════════════════════════════════╗")
            print(AMAR  + "  ║  ❌ Tabela errada  ✅ Classe certa      +1   ║")
            print(AMAR  + "  ╚══════════════════════════════════════════════╝" + R)
            vidas -= 1
        else:
            print(VERM  + "  ╔══════════════════════════════════════════════╗")
            print(VERM  + "  ║  ❌ Tabela errada  ❌ Classe errada     +0   ║")
            print(VERM  + f"  ║  {cat_ico} Correto: {cat:<33}║")
            print(VERM  + "  ╚══════════════════════════════════════════════╝" + R)
            vidas -= 1

        if vidas == 0:
            digitar(VERM + "\n  💀 Sem vidas! A missão foi comprometida.", 0.02)

        pausar(1.2)
        if i < 5 and vidas > 0:
            input(CINZA + "\n  [ ENTER → próxima fórmula ] " + R)

    return pontos, vidas


# ══════════════════════════════════════════════════
#  TELA FINAL
# ══════════════════════════════════════════════════
def tela_final(nome, pts1, pts2, vidas2):
    limpar()
    total  = pts1 + pts2
    maximo = 18
    pct    = int(total / maximo * 100)

    linha("═", 60, ROXO)
    print(ROXO + "  🏁  FIM DA MISSÃO".center(60) + R)
    linha("═", 60, ROXO)
    espaco()

    print(BRAN + f"  Fase 1  ▸  {pts1}/6 pontos" + R)
    print(BRAN + f"  Fase 2  ▸  {pts2}/12 pontos  (tabela + classificação)" + R)
    linha("─", 60, CINZA)
    print(GOLD + f"  TOTAL   ▸  {total}/{maximo} pontos  ({pct}%)" + R)
    espaco()
    barra_progresso(total, maximo, cor=GOLD)
    espaco()

    # Rank e história
    if total >= 16:
        titulo = "⚜  GRÃO-ARQUITETO  ⚜"
        cor    = GOLD
        historia = (
            f"  Você transcendeu a missão, {nome}.\n"
            "  A Ordem ergue seus monumentos em sua honra.\n"
            "  Nenhuma fórmula resiste ao seu julgamento.\n"
            "  Você é a Lógica Pura encarnada."
        )
        desfecho = (
            "  As Tabelas Sagradas brilham novamente.\n"
            "  A corrupção foi completamente erradicada.\n"
            "  A Ordem canta seu nome entre as estrelas. 🌟"
        )
    elif total >= 12:
        titulo = "◈  ARQUITETO MESTRE  ◈"
        cor    = AZUL
        historia = (
            f"  Impressionante, {nome}.\n"
            "  Você domina os fundamentos da lógica proposicional.\n"
            "  Ainda há margem para a perfeição.\n"
            "  Mas os mundos respiram aliviados."
        )
        desfecho = (
            "  A maior parte da corrupção foi neutralizada.\n"
            "  Alguns fragmentos renegados ainda vagam —\n"
            "  mas estão em fuga. A Ordem confia em você. 🛡️"
        )
    elif total >= 7:
        titulo = "▸  ARQUITETO APRENDIZ"
        cor    = CYAN
        historia = (
            f"  Você lutou com coragem, {nome}.\n"
            "  A lógica ainda escorrega entre seus dedos —\n"
            "  mas o potencial está lá.\n"
            "  Estude. Retorne. Evolua."
        )
        desfecho = (
            "  A missão foi parcialmente cumprida.\n"
            "  A Ordem aguarda seu retorno mais forte.\n"
            "  A próxima batalha será sua. 📖"
        )
    else:
        titulo = "☠  INICIANTE CAÓTICO"
        cor    = VERM
        historia = (
            f"  {nome}, a lógica ainda é um mistério para você.\n"
            "  Mas todo Grão-Arquiteto começou do zero.\n"
            "  Revise as tabelas. Tente novamente.\n"
            "  O caos pode ser ordenado."
        )
        desfecho = (
            "  A corrupção avançou desta vez.\n"
            "  Mas cada derrota é um ensinamento.\n"
            "  A Lógica aguarda sua evolução. 🔄"
        )

    linha("─", 60, cor)
    print(cor + f"  {titulo}".center(60) + R)
    linha("─", 60, cor)
    espaco()
    for linha_texto in historia.split("\n"):
        digitar(BRAN + linha_texto + R, 0.015)
    espaco()
    linha("─", 60, CINZA)
    for linha_texto in desfecho.split("\n"):
        digitar(CINZA + linha_texto + R, 0.015)
    espaco()
    linha("═", 60, ROXO)
    print(CINZA + "  Obrigado por jogar! 🎮  |  LÓGICA v2.0" + R)
    linha("═", 60, ROXO)
    espaco()


# ══════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ══════════════════════════════════════════════════
def main():
    while True:
        tela_abertura()
        espaco()
        nome = input(AMAR + "  👤 Qual seu nome, Arquiteto? " + R).strip() or "Arquiteto"
        espaco()

        if not pedir_sim_nao(f"  {nome}, você está preparado(a) para a missão? (sim/não): "):
            espaco()
            digitar(VERM + f"  Tudo bem! Volte quando estiver pronto, {nome}. 📖" + R)
            espaco()
            sys.exit(0)

        espaco()
        digitar(VERDE + f"  Ótimo, {nome}! A Ordem conta com você. 🚀" + R, 0.03)
        pausar(0.8)

        # ── FASE 1 ──
        pts1, passou = fase1(nome)

        if not passou:
            espaco()
            if not pedir_sim_nao("  Deseja tentar novamente? (sim/não): "):
                espaco()
                digitar(CINZA + "  Até a próxima, Arquiteto. 👋" + R)
                espaco()
                break
            continue

        # ── NARRAÇÃO ──
        narracao_entre_fases(nome, pts1)

        # ── FASE 2 ──
        pts2, vidas2 = fase2(nome)

        # ── TELA FINAL ──
        tela_final(nome, pts1, pts2, vidas2)

        espaco()
        if not pedir_sim_nao("  Jogar novamente? (sim/não): "):
            digitar(CINZA + "\n  Até a próxima, Arquiteto. A Ordem aguarda seu retorno. 👋" + R)
            espaco()
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        espaco()
        print(CINZA + "\n  Jogo interrompido. Até logo, Arquiteto! 👋" + R)
        espaco()