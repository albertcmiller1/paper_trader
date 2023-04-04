import argparse
import sys
from trader import Trader

def main() -> int: 
    if not sys.argv[1:]: print("please use the -h or --help option to get started")
    user, list_portfolio, buy_stock, sell_stock, quantity, graph_portfolio, graph_stock = parse_app_args()
    print(f"welcome {user}!")


    # print(list_portfolio)


    # trader = Trader('BABA')
    # df = trader.get_stocks('1wk')
    # trader.get_and_write_to_csv("1d")
    # df = trader.get_from_csv("stock_csvs/BABA_1d.csv")
    # trader.add_moving_average(df, 50)
    # trader.plot_(df, ('high', 'g'), ('low', 'r'), ('50ma', 'b'))
    # trader.plot_volume(df)
    # trader.plot(df, ('high', 'g'))
    # print(df.head())
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

    args = parser.parse_args()

    if args.buy_stock or args.sell_stock or args.quantity: 
        if not ((args.buy_stock and args.quantity) or (args.sell_stock and args.quantity)): 
            print("if you're buying or selling a stock, you must specify a quantity and ticker")
            sys.exit()

    return args.user, args.list_portfolio, args.buy_stock, args.sell_stock, args.quantity, args.graph_portfolio, args.graph_stock


if __name__ == "__main__": 
    main()