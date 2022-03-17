import json

dict1 = { 'name' : 'song', 'age' : 10 }

print(dict1)
print(type(dict1))

json_val = json.dumps(dict1)

print(json_val)
print(type(json_val))

