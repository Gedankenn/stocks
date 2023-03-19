import investpy as inv
import yfinance as yfi
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import asciichartpy as asciiplot
import os
import matplotlib.pyplot as plt
import mplcyberpunk

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

plt.style.use("cyberpunk")

def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def get_all_stocks():
    stocks = inv.get_stocks(country = 'brazil')
    # print(stocks["symbol"])
    return stocks

def get_last_month_history_stock(ticket):
    ticket = ticket + ".sa"

    ticker = yfi.Ticker(ticket)
    hist = ticker.history(period="1mo")
    print(hist)

def read_tickets():
    f = open("my_stocks/papers.txt","r")
    my_stocks = {"SYMBOL":[],"QUANTITY":[],"BUY_PRICE":[],"BUY_DATE":[]}
    lines = f.readlines()
    f.close()
    for line in lines:
        l1 = line.split(",")
        my_stocks["SYMBOL"].append(l1[0].split(":")[1])
        my_stocks["QUANTITY"].append(l1[1].split(":")[1])
        my_stocks["BUY_PRICE"].append(l1[2].split(":")[1])
        my_stocks["BUY_DATE"].append(l1[3].split(":")[1])
    return my_stocks

def save_buy_stock():
    f = open("my_stocks/papers.txt","a")
    line = "\nSYMBOL:"+(str(input("stock symbol: ")))+", "
    line = line + "QUANTITY:"+str(input("Quantity: "))+", "
    line = line + "BUY_PRICE:"+str(input("BUY Price: "))+", "
    line = line + "BUY_DATE:"+str(date.today().strftime("%Y-%m-%d"))
    f.write(line)
    f.close()

def plot_my_stocks(my_stocks):
    for i in range(len(my_stocks["SYMBOL"])):
        # set ticker symbol and buy date
        symbol = my_stocks["SYMBOL"][i]
        ticker_symbol = my_stocks["SYMBOL"][i] + ".sa"
        buy_date_str = my_stocks["BUY_DATE"][i].strip("\n")
        # convert buy date string to datetime object
        buy_date = datetime.strptime(buy_date_str, "%Y-%m-%d")
        # set end date to today's date
        end_date = datetime.now()
        # get historical data for ticker symbol
        ticker = yfi.Ticker(ticker_symbol)
        hist = ticker.history(start=buy_date, end=end_date.strftime("%Y-%m-%d"))
        buy_line = [float(my_stocks["BUY_PRICE"][i]) for b in range(len(hist["Close"]))]
        last_value = hist["Close"][len(hist["Close"])-1]

        config = {
            'width': 100,
            'height': 20,
            'colors': [asciiplot.green,
                        asciiplot.blue],
            'fg_color': [asciiplot.green]
        }
        min1 = min(hist["Close"])
        min1 = min([min1,buy_line[0]])
        print(f"{bcolors.BOLD}{bcolors.HEADER}-------------------{symbol.upper()}-------------------{bcolors.ENDC}")
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}Gain: {last_value- buy_line[0]:.2f}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}Gain %: {((last_value - buy_line[0])/last_value)*100:.2f}{bcolors.ENDC}")
        
        print(asciiplot.plot([buy_line,hist["Close"]],config))
    # mplcyberpunk.add_glow_effects()
    # plt.show()

def stocks_to_alert(my_stocks):
    for i in range(len(my_stocks["SYMBOL"])):
        symbol = my_stocks["SYMBOL"][i]
        ticker_symbol = my_stocks["SYMBOL"][i] + ".sa"
        ticker = yfi.Ticker(ticker_symbol)
        hist = ticker.history(period='1d')
        current_price = hist["Close"][len(hist["Close"])-1]
        buy_price = float(my_stocks["BUY_PRICE"][i])
        gain = (current_price - buy_price)*100/current_price
        if(gain <= 6):
            print(f"{bcolors.BOLD}{bcolors.WARNING}Ticket: {symbol.upper()} Current Price: {current_price:.2f} Buy Price: {buy_price:.2f} Gain: {gain:.2f}{bcolors.ENDC}")


def menu(stocks, my_stocks):
    # clear_terminal()
    print(f"{bcolors.BOLD}{bcolors.OKGREEN}")
    print("--------------------------------------------")
    print("MAIN - MENU")
    print("1 - Get the last month history for ticket ('Brasil only')")
    print("2 - Read Tickets owned")
    print("3 - Save buy operation")
    print("4 - Plot my stocks")
    
    print("0 - To Exit")
    print(f"{bcolors.ENDC}")
    print(f"{bcolors.WARNING}{bcolors.BOLD}---WARNING---{bcolors.ENDC}")
    my_stocks = read_tickets()
    stocks_to_alert(my_stocks)
    choice = input()
    if choice == '0':
        return 0
    
    if choice == '1':
        clear_terminal()
        print("--------------------------------------------")
        ticket = input("Type the ticket code: ")
        print("--------------------------------------------")
        get_last_month_history_stock(ticket)
    
    elif choice == '2':
        my_stocks = read_tickets()
        print(my_stocks)
    
    elif choice == '3':
        save_buy_stock()
    
    elif choice == "4":
        my_stocks = read_tickets()
        plot_my_stocks(my_stocks)

def main():
    stocks = get_all_stocks()
    my_stocks = []
    while menu(stocks, my_stocks) != 0:
        pass




if __name__ == "__main__":
    main()