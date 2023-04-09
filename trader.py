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
import pprint


class Trader: 
    def __init__(self):
        self.conf = Env("configuration.yaml").config
        # self.url = self.conf['stock_url'] + self.stock
        self.url = self.conf['stock_url']
        self.querystring = {"diffandsplits":"false"}
        self.headers = {
            "X-RapidAPI-Key": self.conf['api_key'],
            "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
        }

    def get_stock_data(self, time_interval: str) -> pd.DataFrame:
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
        file_name = "stock_csvs/" + self.stock + "_" + time_interval + ".csv"
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

        plt.title("Stonks")
        plt.xlabel('date')
        plt.ylabel('price')
        plt.legend()
        plt.show()
    
    def add_moving_average(self, df, size) -> pd.DataFrame:
        ma_name = str(size) + "ma" # ex) 50ma
        df[ma_name] = df['close'].rolling(window=size, min_periods=0).mean()
        df.dropna(inplace=True) # removes the entire row of all rows that have NaN
        return df

    def get_current_price(self, ticker): 
        print("getting current price")

    def buy_stock(self, user_id, ticker, quantity) -> int:
        time = dt.now()
        date_time_str = time.strftime('%m/%d/%Y %H:%M:%S')
        post_url = self.conf['aws_api'] + '/product'

        curr_price = "143.32"

        payload = {
            "productId": "007", # need to take this out from template.yaml
            "user_id": user_id, 
            "ticker": ticker, 
            "quantity": quantity, 
            "date": date_time_str, 
            "transaction_type": "buy", 
            "price": curr_price
        }

        response = requests.post(post_url, json = payload)
        # print(response.text)
        return 0

    def sell_stock(self, user_id, stock, quantity):
        '''
        on second thought: thats not really an issue. 
        this will just create the transaction 

        when choosing a stock to sell...
        first check the quantity of that stock the user holds to validate you can sell
        if the user doesnt want to liquidate all of his/her shares...
        start at oldest transaction and sell that first. 
        '''
        time = dt.now()
        date_time_str = time.strftime('%m/%d/%Y %H:%M:%S')
        # datetime_object = dt.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')

        payload = {
            "productId": "007", # need to take this out from template.yaml
            "user_id": user_id, 
            "ticker": stock, 
            "quantity": quantity, 
            "date": date_time_str, 
            "transaction_type": "buy", 
            "price": "143.32"
        }





    def get_user_transactions(self, user) -> pd.DataFrame: 
        '''
        returns a dataframe of a user's transactions
        '''
        get_url = self.conf['aws_api'] + '/products'
        response = requests.get(get_url)
        stocks = json.loads(response.text)['products']['Items']

        stocks_arr = []
        for stock in stocks:
            stocks_arr.append(stock)

        df = pd.DataFrame(stocks_arr)

        return df.loc[df['user_id'] == user]

    def create_portfolio(self, transactions): 
        '''
        take in a df of all a user's transactions
        return a df of their portfolio 
        '''

        print(transactions["ticker"].unique())
        stocks = transactions["ticker"].unique()

        # for stock in stocks: 







    # def create_portfolio_arr(self, stocks):
    #     # find each unique 
  


    #   x



# trader = Trader()
# df = trader.get_stocks('1wk')
# trader.get_and_write_to_csv("1d")
# df = trader.get_from_csv("stock_csvs/BABA_1d.csv")

# trader.add_moving_average(df, 50)
# trader.plot_(df, ('high', 'g'), ('low', 'r'), ('50ma', 'b'))
# trader.plot_volume(df)
# trader.plot(df, ('high', 'g'))
# print(df.head())
