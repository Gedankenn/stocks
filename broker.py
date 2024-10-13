#!/usr/bin/env python3
'''
This is the main script that will run the broker.
Author: Fabio Slika Stella
Date: 2024-09-05

'''


import stocks as st
from bcolors import bcolors
import sys
import datetime as dt


def menu_listing():
    '''
    This function will display the main menu
    '''
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}Broker Menu{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}h{bcolors.ENDC} - Display this help menu")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}a{bcolors.ENDC} - Add a stock to the portfolio")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}r{bcolors.ENDC} - Remove a stock from the portfolio")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}l{bcolors.ENDC} - List all stocks in the portfolio")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}p{bcolors.ENDC} - Plot a stock")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}m{bcolors.ENDC} - Show the main menu")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}q{bcolors.ENDC} - Quit the broker")
    print(f"{bcolors.ENDC}")
    
    key = "-" + str(input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter your choice: {bcolors.ENDC}"))
    if key == "-q":
        sys.exit(0)

    return key

def menu_helper():
    '''
        This function will display the help menu
    '''
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}Broker Help Menu{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}broker.py -h{bcolors.ENDC}                                       - Display this help menu")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}broker.py -a <stock> <buy value> <buy date>{bcolors.ENDC}        - Add a stock to the portfolio")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}broker.py -s <stock> <sell value> <sell date>{bcolors.ENDC}      - Sell a stock from the portfolio")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}broker.py -r <stock>{bcolors.ENDC}                               - Remove a stock from the portfolio")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}broker.py -l{bcolors.ENDC}                                       - List all stocks in the portfolio")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}broker.py -p <stock> <start date> <end date>{bcolors.ENDC}       - Plot a stock")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}broker.py -m{bcolors.ENDC}                                       - Show the main menu")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}broker.py -q{bcolors.ENDC}                                       - Quit the broker")

def menu_navigation(option, stocks, args):
    '''
        This function will navigate through the options
        @param option: The option to be navigated
        @param stocks: The stocks to be navigated
        @param args: The arguments to be used
    '''
    if option == "-a":
        add_stock(stocks, args)
    elif option == "-r":
        print("Removing a stock")
    elif option == "-l":
        print_all_owned_stocks(stocks)
    elif option == "-p":
        print("Plotting a stock")
        if len(args) < 5:
            plot_stock()
        else:
            plot_stock(args[2], args[3], args[4])
    elif option == "-m":
        print("Showing the main menu")
    elif option == "-q":
        save_my_stocks(stocks)
        print("Quitting the broker")
    else:
        print("Invalid option")
        sys.exit(1)

def print_all_owned_stocks(stocks):
    '''
        This function will print all the owned stocks
        @param stocks: The stocks to be printed
    '''
    print("Listing all owned stocks")
    for stock in stocks:
        print(stock)

def load_my_stocks():
    '''
        This function will load the stocks from the file
    '''
    stocks = st.read_tickets()
    my_stocks = []
    for i in range(len(stocks["SYMBOL"])):
        my_stocks.append(st.Stock(stocks["SYMBOL"][i], stocks["QUANTITY"][i], stocks["BUY_PRICE"][i], stocks["BUY_DATE"][i], stocks["SELL_PRICE"][i], stocks["SELL_DATE"][i]))
    return my_stocks

def plot_stock(stock='', start_date='', end_date=''):
    '''
        This function will plot the stock
        @param stock: The stock to be plotted
        @param start_date: The start date
        @param end_date: The end date
    '''
    if stock == '':
        stock = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the stock symbol: {bcolors.ENDC}")
        start_date = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the start date(Y-M-D): {bcolors.ENDC}")
        if start_date == '':
            start_date = dt.date.today() - dt.timedelta(days=365)
            start_date = start_date.isoformat()
        end_date = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the end date(Y-M-D): {bcolors.ENDC}")
        if end_date == '':
            end_date = dt.date.today()
            end_date = end_date.isoformat()
    else:
        stock = stock
        start_date = start_date
        end_date = end_date

    stock = stock.upper()
    if st.is_stock_listed(stock) == False:
        print(f"{bcolors.FAIL}Stock not listed{bcolors.ENDC}")
        sys.exit(1)

    if validate_date(start_date) == False or validate_date(end_date) == False:
        print(f"{bcolors.FAIL}Invalid date{bcolors.ENDC}")
        sys.exit(1)

    stock = st.Stock(stock)
    stock.plot_stock(start_date, end_date)

def save_my_stocks(stocks):
    '''
        This function will save the stocks to the file
        @param stocks: The stocks to be saved
    '''
    st.save_tickets(stocks)

def update_history(stocks):
    '''
        This function will update the history
        @param stocks: The stocks to be updated
    '''


