# trading-with-python


This repo will allow a user to create a paper portfolio by buying and selling stocks. 

## Features: 
* buy and sell paper stocks with api (hosted via AWS SAM, api gateway, lambda, dynamodb)
* view portfolio 
* graph portfolio over time 
* graph any stock 
* graph any stock with moving averages 
* download csv files of any stock 
    
## Further Ideas 
* inlude buy/sell strike prices (aws fargate)
* graph live stocks / live portfolio (would need a stock api that suppors websockets + graphing utility)
* keep stock data in an s3 bucket and check there before making an api call
* backtest a trading strategy for a stock 
* use sns topic to send myself an email each time a new user signs up 

## examples 
* `python main.py --user albert --buy_stock AAPL --quantity 1`
* `python main.py --user albert --list_portfolio`

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
