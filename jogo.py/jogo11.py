"""

╔══════════════════════════════════════════════════════╗
║        LÓGICA — O DESPERTAR DA RAZÃO  v2.1           ║
║   Jogo de Tabela Verdade | Lógica Proposicional      ║
╚══════════════════════════════════════════════════════╝
"""

import random
import time
import sys
import os
import threading

# ══════════════════════════════════════════════════
#  DEPENDÊNCIAS COM FALLBACK SEGURO
# ══════════════════════════════════════════════════
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    _COLORAMA_OK = True
except ImportError:
    # Fallback sem cores se colorama não estiver instalada
    class _Dummy:
        MAGENTA = ""
        CYAN = ""
        GREEN = ""
        RED = ""
        YELLOW = ""
        WHITE = ""
        RESET_ALL = ""
        BRIGHT = ""
        DIM = ""

    Fore  = _Dummy()
    Style = _Dummy()
    _COLORAMA_OK = False

try:
    import numpy as np
    import pygame
    _AUDIO_OK = True
except ImportError:
    _AUDIO_OK = False

# ══════════════════════════════════════════════════
#  PALETA DE CORES
# ══════════════════════════════════════════════════
R     = Style.RESET_ALL
B     = Style.BRIGHT
D     = Style.DIM

ROXO  = Fore.MAGENTA  + Style.BRIGHT
AZUL  = Fore.CYAN     + Style.BRIGHT
VERDE = Fore.GREEN    + Style.BRIGHT
VERM  = Fore.RED      + Style.BRIGHT
AMAR  = Fore.YELLOW   + Style.BRIGHT
BRAN  = Fore.WHITE    + Style.BRIGHT
CINZA = Fore.WHITE    + Style.DIM
GOLD  = Fore.YELLOW   + Style.BRIGHT
CYAN  = Fore.CYAN


# ══════════════════════════════════════════════════
#  SISTEMA DE ÁUDIO
# ══════════════════════════════════════════════════
_mixer_ready  = False
_music_thread = None
_stop_music   = threading.Event()

def _init_audio() -> bool:
    """Inicializa pygame.mixer. Retorna True se bem-sucedido."""
    global _mixer_ready
    if not _AUDIO_OK or _mixer_ready:
        return _mixer_ready
    try:
        # Tenta driver padrão primeiro; cai em dummy se não houver hardware
        for driver in (None, "dummy"):
            try:
                if driver:
                    os.environ["SDL_AUDIODRIVER"] = driver
                pygame.mixer.pre_init(44100, -16, 1, 512)
                pygame.mixer.init()
                _mixer_ready = True
                return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def _gerar_som(freq: float, duracao: float, volume: float = 0.5,
               forma: str = "sine") -> "pygame.mixer.Sound":
    """Gera um Sound do pygame a partir de uma frequência."""
    sample_rate = 44100
    n_samples   = int(sample_rate * duracao)
    t = np.linspace(0, duracao, n_samples, endpoint=False)

    if forma == "sine":
        wave = np.sin(2 * np.pi * freq * t)
    elif forma == "square":
        wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif forma == "sawtooth":
        wave = 2 * (t * freq - np.floor(t * freq + 0.5))
    else:
        wave = np.sin(2 * np.pi * freq * t)

    # Envelope ADSR simples
    attack  = int(n_samples * 0.05)
    decay   = int(n_samples * 0.10)
    sustain = int(n_samples * 0.75)
    release = n_samples - attack - decay - sustain

    envelope = np.ones(n_samples)
    envelope[:attack]                               = np.linspace(0, 1, attack)
    envelope[attack:attack+decay]                   = np.linspace(1, 0.7, decay)
    envelope[attack+decay:attack+decay+sustain]     = 0.7
    envelope[attack+decay+sustain:]                 = np.linspace(0.7, 0, release)

    wave = (wave * envelope * volume * 32767).astype(np.int16)
    sound = pygame.sndarray.make_sound(wave)
    return sound


# ── Melodias ───────────────────────────────────────
# Cada nota: (frequência_Hz, duração_s)
# 0 Hz = pausa

