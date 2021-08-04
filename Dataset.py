import pickle
import random
from Functions import *
from DataFunctions import *
'''
DATASET CLASS

This is the class for the dataset itself. There is a compressed pickle file
that has all of the data for the last 20+ years of Apple Intraday Stock in 
a list data structure to make it easier to access. 

This class provides most of the functinoality for the data.

It also uses all the functions in the DataFunctions module


'''
class Dataset:
    def __init__(self):
        # Loads the data from the pickle file
        self.complete_data = self.load_weeks()

        # This is the earliest day to start taking data from
        # (A lot of intraday data from like 10 years ago isn't that useful)
        self.earliest_point = 3000

        # This narrows the data down to the desired range
        self.narrowed_data = self.complete_data[self.earliest_point:]
        
    # This gets the intraday stock data for a random day 
    def get_random_day(self):
        index = random.randint(0, len(self.narrowed_data) - 1)
        
        return self.narrowed_data[index][:]
    
    # This loads the .data file with all of the intraday data
    def load_weeks(self):
        with open('Data\\DayData.data', 'rb') as infile:
            data = pickle.load(infile)
        print("Successfully Loaded Data!\n")
        return data

    # This saves a .data file with all of the intraday data
    def save_weeks(self):
        with open('Data\\DayData.data', 'wb') as outfile:
            pickle.dump(self.complete_data, outfile)
        print("\nSuccessfully saved Data!")
    
    # This returns a list of the last 250 trading days to 
    # test the winning bot
    def get_winning_data(self):
        winning_list = []
        for i in range(len(self.narrowed_data) - 250, len(self.narrowed_data)):
            for j in range(len(self.narrowed_data[i])):
                winning_list.append(self.narrowed_data[i][j])
        return winning_list


