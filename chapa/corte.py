#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Domingo Morales Palma <dmpalma@us.es>
"""

import math
from IPython.display import Image, Math, Markdown, display
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

plt.rcParams["figure.figsize"] = (8, 6)


    
def Fcorte(K1, UTS, t, L, alfa):
    tgA = math.tan(math.radians(alfa))
    if tgA < t/L:
        return K1*UTS*t*L
    else:
        return K1*UTS*t**2/tgA

def Wcorte(K1, K2, UTS, t, L):
    return K1*K2*UTS*t**2*L /1000

def plot_Fcorte(K1=0.7, UTS=200, t=1, L=10, alfa=0):
    Fmax = Fcorte(K1, UTS, t, L, 0)
    Fc = Fcorte(K1, UTS, t, L, alfa)
    alfaC = math.degrees(math.atan(t/L))
    
    a = np.arange(0, 60, 0.1)
    F = [Fcorte(K1, UTS, t, L, i) for i in a]
    
    fig, ax = plt.subplots()
    ax.plot(a, F, 'b-')
    ax.plot([alfaC, alfaC], [0, Fmax], 'k:', label=r'$\tan \alpha = t/L \rightarrow \alpha=%0.1f°$' % alfaC)
    ax.text(alfaC, 10, '%.1f°' % alfaC)
    ax.plot(alfa, Fc, 'ro', label=r'$\alpha=%s° \rightarrow F=%0.0f$ N' % (alfa, Fc))
    ax.text(alfa+1, Fc, '%.0f N' % Fc)
    ax.set_xlabel(r'Ángulo de corte, $\alpha$ (°)')
    ax.set_ylabel(r'Fuerza de corte $F$ (N)')
    ax.axis([0, 30, 0, Fmax+100])
    plt.legend()
    plt.show()

def print_solution(exercise):
    if exercise==1:
        K1=0.7
        UTS=220
        t=1.6
        L=50
        alfa=10
        F = Fcorte(K1, UTS, t, L, alfa)
        Fmax = Fcorte(K1, UTS, t, L, 0)

        display(plot_Fcorte(K1, UTS, t, L, alfa))
        display(Markdown(r'Note que para un ángulo demasiado pequeño ($\tan \alpha < t/L$) la cizalla se puede considerar como plana.'))
        display(Markdown(r'$\alpha=0 \qquad \rightarrow \qquad F_\max = %.0f$ N' % Fmax))
        display(Markdown(r'$\alpha=%s \qquad \rightarrow \qquad F = %.0f$ N' % (alfa, F)))
        display(Markdown(r'La reducción de fuerza es del %.0f%%.' % ((Fmax-F)/Fmax*100)))
    if math.floor(exercise)==2:
        K1=0.7
        K2=0.5
        UTS=330
        t=2
        alfa=0
        Fprensa=500e3 # N
        Npiezas=500000
        rend=0.8
        
        L1 = 25 + 2*(11 + (38**2 + 7.5**2)**0.5) + math.pi*5
        L2 = math.pi*5
        L = L1 + 3*L2
        
        F = Fcorte(K1, UTS, t, L, alfa)
        W = Wcorte(K1, K2, UTS, t, L)
        WT = Npiezas*W
        Ee = WT/rend
        
    if exercise==2.1:
        display(Image(filename='matriz compuesta x1.png'))
        display(Markdown(r'Contorno exterior: $L_1 = %0.1f$ mm' % L1))
        display(Markdown(r'Contorno interior de una agujero: $L_2 = %0.1f$ mm' % L2))
        display(Markdown(r'Total contornos a cortar: $L = L_1 + 3 L_2 = %0.1f$ mm' % L))
        display(Markdown(r'Fuerza para cortar una pieza: $F = %.0f$ N = %.1f kN' % (F, F/1000)))
    if exercise==2.2:
        display(Markdown(r'Hay 2 limitaciones, en la fuerza de corte y en las dimensiones máximas de la matriz.'))
        display(Markdown(r'Por capacidad de la prensa: $n = \frac{F_{prensa}}{F} = %0.1f \qquad \rightarrow \qquad %.0f$ piezas' % (Fprensa/F, math.floor(Fprensa/F))))
        display(Markdown(r'Por dimensiones de la matriz, $80 \times 80$ mm:'))
        display(Markdown(r'- En anchura no hay problema: el material de partida tiene 58 mm y la pieza final 54 mm.'))
        display(Markdown(r'- En longitud, cada pieza tiene 25 mm y hay 2 mm de separación entre piezas. Por tanto, como máximo se pueden cortar 3 piezas de forma simultánea: 25 + 2 + 25 + 2 + 25 = 79 < 80 mm.'))
        display(Markdown(r'La mayor limitación es la geométrica. El máximo es de 3 piezas.'))
        display(Image(filename='matriz compuesta x3.png'))
    if exercise==2.3:
        display(Markdown(r'Trabajo de una pieza: $W = K_2 \cdot F \cdot t = %.1f$ J' %( W)))
        display(Markdown(r'Trabajo del total de piezas: $%s \times %0.1f = %0.1f$ MJ' % (Npiezas, W, WT/1e6)))
        display(Markdown(r'Energía eléctrica necesaria: $\frac{%0.1f}{%s} = %0.1f$ MJ $= %0.0f$ kW$\cdot$h' % (WT/1e6, rend, Ee/1e6, Ee/(1000*3600))))
        display(Markdown(r''))
        display(Markdown(r''))
        display(Markdown(r''))
        
if __name__ == "__main__":
    K1=0.7
    UTS=200
    t=1
    L=10
    alfa=20
    plot_Fcorte(K1, UTS, t, L, alfa)