def _freq(nota: str) -> float:
    """Converte nome de nota (ex: 'C4') em frequência."""
    notas = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
    if nota == "R":          # Rest / pausa
        return 0.0
    nome, oitava = nota[:-1], int(nota[-1])
    semitom = notas[nome] + (oitava + 1) * 12
    return 440.0 * (2 ** ((semitom - 69) / 12))


MELODIA_MENU = [
    # Tema épico suave de abertura
    ("C4", 0.3), ("E4", 0.3), ("G4", 0.3), ("C5", 0.5),
    ("R",  0.1), ("B4", 0.3), ("G4", 0.3), ("E4", 0.3),
    ("R",  0.15),("A4", 0.3), ("F4", 0.3), ("D4", 0.3), ("F4", 0.4),
    ("R",  0.1), ("G4", 0.5), ("E4", 0.3), ("C4", 0.6),
    ("R",  0.2),
    ("C4", 0.25),("D4", 0.25),("E4", 0.25),("F4", 0.25),
    ("G4", 0.4), ("A4", 0.4), ("B4", 0.4), ("C5", 0.6),
    ("R",  0.2),
    ("G4", 0.3), ("F4", 0.25),("E4", 0.25),("D4", 0.25),("C4", 0.5),
]

MELODIA_FASE1 = [
    # Ritmo tenso de combate
    ("E4", 0.2), ("R", 0.05), ("E4", 0.2), ("R", 0.05),
    ("G4", 0.3), ("R", 0.08), ("F4", 0.2), ("E4", 0.2),
    ("R",  0.1), ("D4", 0.2), ("R", 0.05), ("D4", 0.2),
    ("F4", 0.3), ("R", 0.08), ("E4", 0.2), ("D4", 0.2),
    ("R",  0.1), ("C4", 0.4), ("R", 0.1),
    ("G4", 0.2), ("R", 0.05), ("G4", 0.2), ("R", 0.05),
    ("A4", 0.3), ("G4", 0.2), ("F4", 0.2), ("E4", 0.4),
]

MELODIA_FASE2 = [
    # Tema místico / sábio
    ("A3", 0.4), ("C4", 0.3), ("E4", 0.3), ("G4", 0.5),
    ("R",  0.15),("F4", 0.3), ("E4", 0.3), ("D4", 0.3), ("C4", 0.5),
    ("R",  0.2), ("E4", 0.25),("F4", 0.25),("G4", 0.25),("A4", 0.4),
    ("B4", 0.4), ("A4", 0.3), ("G4", 0.3), ("F4", 0.3), ("E4", 0.6),
    ("R",  0.2), ("C4", 0.3), ("D4", 0.3), ("E4", 0.3), ("F4", 0.3),
    ("G4", 0.5), ("E4", 0.3), ("C4", 0.6),
]

MELODIA_VITORIA = [
    # Fanfarra de vitória
    ("C4", 0.2),("C4", 0.2),("C4", 0.2),("C4", 0.35),
    ("A3", 0.15),("C4", 0.35),
    ("R",  0.1), ("E4", 0.35),("E4", 0.35),("E4", 0.35),
    ("F4", 0.5), ("R", 0.1),
    ("G4", 0.2), ("G4", 0.2), ("G4", 0.6),
    ("R",  0.15),("F4", 0.2), ("E4", 0.2), ("D4", 0.2),
    ("C4", 0.7),
]

MELODIA_DERROTA = [
    # Descida dramática
    ("G4", 0.4), ("F4", 0.4), ("E4", 0.4), ("D4", 0.5),
    ("R",  0.2), ("C4", 0.4), ("B3", 0.4), ("A3", 0.6),
    ("R",  0.3), ("G3", 0.8),
]


