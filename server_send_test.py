import requests
import json
from collections import OrderedDict

url = "http://localhost:8888/api"
room_id = 12345
header = {
    "Content-Type": "application/json"
}
qid_list = []

body = OrderedDict()

body['cmd'] = "list"
body['payload'] = {"roomid":room_id}

res = requests.post(url, headers=header, json=body)
if res.status_code == 200:
    print('connection succese')
    # print(res.json())
    jsonRes = json.loads(res.text)
    questionNum = len(jsonRes['payload']["questions"])
    if len(qid_list) < questionNum :
        for i in range(questionNum - len(qid_list)) :
            qid_list.append(jsonRes['payload']["questions"][len(qid_list)]['qid'])
  
        print(qid_list)
else :
    print('connection fail')
    # jsonRes = json.loads(res.json())
    # print(jsonRes['payload'])
    

print(res.status_code)

