import argparse
import sys
import pprint
from trader import Trader
from parse_conf import Env
from datetime import datetime as dt

def main() -> int: 
    if not sys.argv[1:]: print("please use the -h or --help option to get started")
    user, list_portfolio, buy_stock, sell_stock, quantity, graph_portfolio, graph_stock, list_txns = parse_app_args()
    print(f"welcome {user}!\n")

    use_csvs = True
    list_transactions = False
    trader = Trader()

    if list_portfolio: 
        user_transactions = trader.get_user_transactions(user)
        if user_transactions.empty: 
            print(f"{user} does not have any stocks yet!")
            return 
        user_holdings = trader.create_portfolio(user_transactions)
        print('holdings: ')
        pprint.pprint(user_holdings)

    elif buy_stock: 
        print(f'attempting to buy {quantity} shares of {buy_stock}')
        if trader.buy_stock(user, buy_stock, quantity): print("success!")
        
    elif sell_stock: 
        print(f'attempting to sell {quantity} shares of {sell_stock}')
        if trader.sell_stock(user, sell_stock, int(quantity)): print('success!')

    elif graph_portfolio: 
        '''
        from the time of the first purchase til now ...
            > calculate gain/loss for each day for each stock 
            > aggregate gains/losses into dataframe 
            > y = value_of_portfolio + gain
        '''

        stock_dfs = trader.get_and_trim_stock_data(user, use_csvs)
        user_transactions = trader.get_user_transactions(user) 

        for ticker in stock_dfs: 
            print(f"calculating profits for {ticker}")

            user_txns_of_x_ticker = user_transactions.loc[(user_transactions['ticker'] == ticker)]

            # print(user_txns_of_x_ticker.head(10))
            print(f"{user} has {len(user_txns_of_x_ticker.index)} transactions for {ticker}")
            print("\n")


            user_txn_index = 0
            num_shares = 0
            for _, row in stock_dfs[ticker].iterrows():

                stock_history_date = dt.fromtimestamp(row['date_utc']).date()
                user_txn_date = user_txns_of_x_ticker.iloc[user_txn_index]['date'].to_pydatetime().date()

                if stock_history_date == user_txn_date:
                    # print(f"user transaction occurrd here on date: {stock_history_date}")
                    # print(f"{user} owns {num_shares} share of {ticker}")
                    # print(user_txns_of_x_ticker.iloc[user_txn_index])
                    # print("\n")

                    if user_txns_of_x_ticker.iloc[user_txn_index]['transaction_type'] == 'buy':
                        num_shares += user_txns_of_x_ticker.iloc[user_txn_index]['quantity']
                    elif user_txns_of_x_ticker.iloc[user_txn_index]['transaction_type'] == 'sell':
                        num_shares -= user_txns_of_x_ticker.iloc[user_txn_index]['quantity']
                    else: print("???")
                    
                    # print(f"{user} owns {num_shares} share of {ticker}")
                    # print("\n")

                    if user_txn_index <= len(user_txns_of_x_ticker.index) - 2:
                        user_txn_index += 1


                days_gain = row['open'] - row['close']
                user_profit = days_gain * num_shares
                print(user_profit)


            # if user_txn_index != len(user_txns_of_x_ticker.index):
            #     print("???")
            #     print(f"user_txn_index: {user_txn_index}")
            #     print(f"len user txns: {len(user_txns_of_x_ticker.index)}")



        print("\n")
        # print(stock_dfs["TSLA"].head(10))




    elif graph_stock: 
        print(f"graphing {graph_stock}...")
        # df = trader.get_from_csv("stock_csvs/AAPL_1d.csv")
        df = trader.get_stock_data('AAPL', '1d')
        df = trader.add_moving_average(df, 50)
        # trader.plot_volume(df)
        trader.plot(df, ('high', 'g'), ('low', 'r'), ('50ma', 'b'))
   
    elif list_txns: 
        user_transactions = trader.get_user_transactions(user)
        # find how many rows are in df and use that instead of hardcoding 
        print(df.head(100))
   
    else: 
        print('please use the -h or --help option to list out some of the availiable features of this repository.')

    return 0


def parse_app_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", help="use this flag to tell the program your user_id. this is needed to track which stocks you own.", required=True)
    parser.add_argument("--list_portfolio", help="use this flag to list out what socks you currently own and how much they are worth", action='store_true') 
    parser.add_argument("--buy_stock", help="use this flag to buy a stock. must pass in the ticker after the flag")
    parser.add_argument("--sell_stock", help="use this flag to sell a stock. must pass in the ticker after the flag")
    parser.add_argument("--quantity", help="use this flag to specify how many shares of a stock you would like to buy or sell. must pass in an integer after the flag.")
    parser.add_argument("--graph_portfolio", help="use this flag to graph your current portfolio", action='store_true')
    parser.add_argument("--graph_stock", help="use this flag to graph any stock. must pass in the ticker you would like to see")
    parser.add_argument("--list_txns", help="use this flag to list all the transactions of a user.")
    parser.add_argument("--no_csvs", help="by default, the program will download csvs of the stock data so less api calls will be made. use this flag to prevent downloading csv files and only use the stock api.")

    args = parser.parse_args()

    if args.buy_stock or args.sell_stock or args.quantity: 
        if not ((args.buy_stock and args.quantity) or (args.sell_stock and args.quantity)): 
            print("if you're buying or selling a stock, you must specify a ticker and quantity")
            sys.exit()

    return args.user, args.list_portfolio, args.buy_stock, args.sell_stock, args.quantity, args.graph_portfolio, args.graph_stock, args.list_txns

if __name__ == "__main__": 
    main()