def _tocar_melodia(melodia: list, loop: bool = False,
                   forma: str = "sine", vol: float = 0.4):
    """Toca uma melodia em thread separada. Pode fazer loop."""
    if not _init_audio():
        return
    _stop_music.clear()

    def _run():
        while not _stop_music.is_set():
            for nota, dur in melodia:
                if _stop_music.is_set():
                    return
                freq = _freq(nota)
                if freq > 0:
                    try:
                        som = _gerar_som(freq, dur, vol, forma)
                        som.play()
                        # Espera a duração da nota
                        fim = time.time() + dur
                        while time.time() < fim:
                            if _stop_music.is_set():
                                pygame.mixer.stop()
                                return
                            time.sleep(0.01)
                    except Exception:
                        time.sleep(dur)
                else:
                    # Pausa
                    fim = time.time() + dur
                    while time.time() < fim:
                        if _stop_music.is_set():
                            return
                        time.sleep(0.01)
            if not loop:
                return

    global _music_thread
    parar_musica()                          # Para a anterior
    _music_thread = threading.Thread(target=_run, daemon=True)
    _music_thread.start()


def parar_musica():
    """Para a música atual."""
    _stop_music.set()
    if _mixer_ready:
        try:
            pygame.mixer.stop()
        except Exception:
            pass
    global _music_thread
    if _music_thread and _music_thread.is_alive():
        _music_thread.join(timeout=1.0)
    _music_thread = None


def tocar_menu():
    _tocar_melodia(MELODIA_MENU, loop=True, forma="sine", vol=0.35)

def tocar_fase1():
    _tocar_melodia(MELODIA_FASE1, loop=True, forma="square", vol=0.25)

def tocar_fase2():
    _tocar_melodia(MELODIA_FASE2, loop=True, forma="sine", vol=0.35)

def tocar_vitoria():
    _tocar_melodia(MELODIA_VITORIA, loop=False, forma="sine", vol=0.5)

def tocar_derrota():
    _tocar_melodia(MELODIA_DERROTA, loop=False, forma="sine", vol=0.45)

def _beep_acerto():
    """Toca bip rápido de acerto."""
    if not _init_audio():
        return
    try:
        som = _gerar_som(880, 0.12, 0.4, "sine")
        som.play()
    except Exception:
        pass

def _beep_erro():
    """Toca bip grave de erro."""
    if not _init_audio():
        return
    try:
        som = _gerar_som(220, 0.25, 0.4, "square")
        som.play()
    except Exception:
        pass


# ══════════════════════════════════════════════════
#  UTILITÁRIOS DE TERMINAL
# ══════════════════════════════════════════════════
def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def digitar(texto: str, delay: float = 0.025):
    """Imprime texto com efeito de digitação."""
    for ch in texto:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def sep(char: str = "─", n: int = 60, cor: str = AZUL):
    """Linha separadora (nome evita conflito com variável 'linha')."""
    print(cor + char * n + R)

def espaco(n: int = 1):
    print("\n" * (n - 1))

def cabecalho(titulo: str, subtitulo: str = "", cor: str = ROXO):
    espaco()
    sep("═", 60, cor)
    print(cor + f"  {titulo}".center(60) + R)
    if subtitulo:
        print(CINZA + f"  {subtitulo}".center(60) + R)
    sep("═", 60, cor)
    espaco()

def pausar(seg: float = 0.6):
    time.sleep(seg)

def pedir_vf(prompt: str = "  ➤ Sua resposta (V/F): ") -> str:
    """Pede V ou F ao jogador. Retorna sempre 'V' ou 'F' (str)."""
    while True:
        try:
            r = input(AMAR + prompt + R).strip().upper()
        except EOFError:
            r = ""
        if r in ("V", "F"):
            return r
        print(VERM + "  ⚠  Digite apenas V ou F." + R)

def pedir_tcg(prompt: str = "  ➤ T, C ou G? ") -> str:
    """Pede T, C ou G. Retorna str."""
    while True:
        try:
            r = input(AMAR + prompt + R).strip().upper()
        except EOFError:
            r = ""
        if r in ("T", "C", "G"):
            return r
        print(VERM + "  ⚠  Digite apenas T, C ou G." + R)

