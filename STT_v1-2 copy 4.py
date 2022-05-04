from asyncio.windows_events import NULL
from concurrent.futures.process import _get_chunks
from dataclasses import replace
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
sendQuestionNum = [0,6]
lastQuestionNum = 3

kakao_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
kakao_header = {
    #"Transfer-Encoding": "chunked",
    "Content-Type": "application/octet-stream",
    "Authorization": "KakaoAK " + "5bdcd793f13bebf5e4e874d636b694c0"
}
# device_index = 0
# for device_index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f'{device_index}, {name}')
    # if name == '스테레오 믹스(Realtek(R) Audio)':
    # if name == 'CABLE Output(VB-Audio Virtual Cable)':
    #     print(device_index)
    #     break

dataSet1 = ['1111-1111', '','2222-2222' ,]

dataSet2 = [
    ['이해안가는부분있나요','어려운부분이있나요','어려운부분있나요','내용을해석하기버겁나요','수업내용을잘파악했나요','방금부분에서질문할내용이있나요',
    '내용에대하여추가설명이필요한가요','질문'],
    [],
    [],
    [],
    [],
    ['말씀',],
    ['이해','됬나요','됐나요'],
    # ['이상', '더 이상 질문 없나요?']
]

thread_list1 = [NULL for i in range(10)]
thread_list2 = {}

# canRecording = True

recording_index = 0

canRecording = [True,False,False,False,False,False,False,False,False,False,False,False,False]

timeOut = True

def stt(audio):
    res = requests.post(kakao_url, headers=kakao_header,
                                data=audio.get_raw_data())
    # print(res.text)
    line = res.text.splitlines()
    lineRes = line[-2]
    jsonRes = json.loads(lineRes)
    strRes = jsonRes["value"]
    strRes.replace(" ","")
    print('결과 : ' + jsonRes["value"])

    return strRes.replace(" ","")

def stopper(num,t1,t2) :
    # global canRecording
    global  timeOut
    # canRecording = True
    timeOut = False
    print(str(num)+' time out')
    t1.raise_exception()
    t2.raise_exception()

    

def threadStop(threadNum) :
    print(str(threadNum)+' 빼고 thread stop')
    global thread_list1
    global recording_index
    global canRecording
    canRecording[recording_index] = False
    for i in range(len(thread_list1)):
        if i != threadNum or i != NULL:
            thread_list1[i].raise_exception()
            thread_list1[i] = NULL
        i+=1

class recorder(thread_with_exception):

    def __init__(self, name):
        super().__init__(name)

    def run(self):
        # try:
            global canRecording
            global recording_index
            print(str(self.name)+ " recording start")
            r = sr.Recognizer()
            with sr.Microphone(sample_rate=16000) as source:
                audio = r.listen(source)
            canRecording[recording_index] = True
            print(str(self.name)+ " recording end")
            res = requests.post(kakao_url, headers=kakao_header,
                                data=audio.get_raw_data())
            # print(res.text)
            line = res.text.splitlines()
            lineRes = line[-2]
            jsonRes = json.loads(lineRes)
            strRes = jsonRes["value"]
            strRes.replace(" ","")
            print('결과 : ' + jsonRes["value"])

            if strRes in dataSet2[int(self.name)]:
                threadStop({int(self.name),})
                print(str(self.name)+' 번 dataset에 캐치')

                # 다른 녹음 스레드를 전부 정지
                
                recording_index += 1
                canRecording[recording_index] = True
                nextDataSetNum = int(self.name) + 1
                if self.name in sendQuestionNum:
                    # send question play
                    print('send question')
                    # play_video.playVideo(room_id)
                # else :
                    # send pixed response play
                    # play_video.playVideo1(room_id, dataSet1[int(self.name)])

                # 60초 이내에 이후에 문답을 이어갈 맨트를 받음
                    
                while True : 
                    if canRecording[recording_index]:
                        # if nextDataSetNum == lastQuestionNum:
                            
                        #     sys.exit(0)
                        t1 = recorder(nextDataSetNum)
                        t1.start()
                        print(str(nextDataSetNum)+' thread start')
                        t2 = recorder(nextDataSetNum)

                        t2 = timeStopper(5,stopper,args=(self.name,t1,t2))
                        t2.raise_exception()
                        t2.start()
                        canRecording[recording_index] = False
                        # t.join()
                    # else :
                        # print(str(nextDataSetNum)+'time out')
                        # canRecording = True
                        # sys.exit(0)
                    time.sleep(0.5)
                        
                    
            else:
                # if(self.name == 0):
                #     canRecording = True
                print(str(self.name)+' 번 dataset 캐치x')
                # if(timeOut == False):
                #     # print(str(self.name)+'time out')
                #     sys.exit(0)
        # finally:
        #     print(str(self.name)+' thread end')

# main
while True:
    if canRecording[recording_index] == True:
        
        recordLine1 = 0
        recordLine2 = 5
        print(thread_list1[recordLine1])
        print(thread_list1[recordLine2])
        t1 = recorder(recordLine1)
        t1.start()
        thread_list1[recordLine1] = t1
        # print(thread_list1[recordLine1])
        # thread_list1[recordLine1].raise_exception()
        time.sleep(0.5)
        t2 = recorder(recordLine2)
        t2.start()
        thread_list1[recordLine2] = t2
        # t3 = timeStopper(3,stopper,args=(recordLine1,t1,t2))
        # t3.raise_exception()
        # t3.start()
        canRecording[recording_index] = False
    time.sleep(0.5)
