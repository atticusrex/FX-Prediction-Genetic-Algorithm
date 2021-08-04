'''
ORDER

This class provides all the funcitonality for orders.

'''
class Order:
    # This is where an order is instantiated, and the arguments are:
    # order_type = string ('buy', 'sell')
    # price = the buy/sell price for the position
    # cash = the amount of money in the trader's account at the time of purchase
    # stop_loss = maximum percent loss before closing
    # take_profit = the max percent gain before closing
    def __init__(self, order_type, price, cash, stop_loss, take_profit):
        self.open_price = price
        self.order_type = order_type
        self.initial_value = cash
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.status = 'open'
        self.current_value = cash
    # This checks to see if the stock has passed the stop loss
    # or take profit functions
    def check_stops(self, price, leverage, spread, commission):
        if self.status == 'open':
            buying_power = self.initial_value * leverage
            if self.order_type == 'long':
                current_value = ((price - spread) / self.open_price) * buying_power - buying_power + self.initial_value
                current_value -= commission
            elif self.order_type == 'short':
                current_value = self.initial_value + (1 - (price + spread) / self.open_price) * buying_power
                current_value -= commission
            percent_gained = (current_value / self.initial_value - 1) * 100
            percent_lost = (1 - current_value / self.initial_value) * 100

            self.current_value = current_value
            if percent_gained >= self.take_profit:
                self.close(price, leverage, spread, commission)
            elif percent_lost >= self.stop_loss:
                self.close(price, leverage, spread, commission)
    
    # This provides the functionality for closing an order.
    # It takes the new price of the security, the leverage of the trader,
    # the spread of the trader, and any commission there might be.
    def close(self, price, leverage, spread, commission):
        buying_power = self.initial_value * leverage
        if self.status == 'open':
            if self.order_type == 'long':
                current_value = ((price - spread) / self.open_price) * buying_power - buying_power + self.initial_value
                current_value -= commission
            elif self.order_type == 'short':
                current_value = self.initial_value + (1 - (price + spread) / self.open_price) * buying_power
                current_value -= commission
            self.current_value = current_value
            self.status = 'closed'
        return self.current_value
            
'''
TRADER

This is the class that creates our little trading bots.

These bots have to have the ability to buy, sell, and close their trades.

This is a central place for adjusting all of the trading-specific parameters
like leverage, commission, spread, stoploss, takeprofit, etc.

'''
class Trader:
    # Instantiation of the trader with an initial portfolio value.
    def __init__(self, portfolio_val):
        self.cash = portfolio_val
        self.leverage = 1
        self.commission = 0
        self.spread = .0000
        self.sold = False
        self.bought = False
        # Initially, the trader's order is a None object,
        # but once it gets a buy or sell signal it becomes an Order object
        self.order = None
        self.stoploss = 5
        self.takeprofit = 1e6
    
    # This checks to see whether the trader has hit any stops or not
    def refresh(self, price):
        if self.order != None:
            self.order.check_stops(price, self.leverage, self.spread, self.commission)

    # This gives functionality to buy the stock
    def buy(self, price):
        if self.sold:
            self.cash = self.order.close(price, self.leverage, self.spread, self.commission)
            self.order = Order('long', price, self.cash, self.stoploss, self.takeprofit)
            self.bought = True
            self.sold = False
        elif self.order == None:
            self.order = Order('long', price, self.cash, self.stoploss, self.takeprofit)
            self.bought = True
            self.sold = False
    
    # This gives the functionality to sell the stock
    def sell(self, price):
        if self.bought:
            self.cash = self.order.close(price, self.leverage, self.spread, self.commission)
            self.order = Order('short', price, self.cash, self.stoploss, self.takeprofit)
            self.bought = False
            self.sold = True
        elif self.order == None:
            self.order = Order('short', price, self.cash, self.stoploss, self.takeprofit)
            self.bought = False
            self.sold = True

    # This closes any open orders. 
    def close(self, price):
        
        if self.sold:
            self.cash = self.order.close(price, self.leverage, self.spread, self.commission)
            self.bought = False
            self.sold = False
            self.order = None
        if self.bought:
            self.cash = self.order.close(price, self.leverage, self.spread, self.commission)
            self.bought = False
            self.sold = False
            self.order = None

        