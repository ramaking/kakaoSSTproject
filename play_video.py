import requests
import json
from collections import OrderedDict
# from send_play import sendPlay

def sendPlay(roomId, pid) :
    url = "http://localhost:8888/api"
    header = {
        "Content-Type": "application/json"
    }

    body = OrderedDict()

    body['cmd'] = "play"

    body['payload'] = {"roomid":roomId,"qid":pid}

    res = requests.post(url, headers=header, json=body)
    print(res.status_code)

def playVideo(roomId) :

    url = "http://localhost:8888/api"
    
    header = {
        "Content-Type": "application/json"
    }
    qidList = []
    voteList = []

    body = OrderedDict()

    body['cmd'] = "list"
    body['payload'] = {"roomid":roomId}

    res = requests.post(url, headers=header, json=body)
    if res.status_code == 200:
        print('connection succese')
        # print(res.json())
        jsonRes = json.loads(res.text)
        print(jsonRes)
        questionNum = len(jsonRes['payload']["questions"])
        if len(qidList) < questionNum :
            for i in range(questionNum - len(qidList)) :
                jsonQuestion = jsonRes['payload']["questions"][len(qidList)]
                voteList.append(int(jsonQuestion['votes']))
                qidList.append(jsonQuestion['qid'])
    
        voteList.sort(reverse=True)
        
        for i in voteList :
            for j in range(questionNum) :
                selectedQuestion = jsonRes['payload']["questions"][j]

                if int(selectedQuestion['votes']) == i : 
                    if selectedQuestion['isPlayed'] == False : 
                        pid = selectedQuestion['qid']
                        sendPlay(roomId, pid)
                        return 0

    else :
        print('connection fail')
