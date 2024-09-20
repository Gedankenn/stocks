#!/usr/bin/env python3
'''
This is the stocks class that will handle all the stocks operations.
Author: Fabio Slika Stella
Date: 2024-09-10
'''

import investpy as inv
import yfinance as yfi
from datetime import datetime, date, timedelta
import asciichartpy as asciiplot
from bcolors import bcolors
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

    def get_last_month_history_stock(self):
        '''
        This method will return the last month history of the stock
        '''
        ticket = self.symbol + ".sa"
        ticker = yfi.Ticker(ticket)
        hist = ticker.history(period="1mo")
        return hist

    def __str__(self):
        '''
        This method will return the stock information
        '''
        text = f"{bcolors.BOLD}{bcolors.HEADER} ------ Stock ------{bcolors.ENDC}\n"
        text += f"{bcolors.BOLD}{bcolors.OKGREEN}Symbol: {bcolors.ENDC}{self.symbol.upper()}\n"
        text += f"{bcolors.BOLD}{bcolors.OKGREEN}Quantity: {bcolors.ENDC}{self.quantity}\n"
        text += f"{bcolors.BOLD}{bcolors.OKGREEN}Buy Price: {bcolors.ENDC}{self.buy_price}\n"
        text += f"{bcolors.BOLD}{bcolors.OKGREEN}Buy Date: {bcolors.ENDC}{self.buy_date}\n"
        text += f"{bcolors.BOLD}{bcolors.OKGREEN}Sell Price: {bcolors.ENDC}{self.sell_price}\n"
        text += f"{bcolors.BOLD}{bcolors.OKGREEN}Sell Date: {bcolors.ENDC}{self.sell_date}\n"
        text += f"{bcolors.BOLD}{bcolors.HEADER} -------------------{bcolors.ENDC}\n"
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

        config = {
            'width': 100,
            'height': 20,
            'x_label': 'Time',
            'y_label': 'Price',
            'colors': [asciiplot.lightcyan,
                       asciiplot.lightmagenta],
            'fg_color': [asciiplot.green] # light green foreground
        }

        print(f"{bcolors.BOLD}Stock: {self.symbol.upper()}{bcolors.ENDC}")
        print(asciiplot.plot(hist, config))


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
