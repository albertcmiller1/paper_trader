import requests, json
from models import Order

class Trader: 
    def __init__(self, conf):
        self.conf = conf
    
    def place_order(self, order: Order):
        url = self.conf["local"]["api"]["place_order_route"]
        order = {
            'price': order.price,
            'shares': order.quantity,
            'order_type': order.order_type,
            'user_id': order.user_id
        }
        response = requests.post(url, json=order)
        res_dict = json.loads(response.text)
        print(res_dict)

