

import requests
import json
from collections import OrderedDict

url = "http://localhost:8888/api"
room_id = 12345
header = {
    "Content-Type": "application/json"
}

body = OrderedDict()

body['cmd'] = "list"
body['payload'] = {"roomid":room_id}

res = requests.post(url, headers=header, json=body)
if res.status_code == 200:
    print('connection succese')
    # print(res.json())
    jsonRes = json.loads(res.text)
    print(jsonRes['payload'])
else :
    print('connection fail')
    # jsonRes = json.loads(res.json())
    # print(jsonRes['payload'])
    

print(res.status_code)

