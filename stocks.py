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

class Stock:
    def __init__(self, symbol='', quantity=1, buy_price=0, buy_date="", sell_price='', sell_date=""):
        self.symbol = symbol
        self.quantity = quantity
        self.buy_price = buy_price
        self.buy_date = buy_date
        self.sell_price = sell_price
        self.sell_date = sell_date

    def get_last_month_history_stock(self):
        ticket = self.symbol + ".sa"
        ticker = yfi.Ticker(ticket)
        hist = ticker.history(period="1mo")
        return hist

    def get_all_stocks(self):
        stocks = inv.get_stocks(country = 'brazil')
        return stocks

    def __str__(self):
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


def read_tickets():
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

