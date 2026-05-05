# -*- coding: utf-8 -*-

import random
import time
import sys
import os
from colorama import init, Fore, Style

init(autoreset=True)

# ══════════════════════════════════════════════════

# CORES

# ══════════════════════════════════════════════════

R=Style.RESET_ALL; B=Style.BRIGHT; D=Style.DIM
ROXO=Fore.MAGENTA+B; AZUL=Fore.CYAN+B; VERDE=Fore.GREEN+B
VERM=Fore.RED+B; AMAR=Fore.YELLOW+B; BRAN=Fore.WHITE+B
CINZA=Fore.WHITE+D; GOLD=Fore.YELLOW+B; CYAN=Fore.CYAN

# ══════════════════════════════════════════════════

# UTIL

# ══════════════════════════════════════════════════

def limpar(): os.system('cls' if os.name=='nt' else 'clear')
def pausar(t=0.6): time.sleep(t)
def linha(c="─",n=60,cor=AZUL): print(cor+c*n+R)
def coracoes(v,m): return "❤️ "*v+"🖤 "*(m-v)

def pedir_vf(msg="V/F: "):
while True:
r=input(msg).upper()
if r in ["V","F"]: return r

def pedir_tcg():
while True:
r=input("T/C/G: ").upper()
if r in ["T","C","G"]: return r

# ══════════════════════════════════════════════════

# FASE 1

# ══════════════════════════════════════════════════

FASE1_POOL=[
("¬V",False),("¬F",True),
("V ∧ V",True),("V ∧ F",False),
("V ∨ F",True),("F ∨ F",False),
("V → F",False),("F → V",True),
("V ↔ F",False),("V ↔ V",True)
]

# ══════════════════════════════════════════════════

# 🔥 FASE 2 CORRIGIDA

# ══════════════════════════════════════════════════

FASE2_POOL=[

("(P ∧ Q) → P",lambda p,q:(not(p and q)) or p,"Tautologia"),
("(P ∧ Q) → Q",lambda p,q:(not(p and q)) or q,"Tautologia"),
("P → (Q → P)",lambda p,q:(not p) or ((not q) or p),"Tautologia"),
("(P → Q) ∨ (Q → P)",lambda p,q:((not p) or q) or ((not q) or p),"Tautologia"),

("(P → Q) ∧ P ∧ ¬Q",lambda p,q:((not p) or q) and p and (not q),"Contradição"),
("(P ∨ Q) ∧ ¬P ∧ ¬Q",lambda p,q:(p or q) and (not p) and (not q),"Contradição"),

("P ∧ Q",lambda p,q:p and q,"Contingência"),
("P ∨ Q",lambda p,q:p or q,"Contingência"),
("P → Q",lambda p,q:(not p) or q,"Contingência"),
("P ↔ Q",lambda p,q:p==q,"Contingência"),
("¬(P ∧ Q)",lambda p,q:not(p and q),"Contingência"),
("¬(P ∨ Q)",lambda p,q:not(p or q),"Contingência"),
]

COMBOS=[(True,True),(True,False),(False,True),(False,False)]
CAT={"T":"Tautologia","C":"Contradição","G":"Contingência"}

# ══════════════════════════════════════════════════

# FASE 1

# ══════════════════════════════════════════════════

def fase1():
pts=0; vidas=5
quest=random.sample(FASE1_POOL,5)

```
for i,(exp,resp) in enumerate(quest):
    limpar()
    print(f"Questão {i+1}  {coracoes(vidas,5)}")
    print("Expressão:",exp)
    r=pedir_vf()

    if (r=="V")==resp:
        print(VERDE+"Correto!"+R); pts+=1
    else:
        print(VERM+"Errado!"+R); vidas-=1

    pausar(1)

    if vidas==0: return pts,False

return pts,pts>=3
```

# ══════════════════════════════════════════════════

# FASE 2

# ══════════════════════════════════════════════════

def fase2():
pts=0; vidas=4
quest=random.sample(FASE2_POOL,5)

```
for i,(nome,fn,cat) in enumerate(quest):
    limpar()
    print(f"Fórmula {i+1}  {coracoes(vidas,4)}")
    print(nome,"\n")

    resp_user=[]; resp_ok=[]

    for p,q in COMBOS:
        correto="V" if fn(p,q) else "F"
        resp_ok.append(correto)
        r=pedir_vf(f"P={p} Q={q}: ")
        resp_user.append(r)

    acertos=sum(a==b for a,b in zip(resp_user,resp_ok))

    classe=pedir_tcg()
    classe_ok=(CAT[classe]==cat)

    ganho=0
    if acertos==4: ganho+=1
    if classe_ok: ganho+=1

    pts+=ganho
    if ganho<2: vidas-=1

    print("Correto:",cat)
    pausar(1.5)

    if vidas==0: break

return pts
```

# ══════════════════════════════════════════════════

# MAIN

# ══════════════════════════════════════════════════

def main():
while True:
limpar()
nome=input("Seu nome: ")

```
    pts1,passou=fase1()

    if not passou:
        print("Game Over")
        continue

    pts2=fase2()

    total=pts1+pts2
    print(f"\n{nome}, sua pontuação: {total}/10")

    if input("Jogar novamente? s/n ").lower()!="s":
        break
```

if **name**=="**main**":
main()
