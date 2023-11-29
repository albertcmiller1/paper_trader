from conf import Env
import requests, json, websocket, ast, pprint

class Trader: 
    def __init__(self):
        self.conf = Env("conf.yaml").config
    
    def stream_matches(self, ticker): 
        print(f"start streaming matches for {ticker}\n")
        def on_message(wsapp, message):
            result = ast.literal_eval(message)
            print(f"{result}")

        ws_url = self.conf["local"]["ws"]["matches"]
        wsapp = websocket.WebSocketApp(ws_url, on_message=on_message)
        wsapp.run_forever() 

    def stream_spread(self, ticker): 
        print(f"start streaming spread for {ticker}\n")
        def on_message(wsapp, message):
            arr = message.split(" ")
            for s in arr: 
                if not s: continue 
                price, order_type = s.split("-")[0], s.split("-")[1]
                print(f"price: {price}, order_type: {order_type}")
            print('\n')

        ws_url = self.conf["local"]["ws"]["spread"]
        wsapp = websocket.WebSocketApp(ws_url, on_message=on_message)
        wsapp.run_forever() 

    def get_curr_price(self):
        url = self.conf["local"]["api"]["current_price"]
        response = requests.request("GET", url)
        j = json.loads(response.text)
        print(j)

    def place_order(self, price, shares, order_type, user_id):
        url = self.conf["local"]["api"]["place_order_route"]

        myobj = {
            'price': price,
            'shares': shares,
            'order_type': order_type,
            'user_id': user_id
        }

        response = requests.post(url, json = myobj)
        res_dict = json.loads(response.text)
        print(res_dict)
