#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Domingo Morales Palma <dmpalma@us.es>
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines


plt.rcParams["figure.figsize"] = (16, 6)

def delta(mu):
    return math.degrees(math.atan(mu))

def phi(mu, gamma):
    g = math.radians(gamma)
    d = math.radians(delta(mu))
    f = math.pi/4 + (g - d)/2
    return math.degrees(f)

def xi(mu, gamma):
    g = math.radians(gamma)
    f = math.radians(phi(mu, gamma))
    return math.cos(f-g)/math.sin(f)

def h2(h1, mu, gamma):
    return h1*xi(mu, gamma)

def plot_delta():
    m = np.arange(0, 0.5, 0.01)
    d = [delta(i) for i in m]
    
    fig, ax = plt.subplots()
    ax.plot(m, d, 'b-')
    ax.set_xlabel(r'Coeficiente de fricción, $\mu$')
    ax.set_ylabel(r'Ángulo $\delta$ (°)')
    ax.axis([0, 0.5, 0, 30])
    plt.show()

def plot_phi(mu):
    g = np.arange(-20, 50, 0.1)
    f = [phi(mu, i) for i in g]
    
    fig, ax = plt.subplots()
    ax.plot(g, f, 'b-')
    ax.set_xlabel(r'Ángulo de desprendimiento, $\gamma$ (°)')
    ax.set_ylabel(r'Ángulo de deslizamiento, $\phi$ (°)')
    ax.axis([-20, 50, 30, 70])
    plt.show()

def plot_xi(mu):
    g = np.arange(-20, 50, 0.1)
    h = [xi(mu, i) for i in g]
    
    fig, ax = plt.subplots()
    ax.plot(g, h, 'g-')
    ax.set_xlabel(r'Ángulo de desprendimiento, $\gamma$ (°)')
    ax.set_ylabel(r'Factor de recalcado, $\xi = h_2/h_1$')
    ax.axis([-20, 50, 1, 1.2])
    plt.show()
    
def plot_corte_ortogonal_alone(h1, mu, gamma):
    h2_ = h2(h1, mu, gamma)
    alpha = 3 # ángulo de incidencia
    beta = 90 - (alpha + gamma) # ángulo de filo
    phi_ = phi(mu, gamma)
    
    a = math.radians(alpha)
    g = math.radians(gamma)
    f = math.radians(phi_)
    
    mat = 5 # longitud de material sin mecanizar
    H = 1 # grosor de material mecanizado
    m1 = [-mat, h1]
    m2 = [-h1/math.tan(f), h1]
    sup = 3 # longitud de superficie mecanizada
    s1 = [0, 0]
    s2 = [sup, 0]
    vir = 2 # longitud de viruta
    v1 = [m2[0] + vir*math.sin(g), m2[1] + vir*math.cos(g)]
    v2 = [s1[0] + vir*math.sin(g), s1[1] + vir*math.cos(g)]
    des = 3 # longitud de la cara de desprendimiento
    inc = 3 # longitud de la cara de incidencia
    t2 = s1
    t1 = [t2[0] + des*math.sin(g), t2[1] + des*math.cos(g)]
    t3 = [s1[0] + inc*math.cos(a), s1[1] + inc*math.sin(a)]
        
    fig, ax = plt.subplots(figsize=(16, 6))
    
    ax.fill_between(*zip(*(m1, m2, v1, t1, s1, s2)), y2=-H, color='lightcoral')
    ax.add_line(lines.Line2D(*zip(*(m2, s1)), color='w', ls='--'))
    
    ax.fill(*zip(*(t1, t2, t3, t1)), color='lightgray')
    ax.add_line(lines.Line2D(*zip(*(t1, t2, t3)), color='k', lw=3))
    
    ax.add_line(lines.Line2D(*zip(*(t2, [t2[0], t2[1]+vir])), color='k'))
    ax.add_line(lines.Line2D(*zip(*(t2, [t2[0]-1, t2[1]])), color='k'))
    
    ax.text(t2[0]+sup, t2[1], r'$\alpha=%.0f$°' % alpha)
    ax.text(t2[0]+0.5, t2[1]+0.2, r'$\beta=%.0f$°' % beta)
    ax.text(t2[0]+t1[0]/2, t2[1]+vir, r'$\gamma=%.0f$°' % gamma, horizontalalignment='center')
    ax.text((m2[0]+t2[0])/2-0.2, (m2[1]+t2[1])/2, r'$\phi=%.0f$°' % phi_, horizontalalignment='right')
    ax.text(m1[0], (m2[1]+t2[1])/2, r'$h_1=%.2f$ mm' % h1)
    ax.text(v1[0], v1[1], r'$h_2=%.2f$ mm' % h2_)
    
    ax.axis([-mat, sup, -H, h1+vir])
    ax.set_aspect("equal")
    plt.axis('off')
    plt.show()

