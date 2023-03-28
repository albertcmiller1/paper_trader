import requests
import json
import pprint
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib import style 
import datetime as dt 
from parse_conf import Env


class Trader: 
    def __init__(self, stock='AAPL'):
        self.conf = Env("configuration.yaml").config

        self.url = f"https://yahoo-finance15.p.rapidapi.com/api/yahoo/hi/history/{stock}/15m"
        self.querystring = {"diffandsplits":"false"}
        self.headers = {
            "X-RapidAPI-Key": self.conf['api_key'],
            "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
        }

    def get_stocks(self):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
        dic = json.loads(response.text)

        stocks_arr = []
        for stock in dic["items"]:
            stocks_arr.append(dic["items"][stock])

        return pd.DataFrame(stocks_arr)

    def get_and_write_to_csv(self, file_name):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
        dic = json.loads(response.text)

        stocks_arr = []
        for stock in dic["items"]:
            stocks_arr.append(dic["items"][stock])

        df = pd.DataFrame(stocks_arr)
        df.to_csv(file_name, index=True, index_label='index')
        return True 

    def get_from_csv(self, csv_file):
        return pd.read_csv(csv_file, parse_dates=True, index_col=0)

    def plot(self, df, *args):
        style.use('ggplot')

        for key in args:
            plt.plot(df["date"], df[key[0]], key[1], label=key[0])
        
        plt.title("Stonks")
        plt.xlabel('date')
        plt.ylabel('price')
        plt.legend()
        plt.show()
    
    def add_moving_average(self, df, size):
        ma_name = str(size) + "ma" # ex) 50ma
        df[ma_name] = df['close'].rolling(window=size, min_periods=0).mean()
        df.dropna(inplace=True) # removes the entire row of all rows that have NaN
        return df



trader = Trader('TSLA')
# df = trader.get_stocks()
# trader.get_and_write_to_csv("stock_csvs/tsla.csv")
df = trader.get_from_csv("stock_csvs/apple.csv")
trader.add_moving_average(df, 50)
trader.plot(df, ('high', 'g'), ('low', 'r'), ('50ma', 'b'))

print(df.head())
