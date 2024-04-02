'''
this will be a socket that is constantly listening to the output of the order book's socket 
as the orderbook outputs a match of a real user, this socket will post to an AWS db to record transactions 

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
'''

import requests, json, websocket, ast, boto3, uuid, sys

# from database.models import Match
from database.db_service import DB_Service, Match

db = DB_Service()

def parse_message(wsapp, message):
    res = ast.literal_eval(message)
    print(res)


    match = Match(
        res["match_id"],
        res["buying_order_id"],
        res["selling_order_id"],
        int(res["sale_quantity"]),
        float(res["sale_price"])
    )
    
    print(
        res["match_id"],
        res["buying_order_id"],
        res["selling_order_id"],
        int(res["sale_quantity"]),
        float(res["sale_price"])
    )

    
    db.insert(match)


HOST="ws://0.0.0.0:5001"
wsapp = websocket.WebSocketApp(f"{HOST}/matches", on_message=parse_message)
wsapp.run_forever() 