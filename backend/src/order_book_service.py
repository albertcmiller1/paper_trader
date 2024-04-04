import requests, json, websocket, ast, pprint

class OrderBookService:
    def __init__(self, conf):
        self.conf = conf

    def get_curr_price(self):
        url = self.conf["local"]["api"]["current_price"]
        response = requests.request("GET", url)
        return json.loads(response.text)

    def stream_spread(self, ticker): 
        print(f"start streaming spread for {ticker}\n")
        def on_message(wsapp, message):
            for s in message.split(" "): 
                if not s: continue 
                price, order_type = s.split("-")[0], s.split("-")[1]
                print(f"{price} {order_type}")
            print()
        self.stream(on_message, self.conf["local"]["ws"]["spread"])

    def stream_curr_price(self, ticker): 
        print(f"start streaming current price for {ticker}\n")
        def on_message(wsapp, message):
            print(message)
        self.stream(on_message, self.conf["local"]["ws"]["curr_price"])

    def stream_matches(self, ticker): 
        print(f"start streaming matches for {ticker}\n")
        def on_message(wsapp, message):
            result = ast.literal_eval(message)
            print(f"{result}")
        self.stream(on_message, self.conf["local"]["ws"]["matches"])

    def stream(self, todo, url):
        wsapp = websocket.WebSocketApp(url, on_message=todo)
        wsapp.run_forever() 
