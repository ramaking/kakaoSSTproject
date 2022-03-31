import requests
from collections import OrderedDict


def updateStudentNum(studentNum, attendenceRate):
    room_id = 12345
    server_url = "http://localhost:8888/api"
    server_header = {
        "Content-Type": "application/json"
    }

    body = OrderedDict()
    body['cmd'] = "updateStudentCnt"
    body['payload'] = {"roomid": room_id, 'studentNum': studentNum, 'attendenceRate': attendenceRate}

    res = requests.post(server_url, headers=server_header, json=body)
    
    if res.status_code == 200:
        print('connection succese')
    else:
        print('connection fail')
