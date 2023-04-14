import sys
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
        self.stock_quote_url = self.conf['rapidapi_quote_url']
        self.stock_history_url = self.conf['rapidapi_history_url']
        self.querystring = {"diffandsplits":"false"}
        self.headers = {
            "X-RapidAPI-Key": self.conf['rapidapi_api_key'],
            "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
        }

    def get_stock_data(self, stock: str, time_interval: str) -> pd.DataFrame:
        possibile_intervals = ["5m", "15m", "30m", "1h", "1d", "1wk", "1mo", "3mo"]
        if time_interval not in possibile_intervals:
            print(f'please ensure your time interval is in {possibile_intervals}')
            sys.exit()
        
        url = self.stock_history_url + "/" + stock + "/" +  time_interval
        response = requests.request("GET", url, headers=self.headers, params=self.querystring)
        dic = json.loads(response.text)

        # load direclty into df --> issue: response comes back in weird format 

        stocks_arr = []
        for stock in dic["items"]:
            stocks_arr.append(dic["items"][stock])

        return pd.DataFrame(stocks_arr)

    def get_and_write_to_csv(self, stock: str, time_interval: str) -> pd.DataFrame:
        stocks = self.get_stock_data(stock, time_interval)
        file_name = "stock_csvs/" + stock + "_" + time_interval + ".csv"
        stocks.to_csv(file_name, index=True, index_label='index')
        return stocks

    def get_stock_data_from_csv(self, csv_file: str) -> pd.DataFrame:
        '''
        pass in relative file path
        return dataframe from .csv file
        '''
        return pd.read_csv(csv_file, parse_dates=True, index_col=0)

    def plot(self, df: pd.DataFrame, *args) -> None:
        '''
        plot a dataframe using matplotlib. 
        ex) trader.plot_(df, ('high', 'g'), ('low', 'r'), ('50ma', 'b'))
        '''
        style.use('ggplot')

        for key in args:
            plt.plot(df["date"], df[key[0]], key[1], label=key[0])
        
        plt.title("Stonks")
        plt.xlabel('date')
        plt.ylabel('price')
        plt.legend()
        plt.show()

    def plot_volume(self, df: pd.DataFrame, *args) -> None:
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
    
    def add_moving_average(self, df: pd.DataFrame, size: str) -> pd.DataFrame:
        '''
        add a moving average to a dataframe 
        ex) trader.add_moving_average(df, 50)
        '''
        ma_name = str(size) + "ma" # ex) 50ma
        df[ma_name] = df['close'].rolling(window=size, min_periods=0).mean()
        df.dropna(inplace=True) # removes the entire row of all rows that have NaN
        return df

    def get_current_price(self, ticker: str) -> float: 
        '''
        return the current price of a stock
        '''
        url = self.stock_quote_url + "/" + ticker
        response = requests.request("GET", url, headers=self.headers, params=self.querystring)
        curr_stock_data = json.loads(response.text)
        if curr_stock_data[0]['ask']: return float(curr_stock_data[0]['ask'])
        print('error getting stock quote')
        sys.exit()

    def buy_stock(self, user_id: str, ticker: str, quantity: int) -> bool:
        time = dt.now()
        date_time_str = time.strftime('%m/%d/%Y %H:%M:%S')
        post_url = self.conf['aws_api'] + '/product'
        txn_id = str(uuid.uuid4())
        curr_price = self.get_current_price(ticker)

        payload = {
            "productId": txn_id,
            "user_id": user_id, 
            "ticker": ticker, 
            "quantity": int(quantity), 
            "date": date_time_str, 
            "transaction_type": "buy", 
            "price": str(curr_price)
        }

        response = requests.post(post_url, json = payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Error attempting to buy a stock: {e}")
        return True

    def sell_stock(self, user_id: str, ticker: str, quantity_to_sell: int) -> bool:
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

        return txns_df_sorted.loc[txns_df_sorted['user_id'] == user]

    def create_portfolio(self, transactions: pd.DataFrame) -> dict: 
        '''
        take in a df of all a user's transactions
        return a dictionary of their portfolio 
        NOTE: uses a LIFO stack to choose which holdings(s) to sell 
        '''

        holdings = {}

        # loop over all the different stocks a user owns 
        for ticker in transactions["ticker"].unique(): 
            holdings[ticker] = {}

            # find how many shares the user holds
            shares_bought = transactions.loc[(transactions['ticker'] == ticker) & (transactions['transaction_type'] == 'buy')]['quantity'].sum()
            shares_sold = transactions.loc[(transactions['ticker'] == ticker) & (transactions['transaction_type'] == 'sell')]['quantity'].sum()
            shares_held = shares_bought - shares_sold
            holdings[ticker]['shares'] = shares_held

            buy_stack = []
            capital_gains = 0
            txns_of_x_ticker = transactions.loc[(transactions['ticker'] == ticker)]

            # loop over each stock bought or sold of same stock ticker 
            for _, row in txns_of_x_ticker.iterrows():
                if row['transaction_type'] == 'buy': 
                    buy_stack.append({
                        'date': row['date'], 
                        'price': row['price'], 
                        'transaction_type': row['transaction_type'], 
                        'ticker': row['ticker'],
                        'quantity': row['quantity'],
                        'num_sold': 0
                    })

                if row['transaction_type'] == 'sell':
                    if not buy_stack:
                        print('something wrong in transaciton history')
                        return 

                    num_stocks_to_sell = row['quantity']
                    stocks_sold = 0
                    while (stocks_sold < num_stocks_to_sell) and buy_stack: 

                        quantity_cnt = 0
                        quantity_from_txn = buy_stack[-1]['quantity']

                        for _ in range(quantity_from_txn):
                            gain = row['price'] - buy_stack[-1]['price']
                            capital_gains += gain
                            stocks_sold += 1
                            quantity_cnt += 1
                            if quantity_cnt >= quantity_from_txn:
                                buy_stack.pop()
                            if stocks_sold >= num_stocks_to_sell: 
                                # add a marker for the stocks that are apart of most recent buy transaction that were sold 
                                # ie) [buy 5, buy 2] we're planning to sell 3, so now we pop and still need to sell 1 one more. 
                                # that means when we calculate total returns, we are accounting for one extra stock. 
                                break

            market_value = 0 
            total_quantity_owned = 0
            for stock in buy_stack: 
                market_value += stock['quantity'] * stock['price']
                total_quantity_owned += stock['quantity']

            holdings[ticker]['market_value'] = round(market_value, 2)
            holdings[ticker]['realized_gains'] = round(capital_gains, 2)
            holdings[ticker]['average_cost'] = round(market_value / total_quantity_owned, 2) 

            # not sure if this logic is 100% correct 
            # we can sell 1 or two stocks from a transaction, but not pop them off of the buy_stack if there is a big quantity 
            # if were on line 
            total_returns = capital_gains
            curr_price = self.get_current_price(ticker)
            for stock in buy_stack: 
                total_returns += (curr_price - stock['price']) * stock['quantity']
           
            holdings[ticker]['total_return'] = round(total_returns, 2)

        total_value = 0
        for stock in holdings.items(): 
            total_value += stock[1]['market_value']
        for stock in holdings: 
            holdings[stock]['portfolio_diversity'] = round((holdings[stock]['market_value'] / total_value) * 100, 2)
        return holdings 


trader = Trader()


# df = trader.get_stock_data('AAPL', '1d')
# df = trader.get_and_write_to_csv('SNOW', '1d')
# df = trader.get_from_csv('stock_csvs/SNOW_1d.csv')
# trader.plot(df, ('high', 'g'), ('low', 'r'))
# trader.add_moving_average(df, 50)
# trader.plot_volume(df)
# print(df.head())
# curr_price = trader.get_current_price('SNOW')
# print(curr_price)



# df = trader.get_stocks('1wk')
# trader.get_and_write_to_csv("1d")
# df = trader.get_from_csv("stock_csvs/BABA_1d.csv")

# trader.plot_(df, ('high', 'g'), ('low', 'r'), ('50ma', 'b'))
# trader.plot_volume(df)
# trader.plot(df, ('high', 'g'))
# print(df.head())
