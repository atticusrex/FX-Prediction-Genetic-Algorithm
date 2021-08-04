from Trader import Trader
from Functions import *
from Dataset import Dataset
from pprint import pprint
import matplotlib.pyplot as plt
import random as rand

def func(k, q, x):
    if x > 0:
        result = func(k, q, x - 1)
        return result * q * (k + x - 1) / x
    else:
        return (1 - q) ** k

p_0 = func(4, 0.6, 0)
p_1 = func(4, 0.6, 1)
p_2 = func(4, 0.6, 2)
p_3 = func(4, 0.6, 3)

print(p_0+ p_1+ p_2+ p_3)