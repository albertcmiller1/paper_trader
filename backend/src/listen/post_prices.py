import websocket, ast
import sys, json 
sys.path.append("..")
from database.db_service import DB_Service, Price

db = DB_Service()
def parse_message(wsapp, message):
    res = ast.literal_eval(message)
    print(res)
    p = Price(
        res['date_time'],
        "AAPL",
        res['curr_price']
    )
    db.insert(p)

if __name__ == "__main__":
    HOST="ws://0.0.0.0:5001"
    wsapp = websocket.WebSocketApp(f"{HOST}/price", on_message=parse_message)
    wsapp.run_forever() 