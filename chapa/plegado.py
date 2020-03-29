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


def landa(Rit):
    if (Rit > 4):
        x = 0.5
    elif Rit>0.2:
        x = 0.42
    else:
        x = 0.33
    return x

def Rit_min(Rit, r):
    return (1-landa(Rit))/r - 1


def plot_Rit_min(r=0.25, t=2, Ri=5):
    Rit = Ri/t
    if Rit > Rit_min(Rit, r):
        msg = 'Sin riesgo de grietas.'
    else:
        msg = 'Hay riesgo de grietas.'
        
    Rit_ = np.arange(0, 100, 0.1)
    r_ = [(1-landa(i))/(i+1)*100 for i in Rit_]
    
    fig, ax = plt.subplots()
    ax.fill_between(r_, Rit_, y2=100, color='cyan')
    ax.fill_between([67, 100], [0, 0], y2=100, color='cyan')
    ax.plot([r*100, r*100], [0, 100], 'r-')
    ax.plot(r*100, Rit, 'bo')
    ax.text(r*100+1, Rit, msg)
    ax.set_xlabel(r'Reducción de área, $r$ (%)')
    ax.set_ylabel(r'$R_i/t$')
    ax.axis([0, 70, 0, 20])
    plt.show()
    
def Fplegado(tipo, UTS, w, t, D):
    if tipo=='V':
        K = 1.33
    elif tipo=='U':
        K = 0.7
    elif tipo=='R':
        K = 0.33
    return K*UTS*w*t**2/D

def RiRif(Rit, sY, E):
    x = Rit*sY/E
    return 4*x**3 - 3*x + 1

def AfA(Rit, sY, E):
    x = RiRif(Rit, sY, E)
    return (Rit + landa(Rit))/(Rit/x + landa(Rit))


def plot_bending(curvature=0.001, l0=10):
    if curvature == 0:
        curvature = 1e-10
    rho = 1/curvature
    alfa = l0/rho
    alfaG = np.rad2deg(alfa)
    width = rho
    height = rho
    
    fig, ax = plt.subplots(2, 1)
    arc = patches.Arc([0,-height/2], width, height, angle=90, theta1=-alfaG/2, theta2=alfaG/2)
    ax[0].add_patch(arc)
    ax[0].plot([0, rho/2*math.sin(-alfa/2)], [-height/2, -height/2+rho/2*math.cos(-alfa/2)], 'k:')
    ax[0].plot([0, rho/2*math.sin(alfa/2)], [-height/2, -height/2+rho/2*math.cos(alfa/2)], 'k:')
    ax[0].text(0, -0.5, r'$l_0 = %.0f$ mm' % l0, horizontalalignment='center')
    ax[0].text(0, -1, r'$R = %.0f$ mm' % rho, horizontalalignment='center')
    ax[0].text(0, -1.5, r'$\alpha = l_0/R = %.0f^{\circ}$' % alfaG, horizontalalignment='center')
    ax[0].axis([-5, 5, -2, 1])
    ax[0].set_axis_off()   
    ax[0].set_aspect("equal")
    
    x = np.arange(0.000001, 0.25, 0.001)
    yR = [1/i for i in x]
    ya = [np.rad2deg(l0*i) for i in x]
    ax[1].plot(x, yR, 'b-', label='Radio de plegado, $R$ (mm)')
    ax[1].plot(x, ya, 'r-', label=r'Ángulo de plegado, $\alpha$ (°)')
    ax[1].plot([curvature, curvature], [0, 100], 'k--')
    ax[1].set_xlabel(r'Curvatura, $1/R$')
    ax[1].axis([0, 0.25, 0, 100])
    
    plt.legend()
    plt.show()


