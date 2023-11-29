import uuid
import time 
from datetime import datetime as dt


# print(dt.fromtimestamp(1364477400).strftime('%Y-%m-%d %H:%M:%S')) 
# t1 = dt.fromtimestamp(1364477400).strftime('%Y-%m-%d %H:%M:%S')
t1 = dt.fromtimestamp(1364477400)

date_time_str = "06/24/2022 12:00:00"
t2 = dt.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')

# print(datetime_object)

print(t1)
print(t2)

print(type(t1))
print(type(t2))


if t1 < t2: 
    print('yay')


# id = str(uuid.uuid4())
# print(id)
# print(type(id))
