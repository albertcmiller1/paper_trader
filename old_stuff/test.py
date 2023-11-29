import requests, json, websocket, ast

# https://websocket-client.readthedocs.io/en/latest/examples.html


def place_order(price, shares, order_type, user_id):
    url = "http://0.0.0.0:5001/place_order"

    # two ways to know if a user's transaction went though 
    #   1. send a URL to the book where the book can post to 
    #   2. just have the book post directly to dynamoDB

    myobj = {
        'price': price,
        'shares': shares,
        'order_type': order_type,
        'user_id': user_id
    }

    response = requests.post(url, json = myobj)
    res_dict = json.loads(response.text)
    print(res_dict)


# place_order(98, 10, "buy", "albert")
# place_order(99, 10, "buy", "albert")
# place_order(100, 10, "buy", "albert")
# place_order(101, 10, "buy", "albert")
# place_order(102, 10, "buy", "albert")
# place_order(103, 10, "buy", "albert")
# place_order(104, 10, "buy", "albert")
# place_order(105, 10, "buy", "albert")

# place_order(106, 10, "sell", "albert")
# place_order(107, 10, "sell", "albert")
# place_order(108, 10, "sell", "albert")
# place_order(109, 10, "sell", "albert")
# place_order(110, 10, "sell", "albert")
# place_order(111, 10, "sell", "albert")
# place_order(112, 10, "sell", "albert")
# place_order(113, 10, "sell", "albert")