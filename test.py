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

        print(self.conf)
        print("\n")

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
        df.to_csv(file_name)
        return True 

    def get_from_csv(self, csv_file):
        return pd.read_csv(csv_file, parse_dates=True, index_col=0)

    def plot(self, df):
        style.use('ggplot')
        df['high'].plot()
        plt.show()
    
    def add_moving_average(self, df, size):
        name = str(size) + "ma"
        df[name] = df['close'].rolling(window=size, min_periods=0).mean()
        df.dropna(inplace=True) # removes the entire row of all rows that have NaN
        return df



trader = Trader('TSLA')
df = trader.get_stocks()


# trader.get_and_write_to_csv("tesla.csv")
# df = trader.get_from_csv("tesla.csv")
# trader.plot(df)
# trader.add_moving_average(df, 50)

print(df.head())
print(df.tail())
