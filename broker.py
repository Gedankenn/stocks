#!/usr/bin/env python3
'''
This is the main script that will run the broker.
Author: Fabio Slika Stella
Date: 2024-09-05

'''


import stocks as st
from bcolors import bcolors
import sys


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
    print(f"{bcolors.ENDC}\n\n\n")
    
    key = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter your choice: {bcolors.ENDC}")
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
        buy_date = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the buy date: {bcolors.ENDC}")
    else:
        stock = args[2]
        quantity = args[3]
        buy_price = args[4]
        buy_date = args[5]

    stocks.append(st.Stock(stock, quantity, buy_price, buy_date))

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
    elif option == "-m":
        print("Showing the main menu")
    elif option == "-q":
        save_my_stocks(stocks)
        print("Quitting the broker")
    else:
        print("Invalid option")
        sys.exit(1)

def menu(args):
    '''
        The main menu will be here
        @param args: The arguments
    '''
    option = "-q"
    if len(args) <= 1:
        menu_helper()
        option = menu_listing()
        args = ''

    elif len(args) >= 2:
        option = args[1]
    
    if args[1] == "-h": 
        menu_helper()
        sys.exit(0)
    
    else:
        stocks = load_my_stocks()
        menu_navigation(option, stocks, args)
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
    print(f"{bcolors.ENDC}\n\n\n")



def main():
    '''
        The main function will be here
    '''
    banner()
    args = sys.argv
    menu(args)

if __name__ == "__main__":
    main()
