README

------------------------------------------------------
        INTRODUCTION
------------------------------------------------------

Hello! Thanks for using my python program for neural network based algorithmic stock trading. 

This is here to explain the basic functionality and how you can adapt it to your needs.

So this program uses the genetic algorithm to deploy a bunch of algorithmically based 
day trading bots that learn over time how to effectively day trade. The way the simulation
works is by using random sets of intraday data for different days of AAPL stock. 

So, to begin, each bot has a random set of weights and biases on its respective neural network. 

Then, the simulation will run one round of daytrading all on the same dataset for each of the bots. 

The bots that do the best will move on to the next generation and have some minor genetic mutations 
giving them the biodiversity to evolve over time and produce new strategies. 

The more iterations you give the bots, the more fine-tuned their day-trading skills will be. 

The larger the population of bots you deploy, the higher the probability is of finding a profittable 
bot. 

A large part of this simulation depends on what data the bots are basing their decision on. 

Right now, I have created a .data file that has a list of all of the days of 20+ years of AAPL
intraday stock data. It gets loaded in the Dataset module. 

The .data file unpacks itself into a list of days in the following format:

self.complete_data = [
    Each item of this list is data for a specific trading day
]

Specific trading day data = [
    Datetime object,
    Open Price,
    High Price,
    Low Price,
    Close Price,
    Volume,
    Price EMA,
    Price MACD,
    Price MACD Signal,
    Price MACD Histogram,
    Price RSI
]

So this is the raw data that the bots have access to. There is also something called
a lookback, and that tells how many past minutes of this data the bots can look at. 

The data then gets conditioned and scaled so that it fits well into the network inputs. 

You're welcome to calculate your own indicators using the already existing price data. 

------------------------------------------------------
        RUNNING THE PROGRAM
------------------------------------------------------

The program runs through the Main.py script. 

All you have to do is just run that program and everything 
else should run through that. 

------------------------------------------------------
        EDITING PARAMETERS
------------------------------------------------------

This is arguably the most important part of this script.
You're going to need to be able to edit the parameters of
the simulation to be able to play around with different 
configurations and find a way to produce the most
profittable traders. 

The Config File:

Under the "Data\" directory, there's a .txt file called 
'config.txt'. That's where you edit a lot of the parameters
for the neural networks themselves. It's really not too hard,
but it's very important for getting results. IT IS VERY 
IMPORTANT THAT YOU DO NOT CHANGE ANYTHING ABOUT THE Config
FILE BUT THE NUMERIC VALUES OR THE SIMULATION WILL NOT RUN. 

- Population: If you want to adjust the population of the simulation
(e.g. the number of bots you deploy at once), that's under the 
pop_size heading. 

- Number of inputs: This is for adjusting the number of datapoints 
you feed to the neural network. That's going to be in the num_inputs
header of the config file. 

- Number of outputs: Right now, there are only two outputs (buy, sell),
but if you want to have more outputs that's under the num_outputs heading. 

Those are the two parameters that you're really only going to want to adjust. 
The rest are just neural-network specific things that I've already adjusted 
to suit the needs of this simulation. 


#NOTE: There are many other global variables in the Functions module and the 
Data Functions module, but those are explained in more detail in their respective 
locations. 