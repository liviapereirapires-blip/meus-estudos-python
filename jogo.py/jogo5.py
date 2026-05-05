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