def plot_corte_ortogonal(h1, mu, gamma, alpha):
    h2_ = h2(h1, mu, gamma)
    beta = 90 - (alpha + gamma) # ángulo de filo
    phi_ = phi(mu, gamma)
    xi_ = xi(mu, gamma)
    
    a = math.radians(alpha) # ángulo de incidencia
    g = math.radians(gamma) # ángulo de desprendimiento
    f = math.radians(phi_)  # ángulo de deslizamiento
    
    mat = 3 # longitud de material sin mecanizar
    H = 1 # grosor de material mecanizado
    m1 = [-mat, h1]
    m2 = [-h1/math.tan(f), h1]
    sup = 3 # longitud de superficie mecanizada
    s1 = [0, 0]
    s2 = [sup, 0]
    vir = 2 # longitud de viruta
    v1 = [m2[0] + vir*math.sin(g), m2[1] + vir*math.cos(g)]
    v2 = [s1[0] + vir*math.sin(g), s1[1] + vir*math.cos(g)]
    des = 3 # longitud de la cara de desprendimiento
    inc = 3 # longitud de la cara de incidencia
    t2 = s1
    t1 = [t2[0] + des*math.sin(g), t2[1] + des*math.cos(g)]
    t3 = [s1[0] + inc*math.cos(a), s1[1] + inc*math.sin(a)]
        
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    ax[0].fill_between(*zip(*(m1, m2, v1, t1, s1, s2)), y2=-H, color='lightcoral')
    ax[0].add_line(lines.Line2D(*zip(*(m2, s1)), color='w', ls='--'))
    
    ax[0].fill(*zip(*(t1, t2, t3, t1)), color='lightgray')
    ax[0].add_line(lines.Line2D(*zip(*(t1, t2, t3)), color='k', lw=3))
    
    ax[0].add_line(lines.Line2D(*zip(*(t2, [t2[0], t2[1]+vir])), color='k'))
    ax[0].add_line(lines.Line2D(*zip(*(t2, [t2[0]-1, t2[1]])), color='k'))
    
    ax[0].text(t2[0]+sup, t2[1], r'$\alpha=%.0f$°' % alpha)
    ax[0].text(t2[0]+0.5, t2[1]+0.2, r'$\beta=%.0f$°' % beta)
    ax[0].text(t2[0]+t1[0]/2, t2[1]+vir, r'$\gamma=%.0f$°' % gamma, horizontalalignment='center')
    ax[0].text((m2[0]+t2[0])/2-0.2, (m2[1]+t2[1])/2, r'$\phi=%.0f$°' % phi_, horizontalalignment='right')
    ax[0].text(m1[0], (m2[1]+t2[1])/2, r'$h_1=%.2f$ mm' % h1)
    ax[0].text(v1[0], v1[1], r'$h_2=%.2f$ mm' % h2_)
    
    ax[0].axis([-mat, sup, -H, h1+vir])
    ax[0].set_aspect("equal")
    ax[0].axis('off')
    
        
    g_ = np.arange(-20, 50, 0.1)
    f_ = [phi(mu, i) for i in g_]
    
    ax[1].plot(g_, f_, 'b-')
    ax[1].plot([gamma, gamma], [0, 100], 'k--')
    ax[1].plot(gamma, phi_, 'bo')
    ax[1].set_xlabel(r'Ángulo de desprendimiento, $\gamma$ (°)')
    ax[1].set_ylabel(r'Ángulo de deslizamiento, $\phi$ (°)')
    ax[1].yaxis.label.set_color('blue')
    ax[1].tick_params(axis='y', colors='blue')
    ax[1].axis([-20, 50, 0, 80])
    
    x = [xi(mu, i) for i in g_]
    par2 = ax[1].twinx()
    par2.plot(g_, x, 'r--')
    par2.plot(gamma, xi_, 'ro')
    par2.set_xlabel(r'Ángulo de desprendimiento, $\gamma$ (°)')
    par2.set_ylabel(r'Factor de recalcado, $\xi = h_2/h_1$')
    par2.yaxis.label.set_color('red')
    par2.tick_params(axis='y', colors='red')
    par2.axis([-20, 50, 1, 2])
    
    plt.show()
    
if __name__ == "__main__":
    h1 = 1
    mu = 0.
    g = 20
    a = 3

    plot_delta()
    plot_phi(mu)
    plot_xi(mu)
    plot_corte_ortogonal(h1, mu, g, a)
    
    print('mu = %s --> delta = %0.2f°' % (mu, delta(mu)))
    print('gamma = %s° --> phi = %0.2f°' % (g, phi(mu, g)))
    print('h1 = %s mm --> h2=%0.2f mm' % (h1, h2(h1, mu, g)))