def pedir_sim_nao(prompt: str) -> bool:
    """Retorna True para sim, False para não."""
    while True:
        try:
            r = input(AMAR + prompt + R).strip().lower()
        except EOFError:
            return False
        if r in ("sim", "s", "não", "nao", "n"):
            return r in ("sim", "s")
        print(VERM + "  ⚠  Digite sim ou não." + R)

def colorir_vf(v) -> str:
    """
    Colore 'V'/'F' ou True/False.
    Aceita tanto str ('V','F') quanto bool (True, False).
    """
    if isinstance(v, bool):
        return (VERDE + "V" + R) if v else (VERM + "F" + R)
    return (VERDE + "V" + R) if str(v).upper() == "V" else (VERM + "F" + R)

def barra_progresso(atual: int, total: int, largura: int = 30, cor: str = ROXO):
    """Barra de progresso. Protege contra divisão por zero."""
    total = max(total, 1)                   # FIX: evita ZeroDivisionError
    preenchido = int(largura * atual / total)
    barra = "█" * preenchido + "░" * (largura - preenchido)
    pct   = int(atual / total * 100)
    print(cor + f"  [{barra}] {pct}%" + R)

def coracoes(vidas: int, maximo: int) -> str:
    return "❤️ " * max(vidas, 0) + "🖤 " * max(maximo - vidas, 0)

