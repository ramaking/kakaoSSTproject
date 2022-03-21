import requests
import json
from collections import OrderedDict

url = "http://localhost:8888/api"
room_id = 12345
header = {
    "Content-Type": "application/json"
}
question_num = 0

# 수정예정
pid_list = '353ea0ed-616f-474c-8446-671feebbe723'

body = OrderedDict()

body['cmd'] = "play"

body['payload'] = {"roomid":room_id,"pid":pid_list}

res = requests.post(url, headers=header, json=body)
print(res.status_code)
