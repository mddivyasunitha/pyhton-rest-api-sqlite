import requests
import json

BASE = "http://127.0.0.1:5000/"
data = [{"likes": 100, "name": "test1", "views": 100},
        {"likes": 1000, "name": "test2", "views": 1000},
        {"likes": 10000, "name": "test3", "views": 10000},
        {"likes": 100000, "name": "test4", "views": 10000},
        {"likes": 1000000, "name": "test5", "views": 10000}]
headers = {"accept": "application/json"}

for i in range(len(data)):
    response = requests.put(
        BASE+"video/"+str(i+1), json=data[i])
    print(response.json())

input()
response = requests.patch(
    BASE+"video/"+str(1), json={'views': 120})
print(response.json())

input()
response = requests.get(BASE+"video/1")
print(response.json())

input()
response = requests.get(BASE+"video/3")
print(response.json())

input()
response = requests.delete(BASE+"video/1")
print(response)

input()
response = requests.delete(BASE+"video/1")
print(response)
