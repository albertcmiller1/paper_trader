import argparse, sys, pprint 
import pandas as pd
from trader import Trader
from parse_conf import Env
from datetime import datetime as dt
from singleton_decorator import singleton

@singleton
class Args: 
    user: str
    list_portfolio: bool
    buy_stock: str
    sell_stock: str
    quantity: int 
    graph_portfolio: bool
    graph_stock: str 
    list_txns: bool 
    no_csvs: bool 
    stream: str 
    curr_price: str 

def main() -> int: 
    if not sys.argv[1:]: 
        print("please use the -h or --help option to get started\n")
        return 
    set_app_args()
    print(f"welcome {Args.user}!\n")

    use_csvs = True
    time_intveral = "1d"
    trader = Trader()

    if Args.list_portfolio: 
        user_transactions: pd.DataFrame = trader.get_user_transactions(Args.user)
        if user_transactions.empty: 
            print(f"{Args.user} does not have any stocks yet!")
            return 
        user_holdings = trader.create_portfolio(user_transactions)
        print('holdings: ')
        pprint.pprint(user_holdings)

    elif Args.buy_stock: 
        print(f'attempting to buy {Args.quantity} shares of {Args.buy_stock}')
        if trader.buy_stock(Args.user, Args.buy_stock, Args.quantity): print("success!")
        else: print("failure...")
        
    elif Args.sell_stock: 
        print(f'attempting to sell {Args.quantity} shares of {Args.sell_stock}')
        if trader.sell_stock(Args.user, Args.sell_stock, int(Args.quantity)): print('success!') 
        else: print(':(')

    elif Args.stream: 
        print(f"starting to stream {Args.stream} from orderbook")
        trader.stream_live_stock_data("TSLA")


    elif Args.graph_portfolio: 
        stock_dfs = trader.get_and_trim_stock_data(Args.user, use_csvs)
        user_transactions = trader.get_user_transactions(Args.user) 
        value_dfs = trader.create_value_dataframes(stock_dfs, user_transactions)

        for df in value_dfs: 
            print(df)
            print(value_dfs[df].head()) 
            # aggregate each of these dataframes 
            # will need to be careful of dates across different stocks 
            # plot 
            trader.plot(value_dfs[df], ('value', 'g'))

    elif Args.graph_stock: 
        print(f"graphing {Args.graph_stock}...")
        if trader.stock_is_in_csv_files(Args.graph_stock, "1d"):
            file_name = Args.graph_stock + "_" + time_intveral + ".csv"
            df = trader.get_stock_data_from_csv("stock_csvs/" + file_name.lower())
        else: 
            df = trader.get_and_write_to_csv(Args.graph_stock, '1d')
        df = trader.add_moving_average(df, 50)
        trader.plot(df, ('high', 'g'), ('low', 'r'), ('50ma', 'b'))
   
    elif Args.list_txns: 
        user_transactions = trader.get_user_transactions(Args.user)
        num_user_txns = len(user_transactions.index)
        print(user_transactions.head(num_user_txns))
   
    else: 
        print('please use the -h or --help option to list out some of the availiable features of this repository.')

    return 0


def set_app_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", help="use this flag to tell the program your user_id. this is needed to track which stocks you own.", required=True)
    parser.add_argument("--stream", help="use this flag to create a socket connection to the orderbook. must pass in the ticker after the flag.")
    parser.add_argument("--no_csvs", help="by default, the program will download csvs of the stock data so less api calls will be made. use this flag to prevent downloading csv files and only use the stock api.", action='store_true')
    parser.add_argument("--quantity", help="use this flag to specify how many shares of a stock you would like to buy or sell. must pass in an integer after the flag.")
    parser.add_argument("--list_txns", help="use this flag to list all the transactions of a user.", action='store_true')
    parser.add_argument("--buy_stock", help="use this flag to buy a stock. must pass in the ticker after the flag")
    parser.add_argument("--curr_price", help="use this flag to return the current trading price of a stock. must pass in the ticker after the flag.")
    parser.add_argument("--sell_stock", help="use this flag to sell a stock. must pass in the ticker after the flag")
    parser.add_argument("--graph_stock", help="use this flag to graph any stock. must pass in the ticker you would like to see")
    parser.add_argument("--list_portfolio", help="use this flag to list out what socks you currently own and how much they are worth", action='store_true') 
    parser.add_argument("--graph_portfolio", help="use this flag to graph your current portfolio", action='store_true')

    args = parser.parse_args()

    if args.buy_stock or args.sell_stock or args.quantity: 
        if not ((args.buy_stock and args.quantity) or (args.sell_stock and args.quantity)): 
            print("if you're buying or selling a stock, you must specify a ticker and quantity")
            sys.exit()

    Args.user = args.user
    Args.stream = args.stream
    Args.quantity = args.quantity
    Args.list_txns = args.list_txns
    Args.buy_stock = args.buy_stock
    Args.sell_stock = args.sell_stock
    Args.graph_stock = args.graph_stock
    Args.list_portfolio = args.list_portfolio
    Args.graph_portfolio = args.graph_portfolio

if __name__ == "__main__": 
    main()
