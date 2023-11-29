from args import set_app_args
from trader import Trader

import requests, json, websocket, ast


def main(): 
    # args = set_app_args()
    trader = Trader()
    trader.stream_matches()

    return 

main()


if __name__ == "__main__": 
    main()

