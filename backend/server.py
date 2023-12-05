from flask import Flask
from trader import Trader
from flask_cors import CORS
import json 

app = Flask(__name__)
CORS(app)

trader = Trader()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/prices")
def get_all_prices():
    return json.loads(trader.get_price_history())

