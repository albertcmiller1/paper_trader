# trading-with-python
This repo will allow a user to create a paper portfolio via buying and selling paper stocks. You may also graph any stock, your portfolio, or a trading algorithm. 

## Features: 
* buy and sell paper stocks with api (hosted via AWS SAM, api gateway, lambda, dynamodb)
* view portfolio 
* graph portfolio over time 
* graph any stock 
* graph any stock with moving averages 
* download csv files of any stock 
    
## Examples 
* `python main.py --user albert --list_portfolio`
* `python main.py --user albert --buy_stock AAPL --quantity 1`
* `python main.py --user albert --sell_stock AAPL --quantity 1`
* `python main.py --user albert --graph_stock AAPL`
* `python main.py --user albert --list_txns`

## Further Ideas 
* inlude buy/sell strike prices (aws fargate + stock api that suppors websockets)
* graph live stocks / live portfolio (websockets graphing utility)
* keep stock data in an s3 bucket (or local) and check there before making an api call
* backtest a trading strategy for a stock 
* use sns topic to send myself an email each time a new user signs up 
* change parition of dynamodb to user_id with clustering on timestamp for better performance 
* write admin tool to generate random transactions for testing purposes 

## Api endpoints
* get all stocks a user owns 
* buy stock 
* sell stock 
* dynamodb schema: (user, stock_ticker, buy_date, price, transaction_type, quantity) 

## To get started clone the repo and run 

* `pipenv shell`
* `pipenv install`
* `python main.py --help`

## Notes before you start 
currently using the yahoo finance [rapidapi](https://rapidapi.com/sparior/api/yahoo-finance15) to get stock data. you will need to get your own api key and update `configuration.yaml`

## Todo
* clean up comments / logs
* fix math error in create_portfolio
* write api calls to csvs, then every time we need to make an api call check csv folder first. 
* finish graph_portfolio
* write admin script to generate transactions for testing 
* write out binary search logic in get_and_trim_stock_data