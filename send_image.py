import requests
import json
from collections import OrderedDict

def sendPlay(roomId, imageKey) :
    url = "http://localhost:8888/api"
    header = {
        "Content-Type": "application/json"
    }

    body = OrderedDict()

    body['cmd'] = "getWordCloud"

    body['payload'] = {"roomid":roomId,"key":imageKey, "value":"image"}

    res = requests.post(url, headers=header, json=body)
    print(res.status_code)

sendPlay(12345, "wordcloud")