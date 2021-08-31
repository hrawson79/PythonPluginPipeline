import json

f = open('config2.json',)

data = json.load(f)

for i in data:
    print(i)