def plot_sheet_bending(curvature=0.001, l0=10, t=2):
    if curvature == 0:
        curvature = 1e-10
    rho = 1/curvature
    Ri = rho - t/2
    Re = rho + t/2
    alfa = l0/rho
    alfaG = np.rad2deg(alfa)
    
    fig, ax = plt.subplots()
    p0x, p0y = 0, -rho/2
    p1x, p1y = Ri/2*math.sin(-alfa/2), -rho/2+Ri/2*math.cos(-alfa/2)
    p2x, p2y = Re/2*math.sin(-alfa/2), -rho/2+Re/2*math.cos(-alfa/2)
    p3x, p3y = Re/2*math.sin(alfa/2), -rho/2+Re/2*math.cos(alfa/2)
    p4x, p4y = Ri/2*math.sin(alfa/2), -rho/2+Ri/2*math.cos(alfa/2)
    arc = patches.Arc([p0x, p0y], Ri, Ri, angle=90, theta1=-alfaG/2, theta2=alfaG/2)
    ax.add_patch(arc)
    arc = patches.Arc([p0x, p0y], Re, Re, angle=90, theta1=-alfaG/2, theta2=alfaG/2)
    ax.add_patch(arc)
    ax.plot([p0x, p1x], [p0y, p1y], 'k:')
    ax.plot([p1x, p2x], [p1y, p2y], 'k-')
    ax.plot([p4x, p0x], [p4y, p0y], 'k:')
    ax.plot([p3x, p4x], [p3y, p4y], 'k-')
    ax.text(0, -1, r'$l_0 = %.0f$ mm' % l0, horizontalalignment='center')
    ax.text(0, -1.5, r'$R_i = %.0f$ mm, $R_e = %.0f$ mm' % (rho, rho+t), horizontalalignment='center')
    ax.text(0, -2, r'$\alpha = l_0/R = %.0f^{\circ}$' % alfaG, horizontalalignment='center')
    ax.axis([-5, 5, -2, 1])
    ax.set_axis_off()   
    ax.set_aspect("equal")
    plt.show()


def plot_sheet_bending_neutral_axis(tRi=0.001):
    if tRi == 0:
        tRi = 1e-10
    t = 2
    l0 = t/3*math.pi
    Ri = t/tRi
    Rm = Ri + t/2
    Re = Rm + t/2
    Rm = (Ri+Re)/2                  # LM
    Rn = (Ri*Re)**0.5               # LN
#    R0 = ((Ri**2 + Re**2)/2)**0.5   # LM en la chapa sin deformar
    landa = (Rn-Ri)/(Re-Ri)
    alfa = l0/Rm
    alfaG = np.rad2deg(alfa)
    
    fig, ax = plt.subplots(figsize=(20,20))
    p0x, p0y = 0, -Rm/2
    p1x, p1y = Ri/2*math.sin(-alfa/2), -Rm/2+Ri/2*math.cos(-alfa/2)
    p2x, p2y = Re/2*math.sin(-alfa/2), -Rm/2+Re/2*math.cos(-alfa/2)
    p3x, p3y = Re/2*math.sin(alfa/2), -Rm/2+Re/2*math.cos(alfa/2)
    p4x, p4y = Ri/2*math.sin(alfa/2), -Rm/2+Ri/2*math.cos(alfa/2)
    arc = patches.Arc([p0x, p0y], Ri, Ri, angle=90, theta1=-alfaG/2, theta2=alfaG/2)
    ax.add_patch(arc)
    arc = patches.Arc([p0x, p0y], Re, Re, angle=90, theta1=-alfaG/2, theta2=alfaG/2)
    ax.add_patch(arc)
    arc = patches.Arc([p0x, p0y], Rm, Rm, angle=90, theta1=-alfaG/2, theta2=alfaG/2, ls='--')
    ax.add_patch(arc)
    arc = patches.Arc([p0x, p0y], Rn, Rn, angle=90, theta1=-alfaG/2, theta2=alfaG/2, color='red')
    ax.add_patch(arc)
