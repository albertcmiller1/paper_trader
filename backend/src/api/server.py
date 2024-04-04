from flask import Flask
from flask_cors import CORS
import sys, json 
sys.path.append("..")
from database.db_service import DB_Service

app = Flask(__name__)
CORS(app)
db = DB_Service()

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/prices")
def get_all_prices():
    return db.select("PRICE_HISTORY")

@app.route("/matches")
def get_all_matches():
    return db.select("MATCH_HISTORY")
