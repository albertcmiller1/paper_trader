import pandas as pd

value_df = pd.DataFrame()

tickers = ["TSLA", "AAPL"]

value_df = value_df._append({tickers[1] : 100}, ignore_index=True)
value_df = value_df._append({tickers[1] : 101}, ignore_index=True)
value_df = value_df._append({tickers[1] : 103}, ignore_index=True)

value_df = value_df._append({tickers[0] : 400}, ignore_index=True)
value_df = value_df._append({tickers[0] : 401}, ignore_index=True)
value_df = value_df._append({tickers[0] : 403}, ignore_index=True)

print(value_df.head())