#    arc = patches.Arc([p0x, p0y], R0, R0, angle=90, theta1=-alfaG/2, theta2=alfaG/2, color='blue', ls='--')
#    ax.add_patch(arc)
    ax.plot([p0x, p1x], [p0y, p1y], 'k:')
    ax.plot([p1x, p2x], [p1y, p2y], 'k-')
    ax.plot([p4x, p0x], [p4y, p0y], 'k:')
    ax.plot([p3x, p4x], [p3y, p4y], 'k-')
    ax.text(0, -1, r'$R_i/t = %.1f$' % (Ri/t), horizontalalignment='center')
    ax.text(0, -1.5, r'$\alpha = %.0f^{\circ}$' % alfaG, horizontalalignment='center')
    ax.text(0, -2, r'$\lambda = %.2f$' % landa, horizontalalignment='center')
    ax.axis([-5, 5, -2, 1])
    ax.set_axis_off()   
    ax.set_aspect("equal")
    plt.show()

def plot_RiRif(Ri, t, sY, E):
    Rit = Ri/t
    y0 = RiRif(Rit, sY, E)
    x0 = E/(2*sY) # comienzo de la plastificación
    x = [i/50*x0 for i in range(50)]
    y = [RiRif(i, sY, E) for i in x]
    x1 = [x0 + i/50*1.5*x0 for i in range(50)]
    y1 = [RiRif(i, sY, E) for i in x1]
    
    fig, ax = plt.subplots()
    ax.plot(x, y, 'b-')
    ax.plot(x1, y1, 'b--')
    ax.plot(Rit, y0, 'ro', label=r'$R_i/t=%.3f \rightarrow R_i/R_{if}$ = %0.3f' % (Rit, y0))
    ax.annotate(r'Comienzo de la plastificación: $R_i/t=%.0f$' % x0, horizontalalignment='center', xy=(x0, 0), xytext=(x0, 0.5), arrowprops=dict(arrowstyle="->"))
    ax.set_xlabel(r'Relación entre el radio de plegado y el espesor, $R_i/t$')
    ax.set_ylabel(r'Relación de radios tras la RE, $R_i/R_{if}$')      
    ax.axis([0, 1.5*x0, 0, 1])
    plt.legend(title=r'$\frac{R_i}{R_{if}} = 4 \left( \frac{R_i}{t}\frac{\sigma_Y}{E} \right)^3 - 3 \left( \frac{R_i}{t}\frac{\sigma_Y}{E} \right) + 1$')
    plt.show()

def plot_bending_RiRif(curvatura, t, l, sY, E):
    Ri = 1/curvatura
    Rit = Ri/t
    y0 = RiRif(Rit, sY, E)
    x0 = E/(2*sY) # comienzo de la plastificación
    x = [i/50*x0 for i in range(50)]
    y = [RiRif(i, sY, E) for i in x]
    x1 = [x0 + i/50*1.5*x0 for i in range(50)]
    y1 = [RiRif(i, sY, E) for i in x1]

#    l = Ri*np.deg2rad(alfa)
    alfa = np.rad2deg(l/Ri)
    alfaR = np.deg2rad(alfa)
    width = Ri
    height = Ri
    
    af = AfA(Rit, sY, E)*alfa
    afR = np.deg2rad(af)
    Rif = Ri/y0
