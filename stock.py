import investpy as inv
import yfinance as yfi
from datetime import datetime, date, timedelta
import os

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

def menu(stocks):
    clear_terminal()
    print("--------------------------------------------")
    print("MAIN - MENU")
    print("1 - Get the last month history for ticket ('Brasil only')")
    choice = input()
    if choice == '0':
        return 0
    
    if choice == '1':
        clear_terminal()
        print("--------------------------------------------")
        ticket = input("Type the ticket code: ")
        print("--------------------------------------------")
        get_last_month_history_stock(ticket)
        

def main():
    stocks = get_all_stocks()
    while menu(stocks) != 0:
        pass




if __name__ == "__main__":
    main()