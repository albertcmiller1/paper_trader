import requests
import json


url = "http://0.0.0.0:5001/curr_price"
response = requests.request("GET", url)
print(response.text)
j = json.loads(response.text)
print(j)


# url = "http://0.0.0.0:5001/place_order"

# two ways to know if a user's transaction went though 
#   1. send a URL to the book where the book can post to 
#   2. just have the book post directly to dynamoDB

# myobj = {
#     'price': 100.34,
#     'shares': 10,
#     'order_type': "buy"
# }

# response = requests.post(url, json = myobj)
# # response = requests.post(url, json = json.dumps(myobj))
# print(response.text)

