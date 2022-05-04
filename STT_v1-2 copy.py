from concurrent.futures.process import _get_chunks
import sys
import threading
from tracemalloc import start
import requests
import json
import speech_recognition as sr
import time
import server_command
from threading import Timer
from timerStopper import timeStopper
import threading 
import ctypes 
from threadException import thread_with_exception

room_id = 12345

kakao_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
kakao_header = {
    #"Transfer-Encoding": "chunked",
    "Content-Type": "application/octet-stream",
    "Authorization": "KakaoAK " + "5bdcd793f13bebf5e4e874d636b694c0"
}
canRecording = True
device_index = 0
timeOut = True

# for device_index, name in enumerate(sr.Microphone.list_microphone_names()):
#     #print(f'{device_index}, {name}')
#     if name == '스테레오 믹스(Realtek(R) Audio)':
#         break

dataSet1 = ['1111-1111', '2222-2222', '3333-3333']
dataSet2 = [
    ['질문', '궁금한게 있는 사람'],
    ['바보', '질문이 뭔가요?'],
    ['멍청이', '더 이상 질문 없나요?']
]

class Recoder(thread_with_exception):
    def stopper(self, str):
        # global canRecording
        global  timeOut
        # canRecording = True
        timeOut = False
        print(str)
        self.raise_exception()
        # super( sys.exit(0))

    def record(dataSetNum):
        global timeOut
        global canRecording
        print(str(dataSetNum)+ " recording start")
        r = sr.Recognizer()
        #마이크 말고 스테레오 믹스
        # with sr.Microphone(device_index=device_index,sample_rate=16000) as source:
        with sr.Microphone(sample_rate=16000) as source:
            audio = r.listen(source)
        print(str(dataSetNum)+ " recording end")
        # if(dataSetNum == 0):
        #     canRecording = True
        res = requests.post(kakao_url, headers=kakao_header,
                            data=audio.get_raw_data())
        line = res.text.splitlines()
        strRes = line[-2]
        jsonRes = json.loads(strRes)
        w = jsonRes["value"]
        print('결과 : ' + jsonRes["value"])
        for i in dataSet2[dataSetNum]:
            # print(i)

            # 분기점


            if i in w:
                # print(i)
                
                # canRecording = False
                # play_video.playVideo(room_id)
                    # play_video.playselectiveVideo(room_id, requestNum)

                    # 10초 이내에 이후에 문답을 이어갈 맨트를 받음
                    # threading.Timer(10,Reset).start()
                timeOut = True
                t2 = timeStopper(20,stopper,args=(dataSetNum,))
                t2.raise_exception()
                t2.start()

                print(str(dataSetNum)+'등록된 질문이 있습니다.')
                nextDataSetNum = dataSetNum + 1
                while True : 
                    if timeOut:
                        # record(dataSetNum)
                        t = threading.Thread(target=record, args=(nextDataSetNum,))
                        # str1 = str(dataSetNum)+' timer'
                        # t1 = Timer(7,stopper,args=(str1,))
                        
                        # t1.start()
                        t.start()
                        print(str(nextDataSetNum)+' thread start')
                        t.join()
                    else :
                        print(str(nextDataSetNum)+'time out')
                        sys.exit(0)
                    
                
            else:
                print(str(dataSetNum)+'질문단어 캐치x')
                if(timeOut == False):
                    print(str(dataSetNum)+'time out')
                    sys.exit(0)
                # if(dataSetNum == 0):
                #     canRecording = True
            # sys.exit(0)
recordThread = [False, False, False, False, ]


def stopper(str) :
    global canRecording
    global  timeOut
    # canRecording = True
    timeOut = False
    # print(str)
    super( sys.exit(0))


def record(dataSetNum):
    global timeOut
    global canRecording
    print(str(dataSetNum)+ " recording start")
    r = sr.Recognizer()
    #마이크 말고 스테레오 믹스
    # with sr.Microphone(device_index=device_index,sample_rate=16000) as source:
    with sr.Microphone(sample_rate=16000) as source:
        audio = r.listen(source)
    print(str(dataSetNum)+ " recording end")
    # if(dataSetNum == 0):
    #     canRecording = True
    res = requests.post(kakao_url, headers=kakao_header,
                        data=audio.get_raw_data())
    line = res.text.splitlines()
    strRes = line[-2]
    jsonRes = json.loads(strRes)
    w = jsonRes["value"]
    print('결과 : ' + jsonRes["value"])
    for i in dataSet2[dataSetNum]:
        # print(i)

        # 분기점


        if i in w:
            # print(i)
            
            # canRecording = False
            # play_video.playVideo(room_id)
                # play_video.playselectiveVideo(room_id, requestNum)

                # 10초 이내에 이후에 문답을 이어갈 맨트를 받음
                # threading.Timer(10,Reset).start()
            timeOut = True
            t2 = timeStopper(5,stopper,args=(dataSetNum,))
            t2.raise_exception()
            t2.start()

            print(str(dataSetNum)+'등록된 질문이 있습니다.')
            nextDataSetNum = dataSetNum + 1
            while True : 
                if timeOut:
                    # print(timeOut)
                    # record(dataSetNum)
                    t = threading.Thread(target=record, args=(nextDataSetNum,))
                    # str1 = str(dataSetNum)+' timer'
                    # t1 = Timer(7,stopper,args=(str1,))
                    
                    # t1.start()
                    t.start()
                    print(str(nextDataSetNum)+' thread start')
                    t.join()
                else :
                    # print(str(nextDataSetNum)+'time out11')
                    canRecording = True
                    sys.exit(0)
            
        else:
            print(str(dataSetNum)+'질문단어 캐치x')
            if(dataSetNum == 0):
                canRecording = True
            if(timeOut == False):
                # print(timeOut)
                # print(str(dataSetNum)+'time out22')
                sys.exit(0)
            
        # sys.exit(0)

# recordLine = 0
while True:
    if canRecording == True:
        recordLine = 0
        t = threading.Thread(target=record, args=(recordLine,))
        t.start()
        # str1 = ' timer'
        # t1 = Timer(3,stoper, args=(str1,))
        # t1.start()
        canRecording = False
        
    time.sleep(0.5)
