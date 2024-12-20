#!/usr/bin/env python3
'''
This is the stocks class that will handle all the stocks operations.
Author: Fabio Slika Stella
Date: 2024-09-10
'''

import investpy as inv
import yfinance as yfi
from datetime import datetime, date, timedelta
from uniplot import plot as asciiplot
from bcolors import bcolors
from yahooquery import Ticker as yq
import os

class Stock:
    '''
    This class will handle all the stock operations
    '''
    def __init__(self, symbol='', quantity='', buy_price='', buy_date="", sell_price='', sell_date=""):
        self.symbol = symbol
        self.quantity = quantity
        self.buy_price = buy_price
        self.buy_date = buy_date
        self.sell_price = sell_price
        self.sell_date = sell_date
        self.dividends = ''
        self.earnings = ''
        self.last_dividend = ''
        self.previous_close = ''

    def get_last_month_history_stock(self):
        '''
        This method will return the last month history of the stock
        '''
        ticket = self.symbol + ".sa"
        ticker = yfi.Ticker(ticket)
        hist = ticker.history(period="1mo")
        return hist

    def get_stock_price(self):
        '''
        This method will return the stock price
        '''
        ticket = self.symbol + ".sa"
        ticker = yfi.Ticker(ticket)
        previous_close = 0
       
        #previous_close = yq(self.symbol).history(period='1d')['close'][-1]
        previous_close = ticker.history(period="1d")["Close"].iloc[-1]
        # Convert the previous close to float with 2 decimal places
        previous_close = "{:.2f}".format(previous_close)
        return previous_close

    def update_stock_info(self):
        '''
        This method will update the stock information
        '''
        ticket = self.symbol + ".sa"
        ticker = yfi.Ticker(ticket)
        self.previous_close = ticker.history(period="1d")["Close"].iloc[-1]
        self.previous_close = "{:.2f}".format(self.previous_close)

        if self.symbol[-2:] == "11":
            # If the stock is a FII
            dividend = ticker.dividends
            if len(dividend) > 0:
                # get the buy_date in the format %Y-%m 
                self.earnings = 0
                self.last_dividend = dividend.iloc[-1]
                self.last_dividend = "{:.2f}".format(float(self.last_dividend))
                buy_date = datetime.strptime(self.buy_date, "%Y-%m-%d")
                buy_date = buy_date.strftime("%Y-%m")

                dividend_list = dividend[dividend.index > buy_date]
                for div in dividend_list:
                    self.earnings += float(div)*float(self.quantity)

                self.earnings = "{:.2f}".format(self.earnings)

    def __str__(self):
        '''
        This method will return the stock information
        '''
        self.update_stock_info()
        price = float(self.previous_close)
        ref_price = float(self.buy_price)
        total = float(self.quantity) * ref_price
        total = "{:.2f}".format(total)

        text = f"{bcolors.HEADER} --------- Stock ---------\n"
        aux = f"{bcolors.HEADER}|{bcolors.WARNING}Symbol: {bcolors.OKBLUE}{self.symbol.upper()}{bcolors.ENDC}"
        text += aux + (" " * (44 - len(aux))) + f"{bcolors.HEADER}|\n"
        
        aux = f"{bcolors.HEADER}|{bcolors.WARNING}Buy Date: {bcolors.ENDC}{self.buy_date}"
        text += aux + " " * (39 - len(aux)) + f"{bcolors.HEADER}|\n"
        
        aux = f"{bcolors.HEADER}|{bcolors.WARNING}Quantity: {bcolors.ENDC}{self.quantity}"
        text += aux + " " * (39 - len(aux)) + f"{bcolors.HEADER}|\n"

        aux = f"{bcolors.HEADER}|{bcolors.WARNING}Buy Price: {bcolors.ENDC}{self.buy_price}"
        text += aux + " " * (39 - len(aux)) + f"{bcolors.HEADER}|\n"
        
        aux = f"{bcolors.HEADER}|{bcolors.WARNING}Total: {bcolors.ENDC}{total}"
        text += aux + " " * (39 - len(aux)) + f"{bcolors.HEADER}|\n"


        if self.sell_price != '' or self.sell_date != '':
            aux = f"{bcolors.HEADER}|{bcolors.WARNING}Sell Price: {bcolors.ENDC}{self.sell_price}"
            text += aux + " " * (39 - len(aux)) + f"{bcolors.HEADER}|\n"

            aux = f"{bcolors.HEADER}|{bcolors.WARNING}Sell Date: {bcolors.ENDC}{self.sell_date}"
            text += aux + " " * (39 - len(aux)) + f"{bcolors.HEADER}|\n"

            price = self.sell_price 
            ref_price = self.buy_price

        if price >= ref_price:
            variation = "{:.2f}".format((price - ref_price) / ref_price * 100)
            gain = "{:.2f}".format((price - ref_price) * float(self.quantity))
            aux = f"{bcolors.HEADER}|{bcolors.WARNING}Price: {bcolors.OKGREEN}{price}"
            text += aux + " " * (40 - len(aux)) + f"{bcolors.HEADER}|\n"

            aux = f"{bcolors.HEADER}|{bcolors.WARNING}Gain: {bcolors.OKGREEN}{gain} {variation}%"
            text += aux + " " * (40 - len(aux)) + f"{bcolors.HEADER}|\n"
        
        else:
            variation = "{:.2f}".format((ref_price - price) / ref_price * 100)
            loss =  "{:.2f}".format((ref_price - price) * float(self.quantity)) 
            aux = f"{bcolors.HEADER}|{bcolors.WARNING}Price: {bcolors.FAIL}{price}"
            text += aux + " " * (40 - len(aux)) + f"{bcolors.HEADER}|\n"

            aux = f"{bcolors.HEADER}|{bcolors.WARNING}Loss: {bcolors.FAIL}{loss} {variation}%"
            text += aux + " " * (40 - len(aux)) + f"{bcolors.HEADER}|\n"
        
        if self.last_dividend != '':
            # If the stock is a FII
            aux = f"{bcolors.HEADER}|{bcolors.WARNING}Last Dividend: {bcolors.OKGREEN}{self.last_dividend}"
            text += aux + " " * (40 - len(aux)) + f"{bcolors.HEADER}|\n"

            if self.earnings != '':
                aux = f"{bcolors.HEADER}|{bcolors.WARNING}Dividend Gains: {bcolors.OKGREEN}{self.earnings}"
                text += aux + " " * (40 - len(aux)) + f"{bcolors.HEADER}|\n"
        text += f"{bcolors.HEADER}"
        text += "-" * 26
        text += f"{bcolors.ENDC}\n"
        return text

    def plot_stock(self, start_date, end_date):
        '''
        This method will plot the stock
        @param start_date: The start
        @param end_date: The end
        '''
        ticket = self.symbol + ".sa"
        ticker = yfi.Ticker(ticket)
        hist = ticker.history(start=start_date, end=end_date)
        hist = hist["Close"]

        print(f"{bcolors.BOLD}Stock: {self.symbol.upper()}{bcolors.ENDC}")
        print(f"{asciiplot(hist, color="green", height=20, width=100)}")


    def plot_stock_since_buy(self):
        '''
        This method will plot the stock since the buy date
        '''
        start_date = self.buy_date
        end_date = date.today()
        self.plot_stock(start_date, end_date)

