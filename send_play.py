import requests
import json
from collections import OrderedDict

def sendPlay(roomId, pid) :
    url = "http://localhost:8888/api"
    header = {
        "Content-Type": "application/json"
    }
    question_num = 0

    body = OrderedDict()

    body['cmd'] = "play"

    body['payload'] = {"roomid":roomId,"qid":pid}

    res = requests.post(url, headers=header, json=body)
    print(res.status_code)