#    lf = Rif*np.deg2rad(af)
    wf = Rif
    hf = Rif
    
    fig, ax = plt.subplots(2, 1)
    arc = patches.Arc([0,-height/2], width, height, angle=90, theta1=-alfa/2, theta2=alfa/2)
    ax[0].add_patch(arc)
    ax[0].plot([0, Ri/2*math.sin(-alfaR/2)], [-height/2, -height/2+Ri/2*math.cos(-alfaR/2)], 'k:')
    ax[0].plot([0, Ri/2*math.sin(alfaR/2)], [-height/2, -height/2+Ri/2*math.cos(alfaR/2)], 'k:')
    arc = patches.Arc([0,-hf/2], wf, hf, angle=90, theta1=-af/2, theta2=af/2, ls='--', color='r')
    ax[0].add_patch(arc)
    ax[0].plot([0, Rif/2*math.sin(-afR/2)], [-hf/2, -hf/2+Rif/2*math.cos(-afR/2)], 'r:')
    ax[0].plot([0, Rif/2*math.sin(afR/2)], [-hf/2, -hf/2+Rif/2*math.cos(afR/2)], 'r:')
    ax[0].text(0, -0.5, r'$\alpha = %.1f^{\circ}$' % alfa, horizontalalignment='center')
    ax[0].text(0, -1, r'$\alpha_f = %.1f^{\circ}$' % af, horizontalalignment='center', color='r')
    ax[0].text(0, -1.5, r'$R_i = %.1f$ mm' % Ri, horizontalalignment='center')
    ax[0].text(0, -2, r'$R_{if} = %.1f$ mm' % Rif, horizontalalignment='center', color='r')
    ax[0].axis([-5, 5, -2, 1])
    ax[0].set_axis_off()   
    ax[0].set_aspect("equal")
    
    ax[1].plot(x, y, 'b-')
    ax[1].plot(x1, y1, 'b--')
    ax[1].plot(Rit, y0, 'ro', label=r'$R_i/t=%.3f \rightarrow R_i/R_{if}$ = %0.3f' % (Rit, y0))
    ax[1].annotate(r'Comienzo de la plastificación: $R_i/t=%.0f$' % x0, horizontalalignment='center', xy=(x0, 0), xytext=(x0, 0.5), arrowprops=dict(arrowstyle="->"))
    ax[1].set_xlabel(r'Radio de plegado, $R_i$')
    ax[1].set_ylabel(r'$R_i/R_{if}$')      
    ax[1].axis([0, 1.5*x0, 0, 1])
#    ax[1].set_axis_off()
#    ax[1].set_aspect("equal")
#    plt.legend(title=r'$\frac{R_i}{R_{if}} = 4 \left( \frac{R_i}{t}\frac{\sigma_Y}{E} \right)^3 - 3 \left( \frac{R_i}{t}\frac{\sigma_Y}{E} \right) + 1$')
    plt.show()

