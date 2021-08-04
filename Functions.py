# IMPORTS
import pickle
import gzip
import neat
from Trader import Trader
from Dataset import Dataset
from DataFunctions import *
import matplotlib.pyplot as plt

'''
FUNCTIONS

This module provides all of the functions for the Main part of the script.

This is responsible for setting up the neural network, testing the winners,
conditioning inputs into the neural network, etc.

'''

# GLOBAL VARS

data = Dataset() # This is where the dataset gets initialized
initial_investment = 10000 # This is the initial investment of the trader bots
gen = 0 # This is just a needed global variable for the algorithm
divisor = 2 # This number tells you how many times the neural network is activated (e.g. checks for signals every **divisor** minutes)
iterations = 100 # This tells how many different samples of the data the networks will take (more iterations will yield better results, but takes longer)
epochs = 1 # This is the number of times the program will repeat the entire simulation. Each simulation will return a different winning trader, so each epoch will 
# have its own winning trader. 

# FUNCTIONS

'''
This function tests the winning trader of the simulation using 
the last 250 trading days of AAPL stock. 

'''
def test_winner(winner, config):

    # Initializes the trader 
    trader = Trader(10000)

    # This is for graphing the trader's progress
    X = [] # Trading days
    Y = [] # Portfolio value

    # This creates a neural network from the winner object 
    net = neat.nn.FeedForwardNetwork.create(winner, config)

    # This gets the data that we'll be using to test the winner on
    winning_data = data.get_winning_data()

    # This is the main loop that the trader trades in
    for i in range(candle_lookback, len(winning_data)):
        X.append(i)
        if (i % divisor) == 0:
            # Finds the current close price
            close_price = winning_data[i][4]

            # Conditions the data into an input for the neural net
            inputs = get_input(winning_data, i)

            # Runs the inputs through the winner's neural net and arrives at outputs
            outputs = net.activate(inputs)

            # The trader makes the decision based on its outputs
            trader = make_decision(trader, outputs, close_price, True)

        # Refreshes just to make sure it didn't hit any stoplosses
        trader.refresh(winning_data[i][4])

        # Adds the trader's portfolio value to the Y list to graph later on 
        Y.append(trader.cash)

    # Closes any open trades. 
    trader.close(winning_data[-1][4])

    # Returns the X and Y variables, as well as the final portfolio value of the winning trader. 
    return [X, Y, trader.cash]


'''
This function is the one that coordinates the simulation. 

It first takes a config file defining the parameters of the simulation. 

Then it creates a population of bots based off of the parameters. 

Then it adds reporters to show the progress of the simulation

Then it runs for the number of specified iterations

Finally, it tests the winner. 

'''
def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to the number of iterations.
    winner = p.run(fitness_func, iterations)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

    return test_winner(winner, config)

# This is the fitness function to assess the fitness of traders
def fitness_func(genomes, config):
    # Makes the generation and initial investments global variables
    global gen, initial_investment

    nets = [] # A list of all of the neural networks
    traders = [] # A list of all of the traders 
    ge = [] # A list of the genomes of each bot

    # Increments the generation by 1
    gen += 1

    # Loops through the genomes to set up each list at the start
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config) # Creates nn for each bot
        nets.append(net) # Appends it to the nets list
        traders.append(Trader(initial_investment)) # Creates a new trader for each item in the population
        ge.append(genome) # Appends the genome of the particular bot to the ge list

    # Gets the data for a random day
    week_data = data.get_random_day()
    #input_lists = get_input_lists(week_data)
    # Loops through the minute by minute data for that day
    for i in range(candle_lookback, len(week_data)):
        if ((i % divisor) == 0):
            close_price = week_data[i][4] # Gets the close price from the raw data
            
            inputs = get_input(week_data, i)

            # Loops through the population to get the individual decisions of 
            # each trader. 

            # Loops through the traders to make decisions
            for x, trader in enumerate(traders):
                # Runs each neural network to produce an output
                outputs = nets[traders.index(trader)].activate(inputs)
                # Decision is made on the output [buy, sell, hold]
                trader = make_decision(trader, outputs, close_price, False)
        for trader in traders:
            trader.refresh(week_data[i][4])
    
    # Makes sure all the traders have sold their shares
    for trader in traders:
        trader.close(close_price)
        
    for x in range(0, len(traders)):
        ge[x].fitness = traders[x].cash

'''
This function is responsible for taking the outputs from the neural network
and then transferring it to the trader so that they can make decisions on whether
or not to buy or sell. 

'''
def make_decision(trader, outputs, close_price, print_bool):
    if (abs(outputs[0] - outputs[1]) > .05):
        decision = outputs.index(max(outputs))
        # Makes the decision based on the output of the network. 

        if decision == 0:
            result = trader.buy(close_price)
            if result and print_bool:
                print("Bought at: " + str(close_price))
                print("Current Cash: " + str(trader.cash))
        elif decision == 1:
            result = trader.sell(close_price)
            if result and print_bool:
                print("Sold at: " + str(close_price))
                print("Current Cash: " + str(trader.cash))
        
    return trader

# This is a function that is used to save any winning traders for 
# future use. If you find a super profittable configuration, then you can
# start saving those traders and using them in Metatrader
def save_winner(winner, final_profit):
        with gzip.open("Data\\WinningTrader.data", 'w', compresslevel=5) as f:
            pickle.dump(winner, f, protocol=pickle.HIGHEST_PROTOCOL)
        # Also saves how profittable the trader was
        outfile = open('Data\BestProfit.txt', 'w+')
        outfile = outfile.write(str(final_profit))


'''
This is a function responsible for turning the raw data from the 
intraday file to scaled inputs for the neural network. 

'''
def get_input(week_data, index):
    # Gets the current price and volume
    current_price = week_data[index][4]
    current_volume = week_data[index][5]
    
    # makes a list for the inputs
    inputs = []

    # Conditions the current candle to feed to the network
    inputs.append((current_price / week_data[index][1] - 1) * multiplier)
    inputs.append((current_price / week_data[index][2] - 1) * multiplier)
    inputs.append((current_price / week_data[index][3] - 1) * multiplier)
    
    # Goes back a specified number of candles to add that data to the network
    for i in range(candle_lookback):
        inputs.append((current_price / week_data[index - i - 1][1] - 1) * multiplier)
        inputs.append((current_price / week_data[index - i - 1][2] - 1) * multiplier)
        inputs.append((current_price / week_data[index - i - 1][3] - 1) * multiplier)
        inputs.append((current_price / week_data[index - i - 1][4] - 1) * multiplier)
        try:
            inputs.append((current_volume / week_data[index - i - 1][5] - 1) * vol_multiplier) 
        except:
            inputs.append((-1 * vol_multiplier)) # Just in case we get a divide by zero error
        
        inputs.append((current_price - week_data[index - i][6]) * multiplier)
        inputs.append(week_data[index - i][7] * multiplier)
        inputs.append(week_data[index - i][8] * multiplier)
        inputs.append(week_data[index - i][9] * multiplier)
        inputs.append(week_data[index - i][10] / 16.67 - 3)
    
    # returns the inputs so that the rest of the script can use them
    return inputs

