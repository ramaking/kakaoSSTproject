
import requests
import json

url = "http://localhost:8888/api"
rood_id = 12345
header = {
    "Content-Type": "application/json"
}

body = {
    'cmd': 'play',
    'payload': {
        'roomid': '1234',
        # 'qid': 'f9c3d2a6-4e0d-4359-99e4-b1d1c4e1c586'
    }
}


res = requests.post(url, headers=header, json={'cmd': 'play', 'payload': {
                    'roomid': '12345'
                    # ,  'qid': 'daba40c0-5f11-4df6-a253-e4b79368b3b7'
                     }})
print(res.status_code)
