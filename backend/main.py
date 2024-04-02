from args import set_app_args
from trader import Trader

def main(): 
    args = set_app_args()
    trader = Trader()

    if args.stream_matches: 
        trader.stream_matches(args.stream_matches)

    if args.stream_spread: 
        trader.stream_spread(args.stream_spread)

    # works
    if args.buy: 
        trader.place_order(float(args.price), int(args.quantity), "buy", args.user)

    # works 
    if args.sell: 
        trader.place_order(float(args.price), int(args.quantity), "sell", args.user)

if __name__ == "__main__": 
    main()

