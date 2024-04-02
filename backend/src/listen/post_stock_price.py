'''
this service will post the current price of the book's stock every 60 seconds
'''

import requests, json, websocket, ast, boto3, uuid

def parse_message(wsapp, message):
    print(f"og message: {message}")
    result = ast.literal_eval(message)
    put_message_in_table(result)


def put_message_in_table(message): 
    dynamodbTableName = 'price_history'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodbTableName)

    table.put_item(
        TableName=dynamodbTableName,
        Item=message
    )


HOST="ws://0.0.0.0:5001"

wsapp = websocket.WebSocketApp(f"{HOST}/price", on_message=parse_message)
wsapp.run_forever() 

