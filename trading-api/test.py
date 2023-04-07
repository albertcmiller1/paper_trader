import json
import requests

shit = {'resource': '/hello', 'path': '/hello/', 'httpMethod': 'GET', 'headers': {'Accept': '*/*', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '12271', 'CloudFront-Viewer-Country': 'US', 'Host': 'rbks09r44k.execute-api.us-east-1.amazonaws.com', 'User-Agent': 'curl/7.79.1', 'Via': '2.0 cd958e502c6aea704f0f824e60431e72.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'PwDwr6B3VdDOLXPZoWVdC6qjo-ap0wLqh1AQyg4FFE-XW4xHBtT8iA==', 'X-Amzn-Trace-Id': 'Root=1-642c9cdf-002259364e64fa8215769a4f', 'X-Forwarded-For': '47.230.198.14, 15.158.35.207', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['12271'], 'CloudFront-Viewer-Country': ['US'], 'Host': ['rbks09r44k.execute-api.us-east-1.amazonaws.com'], 'User-Agent': ['curl/7.79.1'], 'Via': ['2.0 cd958e502c6aea704f0f824e60431e72.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['PwDwr6B3VdDOLXPZoWVdC6qjo-ap0wLqh1AQyg4FFE-XW4xHBtT8iA=='], 'X-Amzn-Trace-Id': ['Root=1-642c9cdf-002259364e64fa8215769a4f'], 'X-Forwarded-For': ['47.230.198.14, 15.158.35.207'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'x6qouf', 'resourcePath': '/hello', 'httpMethod': 'GET', 'extendedRequestId': 'C31y_EIgIAMFnWw=', 'requestTime': '04/Apr/2023:21:55:43 +0000', 'path': '/Prod/hello/', 'accountId': '719501685385', 'protocol': 'HTTP/1.1', 'stage': 'Prod', 'domainPrefix': 'rbks09r44k', 'requestTimeEpoch': 1680645343655, 'requestId': 'ae4e20be-00a7-4df6-b5df-04f95e48bbdb', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '47.230.198.14', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'curl/7.79.1', 'user': None}, 'domainName': 'rbks09r44k.execute-api.us-east-1.amazonaws.com', 'apiId': 'rbks09r44k'}, 'body': {"productId": "001", "name": "lucky_charms"}, 'isBase64Encoded': False}

# print(json.dumps(shit))

url = "https://bjnhhj5gd2.execute-api.us-east-1.amazonaws.com/Prod"
say_hi = url + '/hello'
get_url = url + '/products'
post_url = url + '/product'

myobj = {'productId': "003", 'name': "IMJSON"}
print(type(shit))
# print(isinstance(shit, dict))

# x = requests.get(say_hi)
x = requests.get(get_url)
# x = requests.post(post_url, json = myobj)
# x = requests.post(post_url, json = json.dumps(myobj))

print(x.text)