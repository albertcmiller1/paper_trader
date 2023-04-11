import requests
import json
import uuid
import pprint
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib import style 
import datetime as dt 
from parse_conf import Env
from datetime import datetime as dt
from matplotlib import dates as mdates


class Trader: 
    def __init__(self):
        self.conf = Env("configuration.yaml").config
        self.stock_quote_url = self.conf['stock_quote_url']
        self.history_url = self.conf['stock_history_url']
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
        stocks = self.get_stocks(time_interval)
        file_name = "stock_csvs/" + self.stock + "_" + time_interval + ".csv"
        stocks.to_csv(file_name, index=True, index_label='index')
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

    def get_current_price(self, ticker) -> float: 
        print("getting current price...")
        url = self.stock_quote_url + "/" + ticker
        response = requests.request("GET", url, headers=self.headers, params=self.querystring)
        curr_stock_data = json.loads(response.text)

        # print('response from getting quote: ')
        # pprint.pprint(curr_stock_data[0]['ask'])

        return float(curr_stock_data[0]['ask'])

    def buy_stock(self, user_id, ticker, quantity) -> int:
        time = dt.now()
        date_time_str = time.strftime('%m/%d/%Y %H:%M:%S')
        post_url = self.conf['aws_api'] + '/product'
        txn_id = str(uuid.uuid4())

        curr_price = "143.32"
        payload = {
            "productId": txn_id, # need to take this out from template.yaml
            "user_id": user_id, 
            "ticker": ticker, 
            "quantity": int(quantity), 
            "date": date_time_str, 
            "transaction_type": "buy", 
            "price": curr_price
        }

        response = requests.post(post_url, json = payload)
        return 0

    def sell_stock(self, user_id, ticker, quantity_to_sell) -> bool:
        '''
        post a sell order to the tansactions database
        '''
        user_transactions = self.get_user_transactions(user_id)

        shares_bought = user_transactions.loc[(user_transactions['ticker'] == ticker) & (user_transactions['transaction_type'] == 'buy')]['quantity'].sum()
        shares_sold = user_transactions.loc[(user_transactions['ticker'] == ticker) & (user_transactions['transaction_type'] == 'sell')]['quantity'].sum()
        shares_held = shares_bought - shares_sold

        if shares_held < quantity_to_sell: 
            print(f"{user_id} is trying to sell {quantity_to_sell} shares of {ticker} but only owns {shares_held}")
            return False

        txn_id = str(uuid.uuid4())
        time = dt.now()
        date_time_str = time.strftime('%m/%d/%Y %H:%M:%S')
        post_url = self.conf['aws_api'] + '/product'

        # datetime_object = dt.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')

        curr_price = self.get_current_price(ticker)
        payload = {
            "productId": txn_id, # need to take this out from template.yaml
            "user_id": user_id, 
            "ticker": ticker, 
            "quantity": quantity_to_sell, 
            "date": date_time_str, 
            "transaction_type": "sell", 
            "price": str(curr_price)
        }

        response = requests.post(post_url, json = payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Error posting sell order: {e}")
        return True

    def get_user_transactions(self, user: str) -> pd.DataFrame: 
        '''
        returns a dataframe of a user's transactions
        '''
        get_url = self.conf['aws_api'] + '/products'
        response = requests.get(get_url)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Error fetching user transactions: {e}")

        txns_df = pd.DataFrame(json.loads(response.text)['products']['Items'])
        txns_df['price'] = pd.to_numeric(txns_df['price'])
        txns_df['quantity'] = txns_df['quantity'].astype('int')
        txns_df['date'] = pd.to_datetime(txns_df['date'])
        txns_df_sorted = txns_df.sort_values(by='date')
        # print(rtn.head(10))
        # print('type: ')
        # print(type(txns_df.date[0]))

        return txns_df_sorted.loc[txns_df_sorted['user_id'] == user]

    def create_portfolio(self, transactions: pd.DataFrame): 
        '''
        take in a df of all a user's transactions
        return a df of their portfolio 
        '''

        '''
        note: 

        when choosing a stock to sell...
        first check the quantity of that stock the user holds to validate you can sell
        if the user doesnt want to liquidate all of his/her shares...
        start at oldest transaction and sell that first. 
        '''
        print(transactions.head(10))
        stocks_held = transactions["ticker"].unique()

        holdings = {}

        for ticker in stocks_held: 
            holdings[ticker] = {}

            # find how many shares the user holds
            shares_bought = transactions.loc[(transactions['ticker'] == ticker) & (transactions['transaction_type'] == 'buy')]['quantity'].sum()
            shares_sold = transactions.loc[(transactions['ticker'] == ticker) & (transactions['transaction_type'] == 'sell')]['quantity'].sum()
            shares_held = shares_bought - shares_sold
            holdings[ticker]['shares'] = shares_held
            # print(f"user holds {shares_held} shares of {ticker}")


            # find the current value of each stock held 
            # ticker_curr_price = self.get_current_price(ticker)

        print('holdings: ')
        print(holdings)

        holdings = {
            'AAPL': {
                'shares': 3,
                'avg cost': 253.34,
                'market value': 253.32,
                'portfolio diversity': 3.00,
                'total return': 0.02
            },
            'TSLA': {
                'shares': 3,
                'avg cost': 253.34,
                'market value': 253.32,
                'portfolio diversity': 3.00,
                'total return': 0.02
            }
        }









trader = Trader()
# value = trader.get_current_price('AAPL')





# df = trader.get_stocks('1wk')
# trader.get_and_write_to_csv("1d")
# df = trader.get_from_csv("stock_csvs/BABA_1d.csv")

# trader.add_moving_average(df, 50)
# trader.plot_(df, ('high', 'g'), ('low', 'r'), ('50ma', 'b'))
# trader.plot_volume(df)
# trader.plot(df, ('high', 'g'))
# print(df.head())
