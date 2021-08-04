
# FIELDS
ema_period = 120 # How many minutes the exponential average is
candle_lookback = 10 # How many candles back the neural network looks
multiplier = 10000 # The multiplier for conditioning the data 
vol_multiplier = 1 # The multiplier for conditioning volume data 

# Just a function that takes the average of a list
def average(data):
    sum = 0
    index = 0
    for entry in data:
        sum += entry
        index += 1
    if index > 0:
        return sum / index
    else:
        return 0

# This is a function that completes a raw list of the week data.
# Since this has already been done, and the file is saved as a .data file,
# You shouldn't have to worry about this one too much. Look in the README 
# as to the format of the completed dataset. 
def complete_data(week_data):
    ema = week_EMA(week_data, ema_period)
    [macd, signal, histogram] = MACD(week_data)
    rsi = RSI(week_data)
    complete_dataset = []
    for i in range(len(week_data)):
        complete_list = []
        for j in range(len(week_data[i])):
            complete_list.append(week_data[i][j])
        complete_list.append(ema[i])
        complete_list.append(macd[i])
        complete_list.append(signal[i])
        complete_list.append(histogram[i])
        complete_list.append(rsi[i])
        complete_dataset.append(complete_list)
    
    return complete_dataset

# This is responsible for finding the exponential moving average
def week_EMA(week_data, period):
    ema = [week_data[0][4]]
    for i in range(1, len(week_data)):
        current = week_data[i][4]
        previous = week_data[i - 1][4]
        ema.append((current * (2 / (1 + period)) + ema[i - 1] * (1 - 2 / (1 + period))))
    return ema

# This is responsible for finding a simple ema of a list
def EMA(data_list, period):
    ema = [data_list[0]]
    for i in range(1, len(data_list)):
        current = data_list[i]
        previous = data_list[i - 1]
        ema.append((current * (2 / (1 + period)) + ema[i - 1] * (1 - 2 / (1 + period))))
    return ema

# This finds a 12-26 macd with a signal of 9 days
def MACD(week_data):
    bar_12 = week_EMA(week_data, 12)
    bar_26 = week_EMA(week_data, 26)
    macd = []
    for i in range(len(bar_12)):
        macd.append(bar_12[i] - bar_26[i])
    
    signal = EMA(macd, 9)

    histogram = []

    for i in range(len(signal)):
        histogram.append(macd[i] - signal[i])
    
    return [macd, signal, histogram]

# This calculates the relative strength index of the 
# data. 
def RSI(week_data):
    rsi = [0]
    period = 14
    for i in range(1, len(week_data)):
        if i < period:
            narrowed_list = week_data[0:i + 1]
            ups = []
            downs = []
            for j in range(1, len(narrowed_list)):
                change = narrowed_list[j][4] / narrowed_list[j - 1][1] - 1
                if change > 0:
                    ups.append(change)
                if change < 0:
                    downs.append(abs(change))
        else:
            ups = []
            downs = []
            for j in range(1, period + 1):
                change = week_data[i - period + j][4] / week_data[i - period + j - 1][1] - 1
                if change > 0:
                    ups.append(change)
                if change < 0:
                    downs.append(abs(change))
        
        
        up_avg = average(ups)
        down_avg = average(downs)
        if down_avg == 0:
            rsi.append(100)
        else:
            rsi.append(100 - 100 / (1 + (up_avg / down_avg)))
        
    return rsi
            
        