def banner_ascii():
    print(ROXO + r"""
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
    ("P ∨ ¬P",               lambda p, q: p or not p,                        "Tautologia"),
    ("¬P ∨ P",               lambda p, q: not p or p,                        "Tautologia"),
    ("P → P",                lambda p, q: not p or p,                        "Tautologia"),
    ("(P ∧ Q) → P",          lambda p, q: not (p and q) or p,                "Tautologia"),
    ("P → (Q → P)",          lambda p, q: not p or (not q or p),             "Tautologia"),
    ("¬(P ∧ ¬P)",            lambda p, q: not (p and not p),                  "Tautologia"),
    # Contradições
    ("P ∧ ¬P",               lambda p, q: p and not p,                        "Contradição"),
    ("¬P ∧ P",               lambda p, q: not p and p,                        "Contradição"),
    ("¬(P ∨ ¬P)",            lambda p, q: not (p or not p),                   "Contradição"),
    ("P ∧ (¬P ∧ Q)",         lambda p, q: p and (not p and q),                "Contradição"),
    ("(P → Q) ∧ (P ∧ ¬Q)",  lambda p, q: (not p or q) and (p and not q),     "Contradição"),
    ("(P ∨ Q) ∧ ¬(P ∨ Q)",  lambda p, q: (p or q) and not (p or q),          "Contradição"),
    # Contingências
    ("P ∧ Q",                lambda p, q: p and q,                            "Contingência"),
    ("P ∨ Q",                lambda p, q: p or q,                             "Contingência"),
    ("P → Q",                lambda p, q: not p or q,                         "Contingência"),
    ("¬(P ∧ Q)",             lambda p, q: not (p and q),                      "Contingência"),
    ("¬(P ∨ Q)",             lambda p, q: not (p or q),                       "Contingência"),
    ("P ↔ Q",                lambda p, q: p == q,                             "Contingência"),
]

COMBOS  = [(True, True), (True, False), (False, True), (False, False)]
LABEL   = {True: "V", False: "F"}
CAT_MAP = {"T": "Tautologia", "C": "Contradição", "G": "Contingência"}
CAT_COR = {"Tautologia": VERDE, "Contradição": VERM, "Contingência": AMAR}
CAT_ICO = {"Tautologia": "🟢",  "Contradição": "🔴",  "Contingência": "🟡"}


def montar_fase2() -> list:
    """Garante ao menos 1 de cada categoria nas 6 questões."""
    cats   = ["Tautologia", "Contradição", "Contingência"]
    por_cat = {c: [f for f in FASE2_POOL if f[2] == c] for c in cats}
    for v in por_cat.values():
        random.shuffle(v)
    sel  = [por_cat[c].pop() for c in cats]
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
    sep("═", 60, ROXO)
    banner_ascii()
    sep("═", 60, ROXO)
    espaco()

    if _AUDIO_OK:
        print(CINZA + "  🎵 Música: ativada" + R)
    else:
        print(CINZA + "  🔇 Música: instale numpy e pygame para ativar" + R)
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
    sep("─", 60, CINZA)


# ══════════════════════════════════════════════════
#  FASE 1
# ══════════════════════════════════════════════════
def fase1(nome: str):
    limpar()
    cabecalho("⚡  FASE 1 — Julgamento do Oráculo", "Fase 01 de 02", AZUL)

    digitar(CINZA + "  O Oráculo lança proposições diante de você." + R, 0.02)
    digitar(CINZA + "  Julgue cada expressão: V (Verdadeiro) ou F (Falso)." + R, 0.02)
    digitar(CINZA + "  Seis questões. Mínimo de 4 acertos para avançar." + R, 0.02)
    espaco()
    try:
        input(CINZA + "  [ Pressione ENTER para começar ] " + R)
    except EOFError:
        pass

    tocar_fase1()                           # 🎵 Música de combate

    pool   = random.sample(FASE1_POOL, 6)
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
        sep("─", 60, CINZA)
        print(BRAN + f"\n     Expressão:  {GOLD}{expr}{R}\n")
        sep("─", 60, CINZA)
        espaco()

        resp        = pedir_vf()
        correto_str = "V" if gabarito else "F"
        espaco()

        if resp == correto_str:
            pontos += 1
            _beep_acerto()
            print(VERDE + "  ╔══════════════════════════╗")
            print(VERDE + "  ║   ✅  CORRETO!   +1 pt   ║")
            print(VERDE + "  ╚══════════════════════════╝" + R)
            digitar(CINZA + f"\n  A expressão é {colorir_vf(correto_str)}.", 0.02)
        else:
            vidas -= 1
            _beep_erro()
            print(VERM + "  ╔══════════════════════════════════╗")
            print(VERM + f"  ║  ❌  ERROU!  Correto: {correto_str}          ║")
            print(VERM + "  ╚══════════════════════════════════╝" + R)
            if vidas == 0:
                digitar(VERM + "\n  💀 Sem vidas! Missão comprometida.", 0.02)

        pausar(1.2)

    # ── Resultado Fase 1 ──
    limpar()
    cabecalho("📊  RESULTADO — FASE 1", "", AZUL)
    print(BRAN + f"  Pontos: {pontos}/6   Vidas restantes: {vidas}" + R)
    barra_progresso(pontos, 6, cor=AZUL)
    espaco()

    if vidas == 0 or pontos < 4:
        parar_musica()
        tocar_derrota()
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
def narracao_entre_fases(nome: str, pts1: int):
    parar_musica()
    tocar_menu()                            # 🎵 Música ambiente entre fases
    limpar()
    sep("═", 60, ROXO)
    print(ROXO + "  ◈  TRANSMISSÃO DA ORDEM DOS ARQUITETOS  ◈".center(60) + R)
    sep("═", 60, ROXO)
    espaco()

    digitar(GOLD + f"  Impressionante, {nome}.", 0.03)
    espaco()
    digitar(BRAN + "  Você provou que pode ler as proposições elementares.", 0.02)
    digitar(BRAN + "  Mas o verdadeiro desafio aguarda.", 0.02)
    espaco()
    digitar(CYAN + "  A Fase 2 exige que você construa as Tabelas Sagradas", 0.02)
    digitar(CYAN + "  do zero — e classifique a natureza de cada fórmula.", 0.02)
    espaco()

    print(VERDE + "  🟢  T = TAUTOLOGIA   → sempre Verdadeira" + R)
    print(VERM  + "  🔴  C = CONTRADIÇÃO  → sempre Falsa" + R)
    print(AMAR  + "  🟡  G = CONTINGÊNCIA → mistura de V e F" + R)
    espaco()

    digitar(GOLD + "  O destino dos mundos está em suas mãos.", 0.03)
    espaco()
    print(CINZA + f"  Pontuação atual: {pts1}/6 pts  — máximo possível: 18 pts" + R)
    espaco()
    try:
        input(CINZA + "  [ Pressione ENTER para a Fase 2 ] " + R)
    except EOFError:
        pass


# ══════════════════════════════════════════════════
#  FASE 2
# ══════════════════════════════════════════════════
def fase2(nome: str):
    parar_musica()
    limpar()
    cabecalho("⚔️  FASE 2 — As Tabelas Sagradas", "Fase 02 de 02", ROXO)

    digitar(CINZA + "  Para cada fórmula, preencha a tabela verdade (V ou F)" + R, 0.02)
    digitar(CINZA + "  e classifique a fórmula: T, C ou G." + R, 0.02)
    digitar(CINZA + "  Tabela correta = +1 pt  |  Classificação correta = +1 pt" + R, 0.02)
    espaco()
    try:
        input(CINZA + "  [ Pressione ENTER para começar ] " + R)
    except EOFError:
        pass

    tocar_fase2()                           # 🎵 Música mística fase 2

    formulas = montar_fase2()
    pontos   = 0
    vidas    = 5

    for i, (nome_formula, fn, cat) in enumerate(formulas):
        if vidas == 0:
            break

        limpar()
        cabecalho("⚔️  FASE 2 — As Tabelas Sagradas", "Fase 02 de 02", ROXO)

        # HUD
        print(f"  {ROXO}Fórmula {i+1}/6{R}  {coracoes(vidas, 5)}  {GOLD}⚡ {pontos} pts{R}")
        barra_progresso(i, 6, cor=ROXO)
        espaco()

        # Fórmula
        sep("─", 60, CINZA)
        print(BRAN + f"\n  Fórmula Sagrada:  {GOLD}{nome_formula}{R}\n")
        sep("─", 60, CINZA)
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
            pv    = colorir_vf(LABEL[p])
            qv    = colorir_vf(LABEL[q])
            rjv   = colorir_vf(rj)
            rcv   = colorir_vf(rc)
            icone = VERDE + "  ✔  " + R if rj == rc else VERM + "  ✘  " + R
            print(f"  {CINZA}│{R}  {pv}   {CINZA}│{R}  {qv}   {CINZA}│{R}   {rjv}    {CINZA}│{R}    {rcv}    {CINZA}│{R} {icone}{CINZA}│{R}")

        print(CINZA + "  └──────┴──────┴──────────┴──────────┴────────┘" + R)
        espaco()

        if acertos_tabela == 4:
            print(VERDE + f"  ✅  Tabela perfeita! 4/4 linhas corretas." + R)
        else:
            print(AMAR + f"  ⚠   {acertos_tabela}/4 linhas corretas na tabela." + R)
        espaco()

        # Classificação
        sep("─", 60, CINZA)
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
        ganho  = int(ganhou_tabela) + int(ganhou_classe)
        pontos += ganho

        cat_cor = CAT_COR[cat]
        cat_ico = CAT_ICO[cat]

        if ganhou_tabela and ganhou_classe:
            _beep_acerto()
            print(VERDE + "  ╔══════════════════════════════════════════════╗")
            print(VERDE + "  ║  🏆  PERFEITO! Tabela + Classe correta  +2  ║")
            print(VERDE + f"  ║  {cat_ico} A fórmula é {cat:<28}║")
            print(VERDE + "  ╚══════════════════════════════════════════════╝" + R)
        elif ganhou_tabela and not ganhou_classe:
            _beep_erro()
            print(AMAR + "  ╔══════════════════════════════════════════════╗")
            print(AMAR + "  ║  ✅ Tabela certa   ❌ Classe errada     +1   ║")
            print(AMAR + f"  ║  {cat_ico} Correto: {cat:<33}║")
            print(AMAR + "  ╚══════════════════════════════════════════════╝" + R)
            vidas -= 1
        elif not ganhou_tabela and ganhou_classe:
            _beep_erro()
            print(AMAR + "  ╔══════════════════════════════════════════════╗")
            print(AMAR + "  ║  ❌ Tabela errada  ✅ Classe certa      +1   ║")
            print(AMAR + "  ╚══════════════════════════════════════════════╝" + R)
            vidas -= 1
        else:
            _beep_erro()
            print(VERM + "  ╔══════════════════════════════════════════════╗")
            print(VERM + "  ║  ❌ Tabela errada  ❌ Classe errada     +0   ║")
            print(VERM + f"  ║  {cat_ico} Correto: {cat:<33}║")
            print(VERM + "  ╚══════════════════════════════════════════════╝" + R)
            vidas -= 1

        if vidas == 0:
            digitar(VERM + "\n  💀 Sem vidas! A missão foi comprometida.", 0.02)

        pausar(1.2)
        if i < 5 and vidas > 0:
            try:
                input(CINZA + "\n  [ ENTER → próxima fórmula ] " + R)
            except EOFError:
                pass

    return pontos, vidas


# ══════════════════════════════════════════════════
#  TELA FINAL
# ══════════════════════════════════════════════════
def tela_final(nome: str, pts1: int, pts2: int, vidas2: int):
    parar_musica()
    limpar()
    total  = pts1 + pts2
    maximo = 18
    pct    = int(total / maximo * 100)

    sep("═", 60, ROXO)
    print(ROXO + "  🏁  FIM DA MISSÃO".center(60) + R)
    sep("═", 60, ROXO)
    espaco()

    print(BRAN + f"  Fase 1  ▸  {pts1}/6 pontos" + R)
    print(BRAN + f"  Fase 2  ▸  {pts2}/12 pontos  (tabela + classificação)" + R)
    sep("─", 60, CINZA)
    print(GOLD + f"  TOTAL   ▸  {total}/{maximo} pontos  ({pct}%)" + R)
    espaco()
    barra_progresso(total, maximo, cor=GOLD)
    espaco()

    # Rank e história
    if total >= 16:
        titulo   = "⚜  GRÃO-ARQUITETO  ⚜"
        cor      = GOLD
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
        tocar_vitoria()
    elif total >= 12:
        titulo   = "◈  ARQUITETO MESTRE  ◈"
        cor      = AZUL
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
        tocar_vitoria()
    elif total >= 7:
        titulo   = "▸  ARQUITETO APRENDIZ"
        cor      = CYAN
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
        tocar_derrota()
    else:
        titulo   = "☠  INICIANTE CAÓTICO"
        cor      = VERM
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
        tocar_derrota()

    sep("─", 60, cor)
    print(cor + f"  {titulo}".center(60) + R)
    sep("─", 60, cor)
    espaco()
    for txt in historia.split("\n"):
        digitar(BRAN + txt + R, 0.015)
    espaco()
    sep("─", 60, CINZA)
    for txt in desfecho.split("\n"):
        digitar(CINZA + txt + R, 0.015)
    espaco()
    sep("═", 60, ROXO)
    print(CINZA + "  Obrigado por jogar! 🎮  |  LÓGICA v2.1" + R)
    sep("═", 60, ROXO)
    espaco()


# ══════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ══════════════════════════════════════════════════
def main():
    while True:
        tela_abertura()
        tocar_menu()                        # 🎵 Música do menu principal
        espaco()

        try:
            nome = input(AMAR + "  👤 Qual seu nome, Arquiteto? " + R).strip() or "Arquiteto"
        except EOFError:
            nome = "Arquiteto"
        espaco()

        if not pedir_sim_nao(f"  {nome}, você está preparado(a) para a missão? (sim/não): "):
            parar_musica()
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
            pausar(2.0)                     # Deixa a música de derrota tocar
            parar_musica()
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

        pausar(3.0)                         # Deixa a música final tocar
        parar_musica()
        espaco()
        if not pedir_sim_nao("  Jogar novamente? (sim/não): "):
            digitar(CINZA + "\n  Até a próxima, Arquiteto. A Ordem aguarda seu retorno. 👋" + R)
            espaco()
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        parar_musica()
        espaco()
        print(CINZA + "\n  Jogo interrompido. Até logo, Arquiteto! 👋" + R)
        espaco()
    finally:
        parar_musica()
        if _mixer_ready:
            try:
                pygame.mixer.quit()
            except Exception:
                pass