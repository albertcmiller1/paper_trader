import uuid
import boto3
import random
import pprint
import requests
from old_stuff.trader import Trader

num_txns = 10
user_id = "trent"
ticker = "TSLA"
time_intveral = "1d"
load_to_dynamodb = False

trader = Trader()

def generate_test_data():
    if trader.stock_is_in_csv_files(ticker, time_intveral):
        file_name = ticker + "_" + time_intveral + ".csv"
        df = trader.get_stock_data_from_csv("stock_csvs/" + file_name.lower())
    else: 
        df = trader.get_and_write_to_csv(ticker, time_intveral)

    rand_indexs = [random.randint(0, len(df.index)) for x in range(num_txns)]
    rand_indexs.sort()

    txns = []
    quantity_owned = 0
    for i in rand_indexs:
        row = df.iloc[i]
        date = row['date']
        price = row['close']

        if quantity_owned <= 5: 
            txn_type = 'buy'
            quantity = random.randint(1, 4)
            quantity_owned += quantity
        else: 
            txn_type = 'sell'
            quantity = random.randint(1, quantity_owned)
            quantity_owned -= quantity

        txns.append({
            "productId": str(uuid.uuid4()),
            "user_id": user_id,
            "ticker": ticker.upper(),
            "quantity": quantity,
            "date": date,
            "transaction_type": txn_type,
            "price": price
        })

    return txns

def load_test_data(transactions):
    post_url = "https://bjnhhj5gd2.execute-api.us-east-1.amazonaws.com/Prod" + "/product"
    dynamodbTableName = 'paper-trader-transactions'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodbTableName)

    for txn in transactions: 
        response = requests.post(post_url, json = txn) # this works when data is all strings
        # pprint.pprint(txn)
        print("\n")
        print(response.text)
        # table.put_item(Item=item)


txns = generate_test_data()
load_test_data(txns)
