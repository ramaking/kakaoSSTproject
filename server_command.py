import requests
import json
from collections import OrderedDict
url = "http://localhost:8888/api"
header = {
        "Content-Type": "application/json"
    }

def post(url, header, body):
    try:
        res = requests.post(url, headers=header, json=body)
    except:
        print('server connect fail')
    return res

def displayWordCloud(roomId):
    body = OrderedDict()

    body['cmd'] = "displayWordCloud"

    body['payload'] = {"roomid":roomId}
    post(url, header, body)



def sendPlay(roomId, pid):

    body = OrderedDict()

    body['cmd'] = "play"

    body['payload'] = {"roomid":roomId,"qid":pid}

    post(url, header, body)


def isPlaying(roomId):

    body = OrderedDict()

    body['cmd'] = "getIsPlay"

    body['payload'] = {"roomid":roomId}

    try :
        res = post(url, header, body)
        jsonRes = json.loads(res.text)
        return jsonRes['payload']['isPlaying']
    except :
        return True

def playVideo1(roomId, responseNum) :

    body = OrderedDict()

    body['cmd'] = "play"

    # responseNum은 정해진 응답
    # 0000-0000의 경우 안녕하세요
    # 1111-1111의 경우 질문이 있습니다
    # 2222-2222의 경우 이해했습니다 감사합니다

    body['payload'] = {"roomid":roomId,"responseNum":responseNum}
    post(url, header, body)

# playselectiveVideo(12345,'0000-0000')

def playVideo(roomId) :

    qidList = []
    voteList = []

    body = OrderedDict()

    body['cmd'] = "list"
    body['payload'] = {"roomid":roomId}

    try : 
        res = post(url, header, body)
    except :
        print('error')
    if res.status_code == 200:
        print('connection succese')
        # print(res.json())
        jsonRes = json.loads(res.text)
        print(jsonRes)

        if(jsonRes['status']['status'] != 'bad'):
            
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

# isPlaying(12345)