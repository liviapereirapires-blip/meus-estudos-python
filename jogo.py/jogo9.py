# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║       LÓGICA — O DESPERTAR DA RAZÃO  v3.0 Pygame    ║
║   Jogo de Tabela Verdade | Lógica Proposicional      ║
╚══════════════════════════════════════════════════════╝

Instale as dependências antes de rodar:
    pip install pygame

Depois execute:
    python logica_pygame.py
"""

import pygame
import sys
import math
import random
import time

# ══════════════════════════════════════════════════════
#  INICIALIZAÇÃO
# ══════════════════════════════════════════════════════
pygame.init()
pygame.mixer.init()

W, H = 900, 650
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("LÓGICA — O Despertar da Razão v3.0")
clock = pygame.time.Clock()

# ══════════════════════════════════════════════════════
#  CORES
# ══════════════════════════════════════════════════════
C = {
    "bg":       (8,   9,  20),
    "panel":    (13,  16,  32),
    "panel2":   (18,  22,  44),
    "border":   (30,  42,  74),
    "roxo":     (176, 110, 255),
    "roxo_d":   (106,  0, 255),
    "azul":     (0,  229, 255),
    "azul_d":   (0,  106, 255),
    "verde":    (0,  255, 136),
    "verde_d":  (0,  102,  54),
    "verm":     (255,  51,  85),
    "verm_d":   (170,   0,  34),
    "amar":     (255, 215,   0),
    "gold":     (255, 204,   0),
    "cinza":    (136, 153, 170),
    "branco":   (200, 216, 240),
    "preto":    (0,     0,   0),
    "trans_ok": (0,  255, 136,  40),
    "trans_err":(255,  51,  85,  40),
    "trans_warn":(255,215,  0,  40),
}

# ══════════════════════════════════════════════════════
#  FONTES
# ══════════════════════════════════════════════════════
def load_font(size, bold=False):
    try:
        return pygame.font.SysFont("monospace", size, bold=bold)
    except:
        return pygame.font.Font(None, size)

F_TITLE  = load_font(42, bold=True)
F_BIG    = load_font(30, bold=True)
F_MED    = load_font(22, bold=True)
F_SMALL  = load_font(18)
F_TINY   = load_font(15)
F_EXPR   = load_font(34, bold=True)

# ══════════════════════════════════════════════════════
#  BANCO DE QUESTÕES — FASE 1
# ══════════════════════════════════════════════════════
FASE1_POOL = [
    ("¬V",           False),
    ("¬F",           True),
    ("V ∧ V",        True),
    ("V ∧ F",        False),
    ("F ∧ V",        False),
    ("F ∧ F",        False),
    ("V ∨ V",        True),
    ("V ∨ F",        True),
    ("F ∨ F",        False),
    ("F ∨ V",        True),
    ("V → V",        True),
    ("V → F",        False),
    ("F → V",        True),
    ("F → F",        True),
    ("V ∧ (F ∨ V)",  True),
    ("F ∨ (V ∧ F)",  False),
    ("¬(V ∧ F)",     True),
    ("¬(V ∨ F)",     False),
    ("V → (F → V)",  True),
    ("(V ∧ V) → F",  False),
    ("¬(F → F)",     False),
    ("(F ∨ V) → F",  False),
    ("V ↔ V",        True),
    ("V ↔ F",        False),
]

# ══════════════════════════════════════════════════════
#  BANCO DE QUESTÕES — FASE 2
#  Regras aplicadas e verificadas:
#   ¬P    = not p
#   P∧Q   = p and q        (V só se ambos V)
#   P∨Q   = p or q         (V se ao menos um V)
#   P→Q   = not p or q     (F só se P=V e Q=F)
#   P↔Q   = p == q         (V se iguais)
#  Todas as fórmulas usam P e Q (variáveis diferentes)
# ══════════════════════════════════════════════════════
FASE2_POOL = [
    # ── TAUTOLOGIAS (sempre V) ────────────────────────
    # VV=V VF=V FV=V FF=V
    {
        "expr": "(P ∧ Q) → P",
        "fn":   lambda p, q: not (p and q) or p,
        "cat":  "Tautologia",
    },
    {
        "expr": "(P ∧ Q) → Q",
        "fn":   lambda p, q: not (p and q) or q,
        "cat":  "Tautologia",
    },
    {
        "expr": "P → (Q → P)",
        # VV: not V or (not V or V)=V | VF: not V or(not F or V)=V
        # FV: not F or(not V or F)=V  | FF: not F or(not F or F)=V
        "fn":   lambda p, q: (not p) or ((not q) or p),
        "cat":  "Tautologia",
    },
    {
        "expr": "(P → Q) ∨ (Q → P)",
        # VV: V∨V=V | VF: F∨V=V | FV: V∨F=V | FF: V∨V=V
        "fn":   lambda p, q: (not p or q) or (not q or p),
        "cat":  "Tautologia",
    },
    {
        "expr": "P → (P ∨ Q)",
        # VV:V→V=V | VF:V→V=V | FV:F→V=V | FF:F→F=V
        "fn":   lambda p, q: (not p) or (p or q),
        "cat":  "Tautologia",
    },
    {
        "expr": "Q → (P ∨ Q)",
        "fn":   lambda p, q: (not q) or (p or q),
        "cat":  "Tautologia",
    },
    {
        "expr": "(P ∧ Q) → (P ∨ Q)",
        # VV:V→V=V | VF:F→V=V | FV:F→V=V | FF:F→F=V
        "fn":   lambda p, q: not (p and q) or (p or q),
        "cat":  "Tautologia",
    },
    {
        "expr": "(P ∨ Q) → (Q ∨ P)",
        # Comutatividade da disjunção — sempre V
        "fn":   lambda p, q: not (p or q) or (q or p),
        "cat":  "Tautologia",
    },
    {
        "expr": "(P ∧ Q) → (Q ∧ P)",
        # Comutatividade da conjunção — sempre V
        "fn":   lambda p, q: not (p and q) or (q and p),
        "cat":  "Tautologia",
    },

    # ── CONTRADIÇÕES (sempre F) ───────────────────────
    {
        "expr": "(P → Q) ∧ P ∧ ¬Q",
        # VV:(V)∧V∧F=F | VF:(F)∧V∧V=F | FV:(V)∧F∧F=F | FF:(V)∧F∧V=F
        "fn":   lambda p, q: (not p or q) and p and (not q),
        "cat":  "Contradição",
    },
    {
        "expr": "(P ∨ Q) ∧ ¬P ∧ ¬Q",
        # VV:V∧F∧F=F | VF:V∧F∧V=F | FV:V∧V∧F=F | FF:F∧V∧V=F
        "fn":   lambda p, q: (p or q) and (not p) and (not q),
        "cat":  "Contradição",
    },
    {
        "expr": "P ∧ ¬P ∧ Q",
        # p and not p é sempre False, q não muda isso
        "fn":   lambda p, q: p and (not p) and q,
        "cat":  "Contradição",
    },
    {
        "expr": "(P ↔ Q) ∧ P ∧ ¬Q",
        # VV:(V)∧V∧F=F | VF:(F)∧V∧V=F | FV:(F)∧F∧F=F | FF:(V)∧F∧V=F
        "fn":   lambda p, q: (p == q) and p and (not q),
        "cat":  "Contradição",
    },
    {
        "expr": "¬(P ∨ Q) ∧ P",
        # VV:F∧V=F | VF:F∧V=F | FV:F∧F=F | FF:V∧F=F
        "fn":   lambda p, q: not (p or q) and p,
        "cat":  "Contradição",
    },
    {
        "expr": "¬(P ∨ Q) ∧ Q",
        # VV:F∧V=F | VF:F∧F=F | FV:F∧V=F | FF:V∧F=F
        "fn":   lambda p, q: not (p or q) and q,
        "cat":  "Contradição",
    },

    # ── CONTINGÊNCIAS (mistura V e F) ─────────────────
    {
        "expr": "P ∧ Q",
        # VV=V VF=F FV=F FF=F
        "fn":   lambda p, q: p and q,
        "cat":  "Contingência",
    },
    {
        "expr": "P ∨ Q",
        # VV=V VF=V FV=V FF=F
        "fn":   lambda p, q: p or q,
        "cat":  "Contingência",
    },
    {
        "expr": "P → Q",
        # VV=V VF=F FV=V FF=V
        "fn":   lambda p, q: not p or q,
        "cat":  "Contingência",
    },
    {
        "expr": "Q → P",
        # VV=V VF=V FV=F FF=V
        "fn":   lambda p, q: not q or p,
        "cat":  "Contingência",
    },
    {
        "expr": "P ↔ Q",
        # VV=V VF=F FV=F FF=V
        "fn":   lambda p, q: p == q,
        "cat":  "Contingência",
    },
    {
        "expr": "¬(P ∧ Q)",
        # VV=F VF=V FV=V FF=V
        "fn":   lambda p, q: not (p and q),
        "cat":  "Contingência",
    },
    {
        "expr": "¬(P ∨ Q)",
        # VV=F VF=F FV=F FF=V
        "fn":   lambda p, q: not (p or q),
        "cat":  "Contingência",
    },
    {
        "expr": "¬(P ↔ Q)",
        # VV=F VF=V FV=V FF=F
        "fn":   lambda p, q: not (p == q),
        "cat":  "Contingência",
    },
    {
        "expr": "¬P ∧ Q",
        # VV=F VF=F FV=V FF=F
        "fn":   lambda p, q: (not p) and q,
        "cat":  "Contingência",
    },
    {
        "expr": "P ∧ ¬Q",
        # VV=F VF=V FV=F FF=F
        "fn":   lambda p, q: p and (not q),
        "cat":  "Contingência",
    },
    {
        "expr": "¬P ∨ Q",
        # VV=V VF=F FV=V FF=V
        "fn":   lambda p, q: (not p) or q,
        "cat":  "Contingência",
    },
    {
        "expr": "P ∨ ¬Q",
        # VV=V VF=V FV=F FF=V
        "fn":   lambda p, q: p or (not q),
        "cat":  "Contingência",
    },
    {
        "expr": "(P ∧ Q) ∨ (¬P ∧ ¬Q)",
        # VV=V VF=F FV=F FF=V  (equivalente a P↔Q)
        "fn":   lambda p, q: (p and q) or ((not p) and (not q)),
        "cat":  "Contingência",
    },
    {
        "expr": "(P ∨ Q) ∧ ¬(P ∧ Q)",
        # VV=F VF=V FV=V FF=F  (XOR)
        "fn":   lambda p, q: (p or q) and not (p and q),
        "cat":  "Contingência",
    },
]

COMBOS = [(True, True), (True, False), (False, True), (False, False)]
LABEL  = {True: "V", False: "F"}
CAT_MAP = {"T": "Tautologia", "C": "Contradição", "G": "Contingência"}
CAT_KEY = {"Tautologia": "T", "Contradição": "C", "Contingência": "G"}
CAT_COR = {
    "Tautologia":  C["verde"],
    "Contradição": C["verm"],
    "Contingência": C["amar"],
}

# ══════════════════════════════════════════════════════
#  AUTO-VERIFICAÇÃO DO BANCO (roda uma vez ao iniciar)
# ══════════════════════════════════════════════════════
def verificar_banco():
    erros = []
    for f in FASE2_POOL:
        results = [f["fn"](p, q) for p, q in COMBOS]
        todos_v = all(r is True  for r in results)
        todos_f = all(r is False for r in results)
        calc = "Tautologia" if todos_v else ("Contradição" if todos_f else "Contingência")
        if calc != f["cat"]:
            erros.append(f['expr'])
    if erros:
        print("⚠️  ERROS NO BANCO:", erros)
    else:
        print(f"✅ Banco verificado — {len(FASE2_POOL)} fórmulas corretas.")

verificar_banco()

# ══════════════════════════════════════════════════════
#  PARTÍCULAS DE FUNDO
# ══════════════════════════════════════════════════════
class Particula:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x   = random.randint(0, W)
        self.y   = random.randint(0, H)
        self.vx  = random.uniform(-0.3, 0.3)
        self.vy  = random.uniform(-0.3, 0.3)
        self.r   = random.uniform(0.5, 2.0)
        self.alpha = random.randint(30, 120)
        self.cor = random.choice([
            (68,  0, 255),
            (0,  136, 255),
            (0,  204, 255),
            (136, 0,  255),
        ])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0: self.x = W
        if self.x > W: self.x = 0
        if self.y < 0: self.y = H
        if self.y > H: self.y = 0

    def draw(self, surf):
        s = pygame.Surface((int(self.r*2+2), int(self.r*2+2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, self.alpha),
                           (int(self.r+1), int(self.r+1)), int(self.r))
        surf.blit(s, (int(self.x - self.r), int(self.y - self.r)))

particulas = [Particula() for _ in range(90)]

# ══════════════════════════════════════════════════════
#  UTILITÁRIOS DE DESENHO
# ══════════════════════════════════════════════════════
def txt(surf, texto, fonte, cor, cx, cy, anchor="center"):
    s = fonte.render(str(texto), True, cor)
    r = s.get_rect()
    if anchor == "center": r.center = (cx, cy)
    elif anchor == "left":  r.midleft = (cx, cy)
    elif anchor == "right": r.midright = (cx, cy)
    surf.blit(s, r)
    return r

def rect_grad(surf, x, y, w, h, c1, c2, radius=10):
    """Retângulo com gradiente horizontal aproximado."""
    for i in range(w):
        t = i / max(w - 1, 1)
        cor = tuple(int(c1[j] + (c2[j]-c1[j])*t) for j in range(3))
        pygame.draw.line(surf, cor, (x+i, y+radius), (x+i, y+h-radius))
    pygame.draw.rect(surf, c1, (x, y, w, h), border_radius=radius)

def panel(surf, x, y, w, h, radius=12, alpha=None):
    """Painel com borda."""
    if alpha:
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*C["panel"], alpha), (0, 0, w, h), border_radius=radius)
        pygame.draw.rect(s, (*C["border"], 200), (0, 0, w, h), 1, border_radius=radius)
        surf.blit(s, (x, y))
    else:
        pygame.draw.rect(surf, C["panel"],  (x, y, w, h), border_radius=radius)
        pygame.draw.rect(surf, C["border"], (x, y, w, h), 1, border_radius=radius)

def barra(surf, x, y, w, h, pct, c1=None, c2=None, radius=4):
    c1 = c1 or C["roxo"]
    c2 = c2 or C["azul"]
    pygame.draw.rect(surf, C["panel2"], (x, y, w, h), border_radius=radius)
    fill = int(w * pct)
    if fill > 0:
        for i in range(fill):
            t = i / max(fill-1, 1)
            cor = tuple(int(c1[j]+(c2[j]-c1[j])*t) for j in range(3))
            pygame.draw.line(surf, cor, (x+i, y+2), (x+i, y+h-2))
        pygame.draw.rect(surf, C["border"], (x, y, fill, h), border_radius=radius)

def botao(surf, texto, x, y, w, h, cor1, cor2, hover=False, radius=8):
    alpha = 255 if hover else 220
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    for i in range(w):
        t = i/max(w-1,1)
        c = tuple(int(cor1[j]+(cor2[j]-cor1[j])*t) for j in range(3))
        pygame.draw.line(s, (*c, alpha), (i, radius), (i, h-radius))
    pygame.draw.rect(s, (*cor1, alpha), (0,0,w,h), border_radius=radius)
    if hover:
        pygame.draw.rect(s, (255,255,255,40), (0,0,w,h), border_radius=radius)
    pygame.draw.rect(s, (*C["border"], 180), (0,0,w,h), 1, border_radius=radius)
    surf.blit(s, (x, y))
    txt(surf, texto, F_SMALL, C["branco"], x+w//2, y+h//2)

def coracoes(v, maximo):
    return "♥" * v + "♡" * (maximo - v)

def fundo(surf, t):
    surf.fill(C["bg"])
    for p in particulas:
        p.update()
        p.draw(surf)
    # linha decorativa no topo
    for i in range(W):
        shade = int(80 + 40*math.sin(i*0.02 + t*0.03))
        pygame.draw.line(surf, (shade//4, shade//4, shade//2), (i, 0), (i, 2))

def titulo_jogo(surf, t):
    txt_str = "LÓGICA"
    shift = math.sin(t * 0.04) * 2
    # sombra
    s = F_TITLE.render(txt_str, True, C["roxo_d"])
    surf.blit(s, s.get_rect(center=(W//2+2, 42+shift+2)))
    # principal
    s = F_TITLE.render(txt_str, True, C["roxo"])
    surf.blit(s, s.get_rect(center=(W//2, 42+shift)))
    txt(surf, "✦  O  D E S P E R T A R  D A  R A Z Ã O  ✦",
        F_TINY, C["gold"], W//2, 72+shift)

# ══════════════════════════════════════════════════════
#  CLASSE BOTÃO INTERATIVO
# ══════════════════════════════════════════════════════
class Btn:
    def __init__(self, texto, x, y, w, h, c1, c2, tag=None):
        self.texto = texto
        self.rect  = pygame.Rect(x, y, w, h)
        self.c1, self.c2 = c1, c2
        self.tag   = tag
        self.hover = False
        self.disabled = False

    def update(self, mouse):
        if not self.disabled:
            self.hover = self.rect.collidepoint(mouse)

    def draw(self, surf):
        botao(surf, self.texto, self.rect.x, self.rect.y,
              self.rect.w, self.rect.h,
              self.c1 if not self.disabled else C["cinza"],
              self.c2 if not self.disabled else C["border"],
              self.hover and not self.disabled)

    def clicked(self, event):
        if self.disabled: return False
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))

# ══════════════════════════════════════════════════════
#  NOTIFICAÇÃO FLUTUANTE
# ══════════════════════════════════════════════════════
class Notif:
    def __init__(self):
        self.msg = ""
        self.timer = 0
        self.cor = C["verde"]

    def show(self, msg, cor=None):
        self.msg   = msg
        self.timer = 150
        self.cor   = cor or C["verde"]

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self, surf):
        if self.timer <= 0: return
        alpha = min(255, self.timer * 8)
        s = pygame.Surface((340, 44), pygame.SRCALPHA)
        pygame.draw.rect(s, (*C["panel"], alpha), (0,0,340,44), border_radius=8)
        pygame.draw.rect(s, (*self.cor, alpha), (0,0,4,44), border_radius=4)
        pygame.draw.rect(s, (*C["border"], alpha//2), (0,0,340,44), 1, border_radius=8)
        fs = F_TINY.render(self.msg, True, (*self.cor, alpha))
        s.blit(fs, fs.get_rect(midleft=(12, 22)))
        surf.blit(s, (W - 350, 16))

notif = Notif()

# ══════════════════════════════════════════════════════
#  ESTADO GLOBAL
# ══════════════════════════════════════════════════════
state = {
    "tela":    "intro",   # intro | fase1 | trans | fase2 | result | gameover
    "nome":    "Arquiteto",
    "f1_pool": [], "f1_idx": 0, "f1_pts": 0, "f1_vidas": 6,
    "f2_pool": [], "f2_idx": 0, "f2_pts": 0, "f2_vidas": 5,
    "f2_res":  [None, None, None, None],  # respostas do jogador
    "f2_fase": "tabela",   # tabela | done
    "f2_lock": False,
    "f2_fb":   "",         # feedback texto
    "f2_fb_cor": C["verde"],
    "tick": 0,
    "digitando": "",
    "cursor_vis": True,
    "cursor_timer": 0,
}

# ══════════════════════════════════════════════════════
#  MONTAGEM DOS POOLS
# ══════════════════════════════════════════════════════
def montar_f1():
    pool = random.sample(FASE1_POOL, 6)
    state["f1_pool"]  = pool
    state["f1_idx"]   = 0
    state["f1_pts"]   = 0
    state["f1_vidas"] = 6

def montar_f2():
    cats = ["Tautologia", "Contradição", "Contingência"]
    por = {c: [f for f in FASE2_POOL if f["cat"] == c] for c in cats}
    for v in por.values(): random.shuffle(v)
    sel = [por[c].pop() for c in cats]
    resto = [f for f in FASE2_POOL if f not in sel]
    random.shuffle(resto)
    sel += resto[:3]
    random.shuffle(sel)
    state["f2_pool"]  = sel
    state["f2_idx"]   = 0
    state["f2_pts"]   = 0
    state["f2_vidas"] = 5

def reset_f2_q():
    state["f2_res"]  = [None, None, None, None]
    state["f2_fase"] = "tabela"
    state["f2_lock"] = False
    state["f2_fb"]   = ""

# ══════════════════════════════════════════════════════
#  TELA: INTRO
# ══════════════════════════════════════════════════════
inp_ativo = True
nome_str  = ""

btn_iniciar = Btn("⚡  INICIAR MISSÃO", W//2-140, 480, 280, 46,
                  C["roxo_d"], C["roxo"])

STORY = [
    "No ano de 3047, a humanidade descobriu que o universo é",
    "governado por uma força suprema: a Lógica Pura.",
    "",
    "A Ordem dos Arquitetos mantém o equilíbrio dos mundos",
    "através de Tabelas Sagradas — fórmulas que definem",
    "o que é real e o que é ilusão.",
    "",
    "Uma ruptura foi detectada. Um agente renegado corrompeu",
    "os registros da Ordem.",
    "",
    "Apenas um Arquiteto treinado pode restaurar a verdade.",
    "Esse Arquiteto... é você.",
]

def draw_intro(surf, t):
    titulo_jogo(surf, t)
    panel(surf, 80, 90, W-160, 370, radius=14)

    for i, linha in enumerate(STORY):
        cor = C["gold"] if "Lógica Pura" in linha or "Tabelas Sagradas" in linha else \
              C["azul"] if "Ordem dos" in linha else \
              C["cinza"] if not linha else C["branco"]
        if linha:
            txt(surf, linha, F_TINY, cor, W//2, 115 + i*25)

    # Campo nome
    panel(surf, W//2-200, 430, 400, 42, radius=8)
    txt(surf, "SEU NOME:", F_TINY, C["cinza"], W//2-185, 451, anchor="left")
    cursor = "|" if (t//30)%2==0 else ""
    txt(surf, nome_str + cursor, F_SMALL, C["gold"], W//2-70, 451, anchor="left")

    btn_iniciar.draw(surf)
    txt(surf, "Digite seu nome e pressione ENTER ou clique no botão",
        F_TINY, C["cinza"], W//2, 544)

# ══════════════════════════════════════════════════════
#  TELA: FASE 1
# ══════════════════════════════════════════════════════
btn_v = Btn("V", W//2-110, 390, 100, 60, C["verde_d"], C["verde"])
btn_f = Btn("F", W//2+10,  390, 100, 60, C["verm_d"],  C["verm"])

f1_feedback_timer = 0
f1_feedback_msg   = ""
f1_feedback_ok    = True

def draw_fase1(surf, t):
    idx   = state["f1_idx"]
    pool  = state["f1_pool"]
    pts   = state["f1_pts"]
    vidas = state["f1_vidas"]

    if idx >= len(pool): return

    expr, _ = pool[idx]

    # Cabeçalho
    panel(surf, 20, 14, W-40, 50, radius=10)
    txt(surf, f"⚡ FASE 1 — JULGAMENTO DO ORÁCULO",
        F_MED, C["azul"], W//2, 39)

    # HUD
    panel(surf, 20, 72, W-40, 38, radius=8)
    txt(surf, f"Questão {idx+1}/6", F_TINY, C["branco"], 60, 91, anchor="left")
    barra(surf, 200, 84, 350, 12, idx/6, C["azul_d"], C["azul"])
    txt(surf, coracoes(vidas, 6), F_SMALL, C["verm"], 580, 91, anchor="left")
    txt(surf, f"⚡ {pts} pts", F_SMALL, C["gold"], W-50, 91, anchor="right")

    # Expressão
    panel(surf, 80, 130, W-160, 200, radius=14)
    txt(surf, "AVALIE A EXPRESSÃO", F_TINY, C["cinza"], W//2, 160)
    # Brilho pulsante
    pulse = int(200 + 55*math.sin(t*0.08))
    cor_expr = (pulse, int(pulse*0.8), 0)
    txt(surf, expr, F_EXPR, cor_expr, W//2, 230)

    # Botões V/F
    if not state["f1_lock"] if "f1_lock" in state else True:
        btn_v.draw(surf)
        btn_f.draw(surf)
        txt(surf, "Pressione  V  ou  F  no teclado, ou clique nos botões",
            F_TINY, C["cinza"], W//2, 475)

    # Feedback
    global f1_feedback_timer
    if f1_feedback_timer > 0:
        f1_feedback_timer -= 1
        alpha = min(255, f1_feedback_timer * 8)
        cor = C["verde"] if f1_feedback_ok else C["verm"]
        s = pygame.Surface((500, 50), pygame.SRCALPHA)
        pygame.draw.rect(s, (*C["panel"], alpha), (0,0,500,50), border_radius=10)
        pygame.draw.rect(s, (*cor, alpha), (0,0,500,50), 2, border_radius=10)
        fs = F_SMALL.render(f1_feedback_msg, True, (*cor, alpha))
        s.blit(fs, fs.get_rect(center=(250, 25)))
        surf.blit(s, (W//2-250, 510))

def resposta_f1(resp):
    global f1_feedback_timer, f1_feedback_msg, f1_feedback_ok
    idx   = state["f1_idx"]
    expr, gabarito = state["f1_pool"][idx]
    correto = "V" if gabarito else "F"
    acertou = (resp == correto)

    if acertou:
        state["f1_pts"] += 1
        f1_feedback_ok  = True
        f1_feedback_msg = f"✅  CORRETO!  +1 pt  |  A expressão é {correto}"
        notif.show("✅  Correto! +1 ponto", C["verde"])
    else:
        state["f1_vidas"] -= 1
        f1_feedback_ok  = False
        f1_feedback_msg = f"❌  ERROU!  |  Correto: {correto}  |  {coracoes(state['f1_vidas'], 6)}"
        notif.show("❌  Resposta errada!", C["verm"])

    f1_feedback_timer = 110
    state["f1_idx"]  += 1
    state["f1_lock"]  = True

    # Checar fim
    pygame.time.set_timer(pygame.USEREVENT + 1, 1400)

# ══════════════════════════════════════════════════════
#  TELA: TRANSIÇÃO
# ══════════════════════════════════════════════════════
btn_fase2 = Btn("⚔️  ENTRAR NA FASE 2", W//2-150, 560, 300, 48,
                C["roxo_d"], C["roxo"])

def draw_trans(surf, t):
    panel(surf, 20, 14, W-40, 50, radius=10)
    txt(surf, "◈  TRANSMISSÃO DA ORDEM DOS ARQUITETOS",
        F_MED, C["roxo"], W//2, 39)

    panel(surf, 60, 78, W-120, 260, radius=12)
    nome = state["nome"]
    linhas = [
        (f"Impressionante, {nome}.", C["gold"]),
        ("", C["cinza"]),
        ("Você provou que pode ler as proposições elementares.", C["branco"]),
        ("A Fase 2 exige que você construa as Tabelas Sagradas", C["azul"]),
        ("do zero — e classifique a natureza de cada fórmula.", C["azul"]),
        ("", C["cinza"]),
        (f"Pontuação atual: {state['f1_pts']}/6 pts — máximo possível: 18", C["cinza"]),
    ]
    for i, (l, c) in enumerate(linhas):
        if l:
            txt(surf, l, F_SMALL, c, W//2, 108 + i*30)

    # Legenda
    panel(surf, 60, 350, W-120, 190, radius=12)
    txt(surf, "CLASSIFICAÇÕES DAS FÓRMULAS", F_TINY, C["cinza"], W//2, 372)
    items = [
        ("🟢  T  =  TAUTOLOGIA",   "resultado sempre Verdadeiro",   C["verde"]),
        ("🔴  C  =  CONTRADIÇÃO",  "resultado sempre Falso",         C["verm"]),
        ("🟡  G  =  CONTINGÊNCIA", "mistura de V e F",               C["amar"]),
    ]
    for i, (a, b, c) in enumerate(items):
        y = 400 + i*44
        txt(surf, a, F_SMALL, c, 120, y, anchor="left")
        txt(surf, b, F_TINY, C["cinza"], 120, y+18, anchor="left")

    btn_fase2.draw(surf)

# ══════════════════════════════════════════════════════
#  TELA: FASE 2
# ══════════════════════════════════════════════════════
btn_cls = [
    Btn("T  TAUTOLOGIA",  W//2-310, 490, 190, 44, C["verde_d"], C["verde"], tag="T"),
    Btn("C  CONTRADIÇÃO", W//2-100, 490, 200, 44, C["verm_d"],  C["verm"],  tag="C"),
    Btn("G  CONTINGÊNCIA",W//2+120, 490, 200, 44, (80,70,0),    C["amar"],  tag="G"),
]
btn_proxima = Btn("➤  PRÓXIMA FÓRMULA", W//2-120, 580, 240, 44,
                  C["roxo_d"], C["roxo"])
btn_proxima.disabled = True

# Células da tabela clicáveis
# Linha i → rect da célula resultado
cell_rects = []

def build_cells():
    global cell_rects
    cell_rects = []
    tx, ty = 80, 250
    cw, rh = 220, 34
    for i in range(4):
        cell_rects.append(pygame.Rect(tx + cw*2, ty + 30 + i*rh, cw, rh))

build_cells()

def draw_fase2(surf, t):
    idx   = state["f2_idx"]
    pool  = state["f2_pool"]
    pts   = state["f2_pts"]
    vidas = state["f2_vidas"]

    if idx >= len(pool): return
    form = pool[idx]
    expr = form["expr"]
    cat  = form["cat"]

    # Cabeçalho
    panel(surf, 20, 14, W-40, 50, radius=10)
    txt(surf, "⚔️  FASE 2 — AS TABELAS SAGRADAS",
        F_MED, C["roxo"], W//2, 39)

    # HUD
    panel(surf, 20, 72, W-40, 38, radius=8)
    txt(surf, f"Fórmula {idx+1}/6", F_TINY, C["branco"], 60, 91, anchor="left")
    barra(surf, 200, 84, 350, 12, idx/6, C["roxo_d"], C["roxo"])
    txt(surf, coracoes(vidas, 5), F_SMALL, C["verm"], 580, 91, anchor="left")
    txt(surf, f"⚡ {pts} pts", F_SMALL, C["gold"], W-50, 91, anchor="right")

    # Expressão
    panel(surf, 80, 118, W-160, 72, radius=10)
    txt(surf, "FÓRMULA SAGRADA", F_TINY, C["cinza"], W//2, 138)
    pulse = int(200 + 55*math.sin(t*0.08))
    txt(surf, expr, F_EXPR, (pulse, int(pulse*0.8), 0), W//2, 168)

    # Tabela verdade
    tx, ty = 60, 208
    cw, rh = 220, 34
    heads = ["P", "Q", "Resultado"]
    panel(surf, tx, ty, cw*3+20, 30 + rh*4 + 10, radius=8)

    # Cabeçalhos
    for j, h in enumerate(heads):
        cx = tx + 10 + cw*j + cw//2
        txt(surf, h, F_TINY, C["azul"], cx, ty+15)

    pygame.draw.line(surf, C["border"], (tx, ty+28), (tx+cw*3+20, ty+28))

    lock = state["f2_lock"]
    res  = state["f2_res"]

    for i, (p, q) in enumerate(COMBOS):
        y = ty + 30 + i*rh
        # P
        txt(surf, LABEL[p], F_SMALL, C["verde"] if p else C["verm"],
            tx+10+cw//2, y+rh//2)
        # Q
        txt(surf, LABEL[q], F_SMALL, C["verde"] if q else C["verm"],
            tx+10+cw+cw//2, y+rh//2)
        # Célula resultado
        cr = cell_rects[i]
        hover = cr.collidepoint(pygame.mouse.get_pos()) and not lock
        # fundo da célula
        cor_cell = (0, 60, 30) if hover else C["panel2"]
        pygame.draw.rect(surf, cor_cell, cr, border_radius=4)
        pygame.draw.rect(surf, C["border"], cr, 1, border_radius=4)

        if lock:
            # mostrar gabarito
            correto = form["fn"](p, q)
            correto_str = "V" if correto else "F"
            jogador = res[i]
            acerto  = (jogador == correto_str)
            bg = (0, 60, 30, 80) if acerto else (80, 0, 20, 80)
            s2 = pygame.Surface((cr.w, cr.h), pygame.SRCALPHA)
            pygame.draw.rect(s2, (0,200,80,60) if acerto else (200,0,40,60),
                             (0,0,cr.w,cr.h), border_radius=4)
            surf.blit(s2, cr.topleft)
            label_j = f"{jogador or '—'} → {correto_str}"
            cor_j = C["verde"] if acerto else C["verm"]
            txt(surf, label_j, F_TINY, cor_j, cr.centerx, cr.centery)
        else:
            val = res[i]
            if val is None:
                txt(surf, "—", F_SMALL, C["cinza"], cr.centerx, cr.centery)
            else:
                txt(surf, val, F_SMALL,
                    C["verde"] if val == "V" else C["verm"],
                    cr.centerx, cr.centery)

        pygame.draw.line(surf, C["border"],
                         (tx, y+rh), (tx+cw*3+20, y+rh))

    # Dica
    if not lock:
        txt(surf, "Clique na coluna Resultado para alternar V / F",
            F_TINY, C["cinza"], W//2, ty + 30 + 4*rh + 18)

    # Botões de classificação
    txt(surf, "CLASSIFICAR A FÓRMULA:", F_TINY, C["cinza"], W//2, 474)
    for b in btn_cls:
        b.draw(surf)

    # Feedback
    if state["f2_fb"]:
        panel(surf, 60, 538, W-120, 52, radius=8)
        txt(surf, state["f2_fb"], F_SMALL, state["f2_fb_cor"], W//2, 564)

    # Botão próxima
    if lock:
        btn_proxima.disabled = False
        btn_proxima.draw(surf)
    else:
        btn_proxima.disabled = True

def toggle_cell(i):
    if state["f2_lock"]: return
    cur = state["f2_res"][i]
    nxt = "V" if cur is None else ("F" if cur == "V" else None)
    state["f2_res"][i] = nxt

def classificar(resp_key):
    if state["f2_lock"]: return
    if any(r is None for r in state["f2_res"]):
        notif.show("⚠️  Preencha toda a tabela primeiro!", C["amar"])
        return

    state["f2_lock"] = True
    form = state["f2_pool"][state["f2_idx"]]
    cat  = form["cat"]

    corretos = ["V" if form["fn"](p, q) else "F" for p, q in COMBOS]
    acertos_tab = sum(r == c for r, c in zip(state["f2_res"], corretos))
    tabela_ok   = (acertos_tab == 4)
    classe_ok   = (CAT_MAP[resp_key] == cat)
    ganho = int(tabela_ok) + int(classe_ok)
    state["f2_pts"] += ganho

    if tabela_ok and classe_ok:
        state["f2_fb"]     = f"🏆  PERFEITO! Tabela + Classificação corretas. +2 pts  |  {cat}"
        state["f2_fb_cor"] = C["verde"]
        notif.show("🏆  Perfeito! +2 pontos", C["verde"])
    elif tabela_ok and not classe_ok:
        state["f2_fb"]     = f"✅ Tabela certa  ❌ Classificação errada. +1 pt  |  Correto: {cat}"
        state["f2_fb_cor"] = C["amar"]
        state["f2_vidas"] -= 1
        notif.show("⚠️  Classificação errada! -1 vida", C["amar"])
    elif not tabela_ok and classe_ok:
        state["f2_fb"]     = f"❌ Tabela: {acertos_tab}/4  ✅ Classificação certa. +1 pt"
        state["f2_fb_cor"] = C["amar"]
        state["f2_vidas"] -= 1
        notif.show("⚠️  Tabela incompleta! -1 vida", C["amar"])
    else:
        state["f2_fb"]     = f"❌ Tabela: {acertos_tab}/4  ❌ Classificação errada. +0 pts  |  Correto: {cat}"
        state["f2_fb_cor"] = C["verm"]
        state["f2_vidas"] -= 1
        notif.show("❌  Duplo erro! -1 vida", C["verm"])

    if state["f2_vidas"] <= 0:
        pygame.time.set_timer(pygame.USEREVENT + 2, 1600)

# ══════════════════════════════════════════════════════
#  TELA: RESULTADO FINAL
# ══════════════════════════════════════════════════════
btn_jogar_nov = Btn("🔄  JOGAR NOVAMENTE", W//2-130, 580, 260, 46,
                    C["verde_d"], C["verde"])

def draw_result(surf, t):
    pts1  = state["f1_pts"]
    pts2  = state["f2_pts"]
    total = pts1 + pts2
    maximo = 18
    pct   = total / maximo

    panel(surf, 20, 14, W-40, 50, radius=10)
    txt(surf, "🏁  FIM DA MISSÃO", F_BIG, C["gold"], W//2, 39)

    # Badge de rank
    if total >= 16:
        titulo, cor = "⚜  GRÃO-ARQUITETO  ⚜",   C["gold"]
        historia = f"Você transcendeu a missão, {state['nome']}. A Ordem canta seu nome entre as estrelas!"
    elif total >= 12:
        titulo, cor = "◈  ARQUITETO MESTRE  ◈",  C["azul"]
        historia = f"Impressionante, {state['nome']}! Você domina a lógica. Os mundos respiram aliviados."
    elif total >= 7:
        titulo, cor = "▸  ARQUITETO APRENDIZ", C["cinza"]
        historia = f"Você lutou com coragem, {state['nome']}. A lógica ainda escorrega — mas evolua e retorne."
    else:
        titulo, cor = "☠  INICIANTE CAÓTICO",   C["verm"]
        historia = f"{state['nome']}, todo Grão-Arquiteto começou do zero. Revise as tabelas e tente novamente!"

    panel(surf, 80, 76, W-160, 80, radius=12)
    txt(surf, titulo, F_MED, cor, W//2, 108)
    txt(surf, historia, F_TINY, C["branco"], W//2, 136)

    # Pontuação
    panel(surf, 80, 168, W-160, 130, radius=10)
    txt(surf, f"Fase 1:", F_SMALL, C["cinza"], 130, 198, anchor="left")
    txt(surf, f"{pts1} / 6 pontos", F_SMALL, C["branco"], W-130, 198, anchor="right")
    txt(surf, f"Fase 2:", F_SMALL, C["cinza"], 130, 228, anchor="left")
    txt(surf, f"{pts2} / 12 pontos", F_SMALL, C["branco"], W-130, 228, anchor="right")
    pygame.draw.line(surf, C["border"], (100, 250), (W-100, 250))
    txt(surf, "TOTAL:", F_MED, C["gold"], 130, 278, anchor="left")
    txt(surf, f"{total} / 18  ({int(pct*100)}%)", F_MED, C["gold"], W-130, 278, anchor="right")

    barra(surf, 80, 308, W-160, 14, pct,
          C["roxo_d"], C["gold"], radius=6)

    # Tabela de rank
    panel(surf, 80, 334, W-160, 150, radius=10)
    txt(surf, "TABELA DE RANK", F_TINY, C["cinza"], W//2, 356)
    ranks = [
        ("16 – 18 pts", "⚜  Grão-Arquiteto",   C["gold"]),
        ("12 – 15 pts", "◈  Arquiteto Mestre",   C["azul"]),
        (" 7 – 11 pts", "▸  Arquiteto Aprendiz", C["cinza"]),
        (" 0 –  6 pts", "☠  Iniciante Caótico",  C["verm"]),
    ]
    for i, (pts_str, nome_rank, cr) in enumerate(ranks):
        y = 378 + i*28
        ativo = (
            (total >= 16 and i == 0) or
            (12 <= total <= 15 and i == 1) or
            (7  <= total <= 11 and i == 2) or
            (total <= 6 and i == 3)
        )
        cor_r = cr if ativo else C["cinza"]
        prefix = "► " if ativo else "  "
        txt(surf, prefix + pts_str, F_TINY, cor_r, 130, y, anchor="left")
        txt(surf, nome_rank, F_TINY, cor_r, W-130, y, anchor="right")

    btn_jogar_nov.update(pygame.mouse.get_pos())
    btn_jogar_nov.draw(surf)

# ══════════════════════════════════════════════════════
#  TELA: GAME OVER
# ══════════════════════════════════════════════════════
btn_tentar_nov = Btn("⟳  TENTAR NOVAMENTE", W//2-160, 440, 320, 48,
                     C["roxo_d"], C["roxo"])
btn_inicio     = Btn("⤺  VOLTAR AO INÍCIO", W//2-130, 500, 260, 44,
                     C["verm_d"], C["verm"])
go_msg = ""

def draw_gameover(surf, t):
    panel(surf, 20, 14, W-40, 50, radius=10)
    txt(surf, "💀  GAME OVER", F_BIG, C["verm"], W//2, 39)

    panel(surf, 100, 90, W-200, 320, radius=14)
    txt(surf, go_msg, F_SMALL, C["verm"], W//2, 220)
    txt(surf, "A Ordem dos Arquitetos chora sua derrota.", F_TINY, C["cinza"], W//2, 260)
    txt(surf, "Os mundos caem no caos lógico.", F_TINY, C["cinza"], W//2, 290)
    txt(surf, "Estude os conceitos e retorne.", F_TINY, C["branco"], W//2, 330)

    # Resumo das regras
    panel(surf, 60, 370, W-120, 50, radius=8)
    txt(surf, "¬(nega)  ∧(e)  ∨(ou)  →(se...então)  ↔(sse)",
        F_SMALL, C["azul"], W//2, 395)

    btn_tentar_nov.update(pygame.mouse.get_pos())
    btn_tentar_nov.draw(surf)
    btn_inicio.update(pygame.mouse.get_pos())
    btn_inicio.draw(surf)

# ══════════════════════════════════════════════════════
#  LÓGICA DE TRANSIÇÃO DE ESTADOS
# ══════════════════════════════════════════════════════
def ir_para(tela):
    state["tela"] = tela

def iniciar_jogo():
    state["nome"] = nome_str.strip() or "Arquiteto"
    montar_f1()
    state["f1_lock"] = False
    btn_v.disabled = False
    btn_f.disabled = False
    ir_para("fase1")

def checar_fim_f1():
    pts   = state["f1_pts"]
    vidas = state["f1_vidas"]
    idx   = state["f1_idx"]
    global go_msg

    if vidas <= 0:
        go_msg = f"Sem vidas! {state['nome']} ficou com {pts}/6 pts na Fase 1."
        ir_para("gameover")
    elif idx >= 6:
        if pts < 4:
            go_msg = f"Pontuação insuficiente! {pts}/6 pts. Mínimo: 4."
            ir_para("gameover")
        else:
            ir_para("trans")
    else:
        state["f1_lock"] = False
        btn_v.disabled   = False
        btn_f.disabled   = False

def checar_fim_f2():
    if state["f2_vidas"] <= 0:
        global go_msg
        go_msg = f"Sem vidas na Fase 2! {state['nome']} fez {state['f2_pts']}/12 pts."
        ir_para("gameover")
    else:
        ir_para("result")

# ══════════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ══════════════════════════════════════════════════════
running = True
nome_str = ""

while running:
    t = state["tick"]
    mouse = pygame.mouse.get_pos()

    # Atualizar botões hover
    btn_iniciar.update(mouse)
    btn_v.update(mouse)
    btn_f.update(mouse)
    btn_fase2.update(mouse)
    for b in btn_cls: b.update(mouse)
    btn_proxima.update(mouse)
    btn_jogar_nov.update(mouse)
    btn_tentar_nov.update(mouse)
    btn_inicio.update(mouse)
    notif.update()

    # ── EVENTOS ──────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.USEREVENT + 1:
            # Timer fim de questão F1
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            checar_fim_f1()

        if event.type == pygame.USEREVENT + 2:
            # Timer game over F2
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            checar_fim_f2()

        tela = state["tela"]

        # ── INTRO ──
        if tela == "intro":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    iniciar_jogo()
                elif event.key == pygame.K_BACKSPACE:
                    nome_str = nome_str[:-1]
                else:
                    if len(nome_str) < 24 and event.unicode.isprintable():
                        nome_str += event.unicode
            if btn_iniciar.clicked(event):
                iniciar_jogo()

        # ── FASE 1 ──
        elif tela == "fase1":
            lock = state.get("f1_lock", False)
            if not lock:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        btn_v.disabled = True; btn_f.disabled = True
                        resposta_f1("V")
                    elif event.key == pygame.K_f:
                        btn_v.disabled = True; btn_f.disabled = True
                        resposta_f1("F")
                if btn_v.clicked(event):
                    btn_v.disabled = True; btn_f.disabled = True
                    resposta_f1("V")
                if btn_f.clicked(event):
                    btn_v.disabled = True; btn_f.disabled = True
                    resposta_f1("F")

        # ── TRANSIÇÃO ──
        elif tela == "trans":
            if btn_fase2.clicked(event):
                montar_f2()
                reset_f2_q()
                ir_para("fase2")

        # ── FASE 2 ──
        elif tela == "fase2":
            if not state["f2_lock"]:
                # Clique nas células
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, cr in enumerate(cell_rects):
                        if cr.collidepoint(event.pos):
                            toggle_cell(i)
                # Atalhos teclado para classificar
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        classificar("T")
                    elif event.key == pygame.K_c:
                        classificar("C")
                    elif event.key == pygame.K_g:
                        classificar("G")
                # Botões de classificação
                for b in btn_cls:
                    if b.clicked(event):
                        classificar(b.tag)
            else:
                # Próxima fórmula
                if btn_proxima.clicked(event):
                    state["f2_idx"] += 1
                    if state["f2_idx"] >= 6:
                        ir_para("result")
                    else:
                        reset_f2_q()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if not btn_proxima.disabled:
                        state["f2_idx"] += 1
                        if state["f2_idx"] >= 6:
                            ir_para("result")
                        else:
                            reset_f2_q()

        # ── RESULTADO ──
        elif tela == "result":
            if btn_jogar_nov.clicked(event):
                nome_str = state["nome"]
                ir_para("intro")

        # ── GAME OVER ──
        elif tela == "gameover":
            if btn_tentar_nov.clicked(event):
                montar_f1()
                state["f1_lock"] = False
                btn_v.disabled   = False
                btn_f.disabled   = False
                ir_para("fase1")
            if btn_inicio.clicked(event):
                nome_str = state["nome"]
                ir_para("intro")

    # ── DESENHO ──────────────────────────────────────
    fundo(screen, t)
    tela = state["tela"]

    if tela == "intro":
        draw_intro(screen, t)
    elif tela == "fase1":
        draw_fase1(screen, t)
    elif tela == "trans":
        draw_trans(screen, t)
    elif tela == "fase2":
        draw_fase2(screen, t)
    elif tela == "result":
        draw_result(screen, t)
    elif tela == "gameover":
        draw_gameover(screen, t)

    notif.draw(screen)

    state["tick"] += 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 