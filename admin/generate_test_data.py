import uuid

num_txns = 10
user_id = "trent"
ticker = "TSLA"

# load in a csv file
# find random dates from first date to last date 
# 


txns = []
for i in range(num_txns):
    txns.append({
        "productId": str(uuid.uuid4()),
        "user_id": user_id,
        "ticker": "TSLA",
        "quantity": 1,
        "date": "05/24/2022 12:00:00",
        "transaction_type": "buy",
        "price": "209.39"
    })





