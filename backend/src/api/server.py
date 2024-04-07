from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
import sys, json, ast
sys.path.append("..")
from database.db_service import DB_Service
from configs.conf import load_conf
from trader import Trader
from models import Order

app = Flask(__name__)
CORS(app)

db      = DB_Service()
conf    = load_conf("../configs/conf.yaml")

@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/prices")
def get_all_prices():
    return db.select("PRICE_HISTORY")

@app.route("/matches")
def get_all_matches():
    return db.select("MATCH_HISTORY")

@app.route('/place_order/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def place_order(user_id):
    if request.method == 'GET':
        pass 
    if request.method == 'POST':
        res = ast.literal_eval(request.data.decode('utf-8'))
        print("res: ", res)

        new_order = Order(
            float(res["price"]),
            int(res["quantity"]),
            "buy" if res["orderType"]=="Bid" else "sell",
            user_id
        )

        print(new_order.order_type)
        print(new_order.user_id)
        print(new_order.price)
        print(new_order.quantity)

        trader = Trader(conf)
        trader.place_order(new_order)

        data = request.form
        return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= data), 200
    
    if request.method == 'DELETE':
        """delete user with ID <user_id>"""
    else:
        # POST Error 405 Method Not Allowed
        pass