def verify_folder():
    '''
    This function will verify if the folder my_stocks exists
    '''
    if not os.path.exists("my_stocks"):
        os.mkdir("my_stocks")

def verify_files():
    '''
    This function will verify if the files exist
    '''
    verify_folder()
    try:
        f = open("my_stocks/papers.txt","r")
        f.close()
    except:
        f = open("my_stocks/papers.txt","w")
        f.close()

    try:
        f = open("my_stocks/history.txt","r")
        f.close()
    except:
        f = open("my_stocks/history.txt","w")
        f.close()

def read_tickets():
    '''
    This function will read the tickets from the file
    @return: The tickets
    '''
    verify_files()
    f = open("my_stocks/papers.txt","r")
    my_stocks = {"SYMBOL":[],"QUANTITY":[],"BUY_PRICE":[],"BUY_DATE":[],"SELL_PRICE":[],"SELL_DATE":[]}
    lines = f.readlines()
    f.close()
    for line in lines:
        l1 = line.split(",")
        my_stocks["SYMBOL"].append(l1[0].split(":")[1])
        my_stocks["QUANTITY"].append(l1[1].split(":")[1])
        my_stocks["BUY_PRICE"].append(l1[2].split(":")[1])
        my_stocks["BUY_DATE"].append(l1[3].split(":")[1])
        my_stocks["SELL_PRICE"].append(l1[4].split(":")[1])
        my_stocks["SELL_DATE"].append(l1[5].split(":")[1].strip("\n"))
    return my_stocks

def save_tickets(my_stocks):
    '''
    This function will save the tickets to the file
    @param my_stocks: The stocks to be saved
    '''

    stocks = ''
    for i in range(len(my_stocks)):
        stocks += f"SYMBOL:{my_stocks[i].symbol}, QUANTITY:{my_stocks[i].quantity}, BUY_PRICE:{my_stocks[i].buy_price}, BUY_DATE:{my_stocks[i].buy_date}, SELL_PRICE:{my_stocks[i].sell_price}, SELL_DATE:{my_stocks[i].sell_date}\n"
    f = open("my_stocks/papers.txt","w")
    f.write(stocks)
    f.close()

def update_history(stock):
    '''
    This function will update the history
    @param stocks: The stocks to be updated
    '''
    f = open("my_stocks/history.txt","a") 
    text = f"{stock.symbol},{stock.quantity},{stock.buy_price},{stock.buy_date},{stock.sell_price},{stock.sell_date}\n"
    f.write(text)
    f.close()

def get_all_stocks():
    '''
    This method will return all the stocks available in the market
    '''
    stocks = inv.get_stocks(country = 'brazil')
    return stocks

def is_stock_listed(stock):
    '''
    This function will verify if the stock is listed
    @param stock: The stock to be verified
    @return: True if the stock is listed, False otherwise
    '''
    all_stocks = get_all_stocks().symbol
    stock = stock.upper()
    for s in all_stocks:
        if s == stock:
            return True
    return False
