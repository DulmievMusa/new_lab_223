import pandas as pd
import numpy as np
from math import sqrt
from math import log
import math

import matplotlib.pyplot as plt
from funcs import *
from mnk import *

spp = []

def paint_graph_RQ(number, to_paint):
    linear_data = pd.read_csv(f'data/{number}0.csv')
    i_es, u_es = list(linear_data['I']), list(linear_data['U'])
    n = len(i_es)


    q_es = [(u_es[i] * i_es[i]) / 1000 for i in range(n)]

    sigma_q_es = []

    for i in range(n):
        s_i = calc_sigma_I(i_es[i])
        s_u = calc_sigma_U(u_es[i])
        s = calc_sigma_2(s_i, s_u, i_es[i], u_es[i], q_es[i])
        sigma_q_es.append(s)


    epsilon_q_es = [(sigma_q_es[i]/q_es[i]) * 100 for i in range(n)]



    r_es = [u_es[i] / i_es[i] for i in range(n)]

    sigma_r_es = []

    for i in range(n):
        s_i = calc_sigma_I(i_es[i])
        s_u = calc_sigma_U(u_es[i])
        s = calc_sigma_2(s_i, s_u, i_es[i], u_es[i], r_es[i])
        sigma_r_es.append(s)

    epsilon_r_es = [(sigma_r_es[i] / r_es[i]) * 100 for i in range(n)]




    tochnost = 3
    r_es = [round(i, tochnost) for i in r_es]
    sigma_r_es = [round(i, tochnost) for i in sigma_r_es]
    epsilon_r_es = [round(i, tochnost) for i in epsilon_r_es]
    sigma_q_es = [round(i, tochnost) for i in sigma_q_es]
    epsilon_q_es = [round(i, tochnost) for i in epsilon_q_es]
    q_es = [round(i,tochnost) for i in q_es]


    k, b, dk, db = linear_regression(q_es, r_es)
    styles = ['-', '--', '-.', ':', '-', '--']
    markers = ['.', '.', '.', '.', 'v', 's']
    msizes = [6, 6, 6, 6, 6, 4]
    colors = ['b', 'g', 'r', 'm', 'c', 'y']


    if to_paint:
        plt.plot(np.array(q_es), k * np.array(q_es) + b, color=colors[number - 2], label=f"{number}0°C",
                linestyle=styles[number - 2], marker=markers[number - 2],
                    markersize=msizes[number - 2])
        plt.errorbar(q_es, r_es, sigma_q_es, sigma_r_es, fmt='.', ecolor='black', zorder=1)
    spp.append((number, k, dk, b, db))

    return (k, dk, b, db)

    #print(f"T: {number * 10} °C, k: {round(k, 6)}, sigma_k: {round(dk, 7)}, varepsilon_k: {round((dk/k) * 100, 3)} , R_0: {round(b, 3)}, sigma_R0: {round(db, 3)}, varepsilon_b: {round((db/b) * 100, 3)}")


def paint_graph_RT(sp, to_paint):
    r_es, sR_es, t_es = find_R_sR_T(sp)

    k, b, dk, db = linear_regression(t_es, r_es)

    if to_paint:
        plt.plot(np.array(t_es), k * np.array(t_es) + b, color='blue')
        plt.errorbar(t_es, r_es, 0, sR_es, fmt='.', ecolor='black', zorder=1)
    
    alpha = (1/b) * k
    print(f""" k: {round(k * 100, 2)}, dk: {round(dk * 100, 2)}, b: {round(b, 3)}, b: {round(db, 3)}, \\alpha: {round(alpha * 1000, 3)}, \\sigma_a: {round(calc_sigma_2(dk, db, k, b, alpha) * 1000, 3)},  
""")
    return k, dk, b, db


def paint_kT(sp, to_paint):

    t_es, k_es, sigma_es, epsilon_es = sp
    if to_paint:
        plt.errorbar(t_es, k_es, sigma_es, 0, fmt='.', ecolor='black', zorder=1)


def paint_ln_graph(data, to_paint):
    t_es, k_es, sigma_es, epsilon_es = data
    t_es = [log(i) for i in t_es]
    k_es = [log(i) for i in k_es]
    sigma_es =[i/100 for i in epsilon_es]
    k, b, dk, db = linear_regression(t_es, k_es)
    if to_paint:
        plt.plot(np.array(t_es), k * np.array(t_es) + b, color='blue')
        plt.errorbar(t_es, k_es, sigma_es, 0, fmt='.', ecolor='black', zorder=1)
    print(f'k: {k}, dk: {dk}')
    




RQ_sp = []



for i in range(2, 8):
    paint_graph_RQ(i, False)


RT_k, RT_dk, RT_b, RT_db = paint_graph_RT(spp, False)


for i in range(2, 8):
    RQ_sp.append(paint_graph_RQ(i, False))


const = log(7000/50) / (2 * math.pi * 0.4)


print('need')
print(table_coefficient_teploprovodnosti(RQ_sp, RT_k, RT_dk, RT_b, RT_db)[0])

paint_kT(table_coefficient_teploprovodnosti(RQ_sp, RT_k, RT_dk, RT_b, RT_db)[1], False)

paint_ln_graph(table_coefficient_teploprovodnosti(RQ_sp, RT_k, RT_dk, RT_b, RT_db)[1], True)











#print(last_table(spp))


plt.xlabel('ln(T)')
plt.ylabel('ln(k)')

plt.grid()
plt.legend()
plt.show()




#print(create_table(i_es, u_es, q_es, sigma_q_es, epsilon_q_es, r_es, sigma_r_es, epsilon_r_es))




