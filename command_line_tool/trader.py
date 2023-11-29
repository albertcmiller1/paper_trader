from conf import Env
import requests, json, websocket, ast, pprint

class Trader: 
    def __init__(self):
        self.conf = Env("conf.yaml").config
    
    def stream_matches(self): 
        def on_message(wsapp, message):
            result = ast.literal_eval(message)
            print(f"message: {result}")

        ws_url = self.conf["local"]["ws"]["matches"]
        wsapp = websocket.WebSocketApp(ws_url, on_message=on_message)
        wsapp.run_forever() 
