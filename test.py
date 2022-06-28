import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 10, "name":"first video!", "views":1000},
		{"likes": 78, "name":"a funny video!", "views":2345},
		{"likes": 200, "name":"a sad video...", "views":45240}]

for i in range(len(data)):
	response = requests.put(BASE + "video/" + str(i), data[i])
	print(response.json())

"""
input("Press return for DELETE with video id 0")
 print(response)
"""

input("Press return for GET with video id 2")
response = requests.get(BASE + "video/6")
print(response.json())