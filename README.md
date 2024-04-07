# Paper Trader
This repo will allow a user to create a paper portfolio via buying and selling paper stocks. You may also graph any stock, your portfolio, or a trading algorithm. 

## Features: 
* stream data from the order book 
* buy and sell paper stocks
* view portfolio 
* graph portfolio over time 
* graph any stock 
* graph any stock with moving averages 
* download csv files of any stock 

### Note
* You must start the backend before the frontend will have full functionality

## Frontend 
* Create React App with CanvasJS charts
* `cd frontend`
* `npm install`
* `npm start`

## Backend

## Examples 
* `python main.py --user albert --curr_price AAPL`
* `python main.py --user albert --buy AAPL --quantity 1 --price 101`
* `python main.py --user albert --sell AAPL --quantity 1 --price 101`
* `python main.py --user albert --stream_matches AAPL`
* `python main.py --user albert --stream_spread AAPL`
* `python main.py --user albert --list_txns AAPL`
* `python main.py --user albert --price_history AAPL`
* `python main.py --user albert --stream_price AAPL`
* `python main.py --user albert --post_matches AAPL`
* `python main.py --user albert --post_prices AAPL`

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

## Todo
* clean up comments / logs
* fix math error in create_portfolio
* write api calls to csvs, then every time we need to make an api call check csv folder first. 
* finish graph_portfolio
* write admin script to generate transactions for testing 
* write out binary search logic in get_and_trim_stock_data

https://dev.to/radioactive11/real-time-interactive-plotting-using-sockets-python-plotly-297g

TODO current: 
* create different pages for react app 
* create a dynamo table for historical prices 
* create a table for all user transactions 
* create buy/sell endpoints for paper trader API 



* update lambda function to take incoming matches from the orderboook 
* update lambda function to take incoming price data from the orderbook 
* create a dynamo table of stock data 
* create GUI to plot live prices, live portfolio, and place trades 


## backend API 
### dependencies 
`pip3 install flask`

### start server 
`flask --app server run`

### conect 
`curl http://127.0.0.1:5000`


https://www.tutorialspoint.com/sqlite/sqlite_python.htm

## frontend sockets 
* https://blog.logrocket.com/websocket-tutorial-real-time-node-react/
* https://www.npmjs.com/package/react-use-websocket
* https://www.youtube.com/watch?v=azvcvbeRZ08&ab_channel=WebDevCody
* https://vishwas-r.medium.com/how-to-use-canvasjs-react-charts-in-react-funcitonal-component-49edf22b632f


## issues 
* the order book doesnt known if a match_id or any id is in the database or not. 
* aka, we need to truncate the databases 