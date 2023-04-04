import requests
import json
import pprint
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib import style 
import datetime as dt 
from parse_conf import Env
from datetime import datetime as dt
from matplotlib import dates as mdates


class Trader: 
    def __init__(
            self, 
            stock="AAPL"
        ):
        self.conf = Env("configuration.yaml").config
        self.stock = stock
        self.url = self.conf['stock_url'] + self.stock
        self.querystring = {"diffandsplits":"false"}
        self.headers = {
            "X-RapidAPI-Key": self.conf['api_key'],
            "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
        }

    def get_stocks(self, time_interval: str) -> pd.DataFrame:
        if time_interval not in  ["5m", "15m", "30m", "1h", "1d", "1wk", "1mo", "3mo"]:
            return False
        
        url = self.url + "/" + time_interval
        response = requests.request("GET", url, headers=self.headers, params=self.querystring)
        dic = json.loads(response.text)

        stocks_arr = []
        for stock in dic["items"]:
            stocks_arr.append(dic["items"][stock])

        return pd.DataFrame(stocks_arr)

    def get_and_write_to_csv(self, time_interval) -> bool:
        file_name = "stock_csvs/" + self.stock + "_" +time_interval + ".csv"
        df = self.get_stocks(time_interval)
        df.to_csv(file_name, index=True, index_label='index')
        return True 

    def get_from_csv(self, csv_file) -> pd.DataFrame:
        return pd.read_csv(csv_file, parse_dates=True, index_col=0)

    def plot(self, df, *args) -> None:
        style.use('ggplot')

        for key in args:
            plt.plot(df["date"], df[key[0]], key[1], label=key[0])
        
        plt.title("Stonks")
        plt.xlabel('date')
        plt.ylabel('price')
        plt.legend()
        plt.show()

    def plot_volume(self, df, *args) -> None:
        style.use('ggplot')

        ax1 =  plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 =  plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

        ax1.plot(df['date'], df['high'], 'g')
        ax1.plot(df['date'], df['low'], 'r')
        ax1.plot(df['date'], df['50ma'], 'b')
        ax2.bar(df['date'], df['volume'])

        plt.show()
    
    def add_moving_average(self, df, size) -> pd.DataFrame:
        ma_name = str(size) + "ma" # ex) 50ma
        df[ma_name] = df['close'].rolling(window=size, min_periods=0).mean()
        df.dropna(inplace=True) # removes the entire row of all rows that have NaN
        return df



