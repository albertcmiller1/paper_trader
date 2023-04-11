import json
import requests
import boto3
import uuid

dynamodbTableName = 'paper-trader-transactions'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

with open('./admin/test_data.json') as f:
   data = json.load(f)

# print(data['data'])

payload = data['data']
post_url = "https://bjnhhj5gd2.execute-api.us-east-1.amazonaws.com/Prod" + "/product"

for item in payload: 
    item["productId"] = str(uuid.uuid4())
    # print(item)
    response = requests.post(post_url, json = item) # this works when data is all strings
    # response = requests.post(post_url, json = json.loads(item)) # this does not work
    print("\n")
    print(response.text)


    # table.put_item(Item=item)

