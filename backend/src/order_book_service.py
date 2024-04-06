import requests, json, websocket, ast
from database.db_service import Match, Price, DB_Service

class OrderBookService:
    def __init__(self, conf):
        self.conf = conf

    def get_curr_price(self, ticker: str):
        url = self.conf["local"]["api"]["current_price"]
        response = requests.request("GET", url)
        return json.loads(response.text)

    def stream_spread(self, ticker: str): 
        print(f"start streaming spread for {ticker}\n")
        def on_message(wsapp, message):
            for s in message.split(" "): 
                if not s: continue 
                price, order_type = s.split("-")[0], s.split("-")[1]
                print(f"{price} {order_type}")
            print()
        self.stream(on_message, self.conf["local"]["ws"]["spread"])

    def stream_curr_price(self, ticker: str): 
        print(f"start streaming current price for {ticker}\n")
        def on_message(wsapp, message):
            print(message)
        self.stream(on_message, self.conf["local"]["ws"]["curr_price"])

    def stream_matches(self, ticker: str): 
        print(f"start streaming {ticker} matches for {ticker}\n")
        def on_message(wsapp, message):
            result = ast.literal_eval(message)
            print(f"{result}")
        self.stream(on_message, self.conf["local"]["ws"]["matches"])

    def post_matches_to_db(self, db: DB_Service, ticker: str): 
        print(f"start posting {ticker} matches to db")
        def on_message(wsapp, message):
            res = ast.literal_eval(message)
            match = Match(
                res["match_id"],
                res["buying_order_id"],
                res["selling_order_id"],
                int(res["sale_quantity"]),
                float(res["sale_price"])
            )
            db.insert(match)
        self.stream(on_message, self.conf["local"]["ws"]["matches"])

    def post_prices_to_db(self, db: DB_Service, ticker: str): 
        print(f"start posting {ticker} prices to db")
        def on_message(wsapp, message):
            res = ast.literal_eval(message)
            print(res)
            p = Price(
                res['date_time'],
                ticker,
                res['curr_price']
            )
            db.insert(p)
        self.stream(on_message, self.conf["local"]["ws"]["curr_price"])


    def stream(self, todo, url):
        wsapp = websocket.WebSocketApp(url, on_message=todo)
        wsapp.run_forever() 
