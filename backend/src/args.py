import argparse, sys
from models import Args

def set_app_args(): 
    if not sys.argv[1:]: 
        print("please use the -h or --help option to get started\n")
        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("--buy",                help="use this flag to buy a stock. must pass in the ticker after the flag")
    parser.add_argument("--sell",               help="use this flag to sell a stock. must pass in the ticker after the flag")
    parser.add_argument("--user",               help="use this flag to tell the program your user_id. this is needed to track which stocks you own.", required=True)
    parser.add_argument("--price",              help="use this flag to specify the price you are willing to bid/ask")
    parser.add_argument("--quantity",           help="use this flag to specify how many shares of a stock you would like to buy or sell. must pass in an integer after the flag.")
    parser.add_argument("--stream_spread",      help="use this flag to create a socket connection to the orderbook. must pass in the ticker after the flag.")
    parser.add_argument("--stream_matches",     help="use this flag to create a socket connection to the orderbook. must pass in the ticker after the flag.")
    parser.add_argument("--curr_price",         help="use this flag to return the current trading price of a stock. must pass in the ticker after the flag.")
    parser.add_argument("--list_txns",          help="use this flag to list all the transactions of a user. must pass in the ticker after the flag.")
    parser.add_argument("--price_history",      help="use this flag to list all the transactions of a user. must pass in the ticker after the flag.")
    parser.add_argument("--stream_price",       help="use this flag to create a socket connection to the orderbook. must pass in the ticker after the flag.")
    parser.add_argument("--post_matches",       help="use this flag to post streamed matches into the local db. must pass in the ticker after the flag.")
    parser.add_argument("--post_prices",        help="use this flag to post streamed prices into the local db. must pass in the ticker after the flag.")
    
    parser.add_argument("--portfolio",          help="use this flag to list out what socks you currently own and how much they are worth", action='store_true') 
    parser.add_argument("--graph_stock",        help="use this flag to graph any stock. must pass in the ticker you would like to see")
    parser.add_argument("--graph_portfolio",    help="use this flag to graph your current portfolio", action='store_true')

    args = parser.parse_args()
    if (args.buy or args.sell or args.quantity) and not (args.quantity and (args.buy or args.sell) and args.price): 
        print("if you're buying or selling a stock, you must specify a ticker, quantity and purchace price")
        sys.exit()

    Args.buy                = args.buy
    Args.post_matches       = args.post_matches
    Args.post_prices        = args.post_prices
    Args.sell               = args.sell
    Args.user               = args.user
    Args.price              = args.price
    Args.stream_matches     = args.stream_matches
    Args.stream_spread      = args.stream_spread
    Args.stream_price       = args.stream_price
    Args.price_history      = args.price_history
    Args.curr_price         = args.curr_price
    Args.quantity           = args.quantity
    Args.list_txns          = args.list_txns
    Args.portfolio          = args.portfolio
    Args.graph_stock        = args.graph_stock
    Args.graph_portfolio    = args.graph_portfolio

    print(f"welcome {Args.user}!\n")
    return Args