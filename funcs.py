from math import *
import math



def calc_sigma_U(u):
    if u < 1000:
        return sqrt((0.00009 * u + 0.01) ** 2 + (0.5) ** 2)
    elif u < 10000:
        return sqrt((0.00012 * u + 0.02) ** 2 + (0.5) ** 2)
    
def calc_sigma_I(i):
    return sqrt((0.0005 * i + 0.001) ** 2 + (0.05) ** 2)

def calc_sigma_2(sigma_x, sigma_y, x, y, O):
    return sqrt((sigma_x/x) ** 2 + (sigma_y/y) ** 2) * O


# (number, k, dk, b, db)
def find_R_sR_T(sp):
    r_es = []
    sR_es = []
    t_es = []
    for i in range(2, 8):
        r_es.append(sp[i - 2][3])
        sR_es.append(sp[i - 2][4])
        t_es.append(sp[i -2 ][0] * 10)
        
    return (r_es, sR_es, t_es)





def generate_latex_table(i_es, u_es, r_es):
    """
    Генерирует LaTeX код для таблицы с измерениями I, U, R.
    
    Параметры:
    i_es -- массив значений силы тока (I)
    u_es -- массив значений напряжения (U)
    r_es -- массив значений сопротивления (R)
    """
    
    # Проверка на одинаковую длину массивов
    if not (len(i_es) == len(u_es) == len(r_es)):
        raise ValueError("Все массивы должны иметь одинаковую длину")
    
    # Начало LaTeX документа
    latex_code = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage[table]{xcolor}
\\usepackage{booktabs}
\\usepackage{siunitx}

\\begin{document}

\\begin{table}[htbp]
\\centering
\\caption{Измерения силы тока, напряжения и сопротивления}
\\label{tab:measurements}
\\begin{tabular}{|c|c|c|}
\\hline
\\textbf{I (\\si{\\ampere})} & \\textbf{U (\\si{\\volt})} & \\textbf{R (\\si{\\ohm})} \\\\
\\hline
"""
    
    # Добавление строк с данными
    for i, (i_val, u_val, r_val) in enumerate(zip(i_es, u_es, r_es)):
        # Преобразуем числа в строки, округляем для красоты
        i_str = f"{i_val:.3f}" if isinstance(i_val, (int, float)) else str(i_val)
        u_str = f"{u_val:.3f}" if isinstance(u_val, (int, float)) else str(u_val)
        r_str = f"{r_val:.3f}" if isinstance(r_val, (int, float)) else str(r_val)
        
        latex_code += f"{i_str} & {u_str} & {r_str} \\\\\n"
        
        # Добавляем горизонтальную линию после каждой строки
        latex_code += "\\hline\n"
    
    # Завершение таблицы и документа
    latex_code += """\\end{tabular}
\\end{table}

\\end{document}"""
    
    return latex_code



def create_table(i_es, u_es, q_es, sigma_q_es, epsilon_q_es, r_es, sigma_r_es, epsilon_r_es):
    
    vstavka = ""
    for i in range(10):
        vstavka += f""" {i_es[i]}  & {u_es[i]} & {r_es[i]} & {sigma_r_es[i]} & {epsilon_r_es[i]} & {q_es[i]} & {sigma_q_es[i]} & {epsilon_q_es[i]} \\\\
\\hline \n"""


    text = f"""\\begin{'{table}'}[H]
\\begin{'{center}'}
\\begin{'{tabular}'}{'{|c|c|c|c|c|c|c|c|}'}
\\hline
\\rule{'{0pt}'}{'{12pt}'}
I, мА & U, мВ & R, Ом & $\\sigma_\\text{'{R}'}$, Ом & $\\varepsilon_\\text{'{R}'}, \\% $ & Q, мВт & $\\sigma_\\text{'{Q}'}$, мВт & $\\varepsilon_\\text{'{Q}'}, \\% $\\\\
\\hline
{vstavka}
\\end{'{tabular}'}
\\end{'{center}'}
\\caption{'{40°C}'}
\\end{'{table}'}"""
    return text


                                                                                                                                                                                        #$\sigma_{R_0}, \text{Ом}$
def last_table(sp):

    vstavka = ""
    for i in range(2, 8):
        number, k, dk, b, db = sp[i - 2]
        vstavka += f"""{number * 10} & {round(k, 4)} & {round(dk, 5)} & {round((dk/k) * 100, 3)} & {round(b, 3)} & {round(db, 3)} & {round((db/b) * 100, 3)} \\\\
\\hline \n"""


    text = f"""\\begin{'{table}'}[H]
\\begin{'{center}'}
\\begin{'{tabular}'}{'{|c|c|c|c|c|c|c|}'}
\\hline
\\rule{'{0pt}'}{'{12pt}'}
T, $\\circ$ C & $\\frac{'{dR}'}{'{dQ}'}, \\frac{'{\\text{Ом}}{\\text{Вт}}'}$ & $\\sigma_{'{\\frac{dR}{dQ}}'}, \\frac{'{\\text{Ом}}{\\text{Вт}}'}$ & $\\varepsilon_{'{\\frac{dR}{dQ}}, \\%'}$ & $R_0, \\text{'{Ом}'}$ & $\\sigma_{'{R_0}'}, \\text{'{Ом}'}$ &  $\\varepsilon_{'{R_0}'}, \\%$\\\\
\\hline
{vstavka}
\\end{'{tabular}'}
\\end{'{center}'}
\\caption{'Сопротивления $R_0$ и коэффициенты $\\frac{dR}{dQ}$ для исследуемых температур'}
\\end{'{table}'}"""
    return text




def table_coefficient_teploprovodnosti(RQ_sp, RT_k, RT_dk, RT_b, RT_db):
    const = log(7000/50) / (2 * math.pi * 0.4)
    vstavka = ""
    for i in range(2, 8):
        coefficient, dk, b, db = RQ_sp[i - 2]
        k = (RT_k/ coefficient) * const

        sigma = sqrt((dk/coefficient) ** 2 + (RT_dk / RT_k) ** 2 + (2/400) ** 2) * k

        epsilon = sigma / k
        vstavka += f"""{i * 10} & {round(k, 2)} & {round(sigma, 2)} & {round(epsilon * 100, 2)} \\\\
\\hline \n"""
        
    text = f"""\\begin{'{table}'}[H]
            \\begin{'{center}'}
            \\begin{'{tabular}'}{'{|c|c|c|c|}'}
            \\hline
            \\rule{'{0pt}'}{'{12pt}'}
            "$T, \\,^\\circ \\text{'{C}'}$ & $k, \\frac{'\\text{мВт}'}{'\\text{м} \\cdot \\text{K}'}$ & $\\sigma_k, \\frac{'\\text{мВт}'}{'\\text{м} \\cdot \\text{K}'}$ & $\\varepsilon_k$, \\%$\\\\
            \\hline
            {vstavka}
            \\end{'{tabular}'}
            \\end{'{center}'}
            \\caption{'Коэффициенты теплопроводности воздуха\\ при атмосферном давлении для исследуемых температур'}
            \\end{'{table}'}"""
    return text
        #print(f'T: {i*10}, k: {k}, sigma_k {sigma}, epsilon_k {epsilon * 100}')




