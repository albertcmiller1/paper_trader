from models import Order
from trader import Trader
from args import set_app_args
from configs.conf import load_conf
from database.db_service import DB_Service
from order_book_service import OrderBookService

def main(): 
    conf    = load_conf("./configs/conf.yaml")
    args    = set_app_args()
    trader  = Trader(conf)
    dbs     = DB_Service()
    obs     = OrderBookService(conf)

    if args.stream_matches: 
        obs.stream_matches(args.stream_matches)
    elif args.post_matches: 
        obs.post_matches_to_db(dbs, args.post_matches)
    elif args.post_prices: 
        obs.post_prices_to_db(dbs, args.post_prices)
    elif args.curr_price: 
        print(f"{args.curr_price}: {obs.get_curr_price(args.curr_price)}")
    elif args.stream_spread: 
        obs.stream_spread(args.stream_spread)
    elif args.stream_price: 
        obs.stream_curr_price(args.stream_price)
    elif args.buy: 
        trader.place_order(
            Order(
                float(args.price), 
                int(args.quantity), 
                "buy", 
                args.user
            )
        )
    elif args.sell: 
        trader.place_order(
            Order(
                float(args.price), 
                int(args.quantity), 
                "sell", 
                args.user
            )
        )
    elif args.list_txns: 
        print(dbs.select("MATCH_HISTORY"))
    elif args.price_history: 
        print(dbs.select("PRICE_HISTORY"))
    else: 
        print("Invalid arguments.") 
    
if __name__ == "__main__": 
    main()

