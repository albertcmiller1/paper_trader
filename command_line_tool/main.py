from args import set_app_args
from trader import Trader

import requests, json, websocket, ast

def main(): 
    args = set_app_args()
    trader = Trader()

    if args.stream_matches: 
        trader.stream_matches(args.stream_matches)

    if args.stream_spread: 
        trader.stream_spread(args.stream_spread)

    return 

main()


if __name__ == "__main__": 
    main()

