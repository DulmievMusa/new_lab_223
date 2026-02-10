import pandas as pd
import numpy as np
from math import sqrt

import matplotlib.pyplot as plt


def least_squares(x, y):
    coeff = np.mean(x*y) / np.mean(x*x)
    err = 1 / np.sqrt(len(x)) * np.sqrt((y*y).mean() / (x*x).mean() - coeff ** 2)
    return coeff, err

def delta_sl(n, R, v, i):
    v_srednee = np.mean(v*v)
    i_srednee = np.mean(i*i)
    result = (1/sqrt(n)) * sqrt((v_srednee / i_srednee) - R**2)
    return result

def delta_sist(R, pog_v, pog_i, v, i):
    return R * sqrt((pog_v/max(v))**2 + ((pog_i/max(i))**2))

def delta_obshee(d_sl, d_sist):
    return sqrt(d_sl**2 + d_sist**2)
