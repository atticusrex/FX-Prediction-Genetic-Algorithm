from Functions import *
import os
from Dataset import Dataset
import matplotlib.pyplot as plt

__author__ = "Atticus Rex"
__copyright__ = "Copyright (C) 2021 Atticus Rex"
__license__ = "Public Domain"
__version__ = "4.0"

# This just initializes the config file
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'Data\\config.txt')

# this sets up the main loops depending on the number of desired epochs.
# If you just want to run the simulation once, go into the Functions module and 
# set the number of epochs to 1. 

for i in range(epochs):
    [X, Y, final_profit] = run(config_path)

    print("\n\nFinal Profit: " + str(final_profit) + "\n\n")

    # Plots the winning trader's portfolio value over time to see how 
    # profittable the neural network actually is. 
    plt.plot(X, Y)
    plt.title("Winning Trader's Portfolio Value Over Time")
    plt.ylabel("Portfolio Value")
    plt.xlabel("Minutes")

plt.show()