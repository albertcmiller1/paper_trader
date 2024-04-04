from args import set_app_args
from trader import Trader
from database.db_service import DB_Service

def main(): 
    args    = set_app_args()
    trader  = Trader()
    db      = DB_Service()

    if args.stream_matches: 
        trader.stream_matches(args.stream_matches)

    if args.curr_price: 
        trader.get_curr_price()

    elif args.stream_spread: 
        trader.stream_spread(args.stream_spread)

    elif args.stream_price: 
        trader.stream_curr_price(args.stream_price)

    elif args.buy: 
        trader.place_order(float(args.price), int(args.quantity), "buy", args.user)

    elif args.sell: 
        trader.place_order(float(args.price), int(args.quantity), "sell", args.user)

    elif args.list_txns: 
        db.select("MATCH_HISTORY")

    elif args.price_history: 
        db.select("PRICE_HISTORY")

    else: 
        print("Invalid arguments.") 
    
if __name__ == "__main__": 
    main()

