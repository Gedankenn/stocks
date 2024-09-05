#!/usr/bin/env python3

import investpy as inv
import yfinance as yfi
from datetime import datetime, date, timedelta
import asciichartpy as asciiplot

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Stock:
    def __init__(self, symbol, quantity=1, buy_price=0, buy_date="", sell_price='', sell_date=""):
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

    def read_tickets(self):
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
            my_stocks["SELL_DATE"].append(l1[5].split(":")[1])
        return my_stocks


    def __str__(self):
        return f"Stock: {self.symbol}, Quantity: {self.quantity}, Buy Price: {self.buy_price}, Buy Date: {self.buy_date}, Sell Price: {self.sell_price}, Sell Date: {self.sell_date}"

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