def print_solution(exercise):
    if exercise==1:
        t = 1
        w = 10
        UTS = 500
        Dv = 50
        Du = 102
        Dr = 11.1
        Fv = Fplegado('V', UTS, w, t, Dv) # función definida en plegado.py
        Fu = Fplegado('U', UTS, w, t, Du)
        Fr = Fplegado('R', UTS, w, t, Dr)

        display(Markdown(r'A igualdad de parámetros $UTS$, $t$, $w$ y $D$, el plegado en V requiriría una fuerza mayor por ser $K=1.33$ el mayor de los coeficientes. Sin embargo, $D$ es diferente en cada caso: '))
        display(Markdown(r'- Plegado en V: $D_V = 50$ mm.'))
        display(Markdown(r'- En el plegado en U, la abertura de la matriz se supone que será el diámetro del punzón más 2 veces el espesor de la chapa: $D_U = 2 \times (50 + 1) = 102$ mm.'))
        display(Markdown(r'- En el rebordeado: $D_R = 5 + 1.1 + 5 = 11.1$ mm.'))
        display(Markdown(r'A menor abertura $D$, mayor fuerza de plegado $F$. Como el valor de $D$ es pequeño en el rebordeado, puede que la fuerza necesaria sea superior a la del plegado en V. Realizando los cálculos para comprobarlo:'))
        display(Markdown(r'- Plegado en V: F = %.0f N' % Fv))
        display(Markdown(r'- Plegado en U: F = %.0f N' % Fu))
        display(Markdown(r'- Rebordeado: F = %.0f N' % Fr))
        display(Markdown(r'Por tanto, la fuerza es mayor en el rebordeado.'))
    if exercise==2:
        display(Image(filename='Ejemplo02.png'))
        display(Math(r'\text{El plegado de chapa es debido a la acción de un momento flector }M'))
        display(Math(r'\text{En plegado en V y en U: }M = \frac{F}{2}\frac{D}{2} + \frac{F}{2}\frac{D}{2} = \frac{F\,D}{2} \qquad \rightarrow \qquad F = \frac{M}{D/2}'))
        display(Math(r'\text{En rebordeado: }M = F\,D  \qquad \rightarrow \qquad F = \frac{M}{D}'))
        display(Math(r'\text{Note que el flector será muy similar en el plegado en V y en el rebordeado porque ambos doblan la chapa a 90°}'))
        display(Math(r'\text{La fuerza ha sido mayor en el rebordeado fundamentalmente por tener un valor relativo muy pequeño de }D'))
    if exercise==6:
        display(Markdown(r'Con $R_i=1$ mm: $R_i/t=0.5 \quad \rightarrow \quad \lambda = 0.42 \qquad \rightarrow \qquad l_0 = 10 + \frac{\pi}{2}(1+0.42 \cdot 2) + 10 = 22.89$ mm'))
        display(Markdown(r'Con $R_i=10$ mm: $R_i/t=5 \quad \rightarrow \quad \lambda = 0.5 \qquad \rightarrow \qquad l_0 = 10 + \frac{\pi}{2}(10+0.5 \cdot 2) + 10 = 37.28$ mm'))
        display(Markdown(r'Las líneas rojas en la figura represental la LN en cada caso.'))
        display(Markdown(r'Suponiendo $\lambda = 0.5$, la longitud sería $l_0 = 23.14$ mm, con un error de 0.25 mm.'))
    if math.floor(exercise)==8:
        E = 210e3
        sY = 210
        t = 1
        Ri = 100
        RRif = RiRif(Ri/t, sY, E)
        Rif = Ri/RRif
        Rite = E/(2*sY)
    if exercise==8.1:
        display(Markdown(r'El material tiene una relación $\frac{\sigma_Y}{E} = %0.3f$.' % (sY/E)))
        display(Markdown(r'$\frac{R_i}{t}=%0.1f \qquad \rightarrow \qquad \frac{R_i}{R_{if}}=%0.3f \qquad \rightarrow \qquad R_{if}=%0.3f$ mm' % (Ri/t, RRif, Rif)))
        display(Markdown(r'NOTA: recuerde del ejemplo 3 que aunque parezca que el radio se recupera mucho, un $%0.0f$%%, el efecto en el ángulo de plegado es relativamente pequeño.' % ((Rif-Ri)/Ri*100)))
        display(plot_RiRif(Ri, t, sY, E))
    if exercise==8.2:
        display(Markdown(r'$\frac{R_i}{t} = \frac{E}{2 \sigma_y} = %0.3f \qquad \rightarrow \qquad \frac{R_i}{R_{if}}=0 \qquad \rightarrow \qquad R_{if}=\infty$ mm' % Rite))
        display(Markdown(r'La recuperación elástica es completa, la chapa recupera su forma plana original.'))
    if exercise==8.3:
        display(Markdown(r'Si el plegado no es suficiente para producir deformación plástica, la chapa recupera su forma plana original. En esta situación no tiene sentido usar la función.'))
    if exercise==8.4:
        display(Markdown(r'Mayor valor de recuperación elástica: $\frac{R_i}{R_{if}}=0 \qquad \rightarrow \qquad$ la chapa se recupera totalmente.'))
        display(Markdown(r'Menor valor de recuperación elástica: $\frac{R_i}{R_{if}}=1$ cuando $R_i=0$ (plegado completo) $\qquad \rightarrow \qquad$ la chapa no se recupera en absoluto.'))
    if math.floor(exercise)==9:
        w = 40
        t = 1.6
        E = 75e3
        sY = 180
        UTS = 220
        r = 0.15
        D = 20        
        Rp = 5        
    if exercise==9.1:
        display(Markdown(r'Los datos del problema son los siguientes:'))
        display(Markdown(r'$w = 40$ mm'))
        display(Markdown(r'$t = 1.6$ mm'))
        display(Markdown(r'$E = 75 \cdot 10^3$ MPa'))
        display(Markdown(r'$\sigma_Y = 180$ MPa'))
        display(Markdown(r'$U\!T\!S = 220$ MPa'))
        display(Markdown(r'$r = 0.15$'))
        display(Markdown(r'$D = 20$ mm'))
        display(Markdown(r'#### Selección del punzón de plegado'))
        display(Markdown(r'Suponiendo $\lambda=0.5$, una primera estimación del radio mínimo de plegado para este material es:'))
        display(Markdown(r'- $\frac{R_i}{t} > \frac{1-0.5}{0.15} - 1 = 2.33$'))
        display(Markdown(r'Esta estimación permite ajustar mejor un valor de $\lambda=0.42$. El radio mínimo de plegado es:'))
        display(Markdown(r'- $\frac{R_i}{t} > \frac{1-0.42}{0.15} - 1 = 2.86 \qquad \rightarrow \qquad R_{i,\min} = 4.59$ mm.'))
        display(Markdown(r'El único punzón que no cumple la condición es el más pequeño. Por tanto, se elige el punzón de radio 5 mm.'))
        display(Markdown(r'- $R_i = R_p = %s$ mm --> $R_i/t = %.2f$' % (Rp, Rp/t)))
        display(plot_Rit_min(r, t, Rp))
    if exercise==9.2:
        tipo = 'V'
        K = 1.33
        display(Markdown(r'#### Fuerza de doblado'))
        display(Markdown(r'Se calcula usando la ecuación correspondiente.'))
        display(Markdown(r'- $F = %s \cdot %s \frac{%s \cdot %s^2}{%s} = %0.0f$ N' % (K, UTS, w, t, D, Fplegado(tipo, UTS, w, t, D))))
    if exercise==9.3:
        display(Markdown(r'#### Recuperación elástica'))
        display(Markdown(r'Se calcula usando la ecuación correspondiente.'))
        RRif = RiRif(Rp/t, sY, E)
        Rif = Rp/RRif
        display(Markdown(r'- $\phi = \frac{R_i}{t}\frac{\sigma_Y}{E} = %0.2f \times 10^{-3} \qquad \rightarrow \qquad \frac{R_i}{R_{if}} = 4 \phi^3 - 3 \phi + 1 = %0.3f \qquad \rightarrow \qquad Rif = %0.3f$ mm' % (sY/E*Rp/t*1000, RRif, Rif)))
        display(Markdown(r'La ecuación para la recuperación elástica puede analizarse representándola en la gráfica siguiente:'))
        display(plot_RiRif(Rp, t, sY, E))
        display(Markdown(r'Como puede observarse, la curva solo es válida cuando el material ha plastificado (tramo continuo de la curva), es decir, para valores de $R_i$ inferiores al señalado como "comienzo de la plastificación". El tramo discontinuo de la curva corresponde a $R_i$ grandes, en los que aún no se ha producido plastificación.'))
        display(Markdown(r'Observe que para curvaturas pequeñas ($R_i$ grandes), la chapa prácticamente recupera su forma original. Conforme se pliega la chapa (se reduce $R_i$) la recuperación cada vez es menor. El valor calculado de recuperación elástica se representa en la figura con un círculo rojo.'))
        display(Markdown(r'La siguiente simulación interactiva permite analizar cómo se deforma la chapa y su correspondiente forma recuperada para distintos grados de plegado. Use el botón deslizante para cambiar la curvatura de la chapa.'))
        
if __name__ == "__main__":
    Ri=5
    curvature = 1/Ri
    t=1
    sY=100
    E=70e3
    l=10
    plot_Rit_min()
    plot_bending(curvature)
    plot_sheet_bending(curvature)
    plot_sheet_bending_neutral_axis(0.157)
    plot_RiRif(Ri, t, sY, E)
    plot_bending_RiRif(1/Ri, t, l, sY, E)
    