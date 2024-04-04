import websocket, ast
import sys, json 
sys.path.append("..")
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
    db.insert(match)

if __name__ == "__main__":
    HOST="ws://0.0.0.0:5001"
    wsapp = websocket.WebSocketApp(f"{HOST}/matches", on_message=parse_message)
    wsapp.run_forever() 