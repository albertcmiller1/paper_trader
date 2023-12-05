import boto3

def create_dynamodb_table(primary_index, dynamodbTableName): 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodbTableName)
    
    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': primary_index,
                'AttributeType': 'S'
            },
        ],
        TableName=dynamodbTableName,
        KeySchema=[
            {
                'AttributeName': primary_index,
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 123,
            'WriteCapacityUnits': 123
        },
    )

create_dynamodb_table("match_id", "order_book_matches")
create_dynamodb_table("date_time", "price_history")