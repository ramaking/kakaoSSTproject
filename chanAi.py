from distutils.command.upload import upload
import requests
import json
from collections import OrderedDict


def updateStudentNum(room_id, studentNum, attendenceRate):
    # room_id = 12345
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

def getQuestionList(roomId):
    # roomId = 12345

    server_url = "http://localhost:8888/api"
    server_header = {
        "Content-Type": "application/json"
    }
    body = OrderedDict()
    body['cmd'] = "List"
    body['payload'] = {"roomid": roomId}

    res = requests.post(server_url, headers=server_header, json=body)
    
    if res.status_code == 200:
        print('connection succese')
        jsonRes = json.loads(res.text)
        # print(jsonRes)
        questions = []
        for i in range(len(jsonRes['payload']['questions'])):
            questions.append(jsonRes['payload']['questions'][i]['text'])
        print(questions)

    else:
        print('connection fail')

img = open('img/rose.PNG', 'rb')

img2 = open('word cloud/wordcloud.png', 'rb')
def sendWordCloud(roomId, img):
     # roomId = 12345

    server_url = "http://localhost:8888/send-word-cloud"
    # server_header = {
    #     "Content-Type": "application/json"
    # }
    upload = {'file': img}
    # res = requests.post(server_url)
    # body = OrderedDict()
    # body['cmd'] = "getWordCloud"
    # body['payload'] = {"roomid": roomId, "img" : img}

    res = requests.post(server_url, files=upload)
    
    if res.status_code == 200:
        print('connection succese')
        
        # send img file
        

    else:
        print('connection fail')
sendWordCloud(12345, img2)