# trading-with-python


This repo will allow a user to create a paper portfolio by buying and selling stocks. 

## Features: 
* buy and sell paper stocks with api (hosted via aws api gateway, lambda, dynamodb)
* view portfolio 
* graph portfolio over time 
* graph any stock 
* graph any stock with moving averages 
* download csv files of any stock 
    
## Further Ideas 
* inlude buy/sell strike prices (aws fargate)
* graph live stocks / live portfolio (would need a stock api that suppors websockets + graphing utility)
* keep stock data in an s3 bucket and check there before making an api call

## To get started... clone the repo and run 

* `pipenv shell`
* `pipenv install`
* `python main.py --help`

## Api endpoints
* get all stocks a user owns 
* buy stock 
* sell stock 
* dynamodb schema: (user, stock_ticker, buy_date, buy_price, buy_quantity) 


## other 
currently using the yahoo finance [rapidapi](https://rapidapi.com/sparior/api/yahoo-finance15) to get stock data. you will need to get your own api key and update `configuration.yaml`
