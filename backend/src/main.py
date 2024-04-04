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
    db      = DB_Service()
    obs     = OrderBookService(conf)

    if args.stream_matches: 
        obs.stream_matches(args.stream_matches)

    if args.curr_price: 
        print(obs.get_curr_price())

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
        print(db.select("MATCH_HISTORY"))

    elif args.price_history: 
        print(db.select("PRICE_HISTORY"))

    else: 
        print("Invalid arguments.") 
    
if __name__ == "__main__": 
    main()