def is_stock_owned(stock, stocks):
    '''
        This function will verify if the stock is owned
        @param stock: The stock to be verified
        @param stocks: The stocks to be verified
        @return: True if the stock is owned, False otherwise
    '''
    for s in stocks:
        if s.symbol == stock:
            return True
    return False

def validate_date(date):
    '''
        This function will validate the date
        @param date: The date to be validated
        @return: True if the date is valid, False otherwise
    '''
    try:
        dt.date.fromisoformat(date)
        return True
    except:
        print(f"{bcolors.FAIL}Invalid date{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Date format must be Y-M-D{bcolors.ENDC}")
        return False

def add_stock(stocks, args):
    '''
        This function will add a stock to the portfolio
        @param stocks: The stocks to be added
        @param args: The arguments
    '''

    stock = ''
    quantity = ''
    buy_price = ''
    buy_date = ''

    if args == '':
        stock = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the stock symbol: {bcolors.ENDC}")
        quantity = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the quantity: {bcolors.ENDC}")
        buy_price = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the buy price: {bcolors.ENDC}")
        buy_date = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the buy date(Y-M-D): {bcolors.ENDC}")
    else:
        stock = args[2]
        quantity = args[3]
        buy_price = args[4]
        buy_date = args[5]
  
    if validate_date(buy_date) == False:
        print(f"{bcolors.FAIL}Invalid date{bcolors.ENDC}")
        sys.exit(1)

    stock = stock.upper()
    
    if is_stock_owned(stock, stocks) == True:
        print(f"{bcolors.FAIL}Stock already owned{bcolors.ENDC}")
        sys.exit(1)

    if st.is_stock_listed(stock) == False:
        print(f"{bcolors.FAIL}Stock not listed{bcolors.ENDC}")
        sys.exit(1)

    if stock == '' or quantity == '' or buy_price == '' or buy_date == '':
        print(f"{bcolors.FAIL}Invalid stock{bcolors.ENDC}")
        sys.exit(1)
    stocks.append(st.Stock(stock, quantity, buy_price, buy_date))
    print(f"{bcolors.OKGREEN}Stock added{bcolors.ENDC}")
    st.save_tickets(stocks)

def sell_stock(stocks, args):
    '''
        This function will sell a stock from the portfolio
        @param stocks: The stocks to be sold
        @param args: The arguments
    '''
    stock = ''
    sell_price = ''
    sell_date = ''

    if args == '':
        stock = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the stock symbol: {bcolors.ENDC}")
        sell_price = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the sell price: {bcolors.ENDC}")
        sell_date = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the sell date(Y-M-D): {bcolors.ENDC}")
    else:
        stock = args[2]
        sell_price = args[3]
        sell_date = args[4]

    if validate_date(sell_date) == False:
        print(f"{bcolors.FAIL}Invalid date{bcolors.ENDC}")
        sys.exit(1)

    stock = stock.upper()
    
    if is_stock_owned(stock, stocks) == False:
        print(f"{bcolors.FAIL}Stock not owned{bcolors.ENDC}")
        sys.exit(1)

    if stock == '' or sell_price == '' or sell_date == '':
        print(f"{bcolors.FAIL}Invalid stock{bcolors.ENDC}")
        sys.exit(1)
    for s in stocks:
        if s.symbol == stock:
            # Remove the stock from the list
            stocks.remove(s)
            # Add the stock to the history
            st.update_history(s)
            print(f"{bcolors.OKGREEN}Stock sold{bcolors.ENDC}")
            st.save_tickets(stocks)
            return
    print(f"{bcolors.FAIL}Stock not found{bcolors.ENDC}")


def menu(args):
    '''
        The main menu will be here
        @param args: The arguments
    '''
    option = "-q"
    if len(args) <= 1:
        option = menu_listing()
        args = ''

    elif args[1] == "-h":
        menu_helper()
        sys.exit(0)

    elif len(args) >= 2:
        option = args[1]
    
    stocks = load_my_stocks()
    while option != "-q":
        menu_navigation(option, stocks, args)
        option = menu_listing()
    sys.exit(0)

def banner():
    '''
        This function will display the banner
    '''
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}"
    "   | |__  _ __ ___ | | _____ _ __\n"
    "   | '_ \\| '__/ _ \\| |/ / _ \\ '__|\n"
    "   | |_) | | | (_) |   <  __/ |\n"
    "   |_.__/|_|  \\___/|_|\\_\\___|_|")
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}   Made by Fabio Slika Stella!{bcolors.ENDC}")
    print(f"{bcolors.ENDC}\n")



def main():
    '''
        The main function will be here
    '''
    banner()
    args = sys.argv
    menu(args)

if __name__ == "__main__":
    main()
