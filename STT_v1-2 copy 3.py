from concurrent.futures.process import _get_chunks
import sys
import threading
from tracemalloc import start
import requests
import json
import speech_recognition as sr
import time
import server_command
from threading import Thread, Timer
from timerStopper import timeStopper
import threading 
import ctypes 
from threadException import thread_with_exception

room_id = 12345
sendQuestionNum = 1
lastQuestionNum = 3

kakao_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
kakao_header = {
    #"Transfer-Encoding": "chunked",
    "Content-Type": "application/octet-stream",
    "Authorization": "KakaoAK " + "5bdcd793f13bebf5e4e874d636b694c0"
}
device_index = 0
for device_index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{device_index}, {name}')
    # if name == '스테레오 믹스(Realtek(R) Audio)':
    # if name == 'CABLE Output(VB-Audio Virtual Cable)':
    #     print(device_index)
    #     break

dataSet1 = ['1111-1111', '','2222-2222' ,]
dataSet2 = [
    ['질문'],
    ['말씀','질문'],
    ['이해','됬나요','됐나요'],
    # ['이상', '더 이상 질문 없나요?']
]

canRecording = True

timeOut = True

def stopper(a) :
    # global canRecording
    global  timeOut
    # canRecording = True
    timeOut = False
    print(str(a)+' time out')
    super(sys.exit(0))

# def threadStop(t) :
#     t.raise_


def record(dataSetNum):
     # room이 playing 상태인지 확인
    if(server_command.isPlaying(room_id) == False):
        if dataSetNum == lastQuestionNum:
            sys.exit(0)
        global timeOut
        global canRecording
        global device_index
        print(str(dataSetNum)+ " recording start")
        r = sr.Recognizer()
        #마이크 말고 스테레오 믹스
        # with sr.Microphone(device_index=2,sample_rate=16000) as source:
        with sr.Microphone(sample_rate=16000) as source:
            audio = r.listen(source)
        print(str(dataSetNum)+ " recording end")
        # if(dataSetNum == 0):
        #     canRecording = True
        res = requests.post(kakao_url, headers=kakao_header,
                            data=audio.get_raw_data())
        # print(res.text)
        line = res.text.splitlines()
        strRes = line[-2]
        jsonRes = json.loads(strRes)
        w = jsonRes["value"]
        print('결과 : ' + jsonRes["value"])
        for i in dataSet2[dataSetNum]:
            if i in w:



                if dataSetNum == sendQuestionNum:
                    # send question play
                    server_command.playVideo(room_id)
                else :
                    # send pixed response play
                    server_command.playVideo1(room_id, dataSet1[dataSetNum])

                    # 60초 이내에 이후에 문답을 이어갈 맨트를 받음
                timeOut = True
                t2 = timeStopper(60,stopper,args=(dataSetNum,))
                t2.raise_exception()
                t2.start()

                print(str(dataSetNum)+' 번 dataset에 캐치')
                nextDataSetNum = dataSetNum + 1
                while True : 
                    if timeOut:
                        if nextDataSetNum == lastQuestionNum:
                            sys.exit(0)
                        t = threading.Thread(target=record, args=(nextDataSetNum,))
                        t.start()
                        print(str(nextDataSetNum)+' thread start')
                        t.join()
                    else :
                        # print(str(nextDataSetNum)+'time out')
                        canRecording = True
                        sys.exit(0)
                    time.sleep(1)
                    
                
            else:
                if(dataSetNum == 0):
                    canRecording = True
                print(str(dataSetNum)+' 번 dataset 캐치x')
                if(timeOut == False):
                    # print(str(dataSetNum)+'time out')
                    sys.exit(0)

# main
# while True:
#     if canRecording == True:
#         recordLine = 0
#         t = threading.Thread(target=record, args=(recordLine,))
#         t.start()
#         canRecording = False
#     time.sleep(0.5)
