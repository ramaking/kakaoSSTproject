from asyncio.windows_events import NULL
import requests
import json
import speech_recognition as sr
import time
import server_command
from timerStopper import timeStopper
from threadException import thread_with_exception

room_id = 12345
sendQuestionNum = [1,3]
lastQuestionNum = 3
timeoutNum = 60

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
    [
        ['이해안가는부분있나요','어려운부분이있나요','어려운부분있나요','내용을해석하기버겁나요','수업내용을잘파악했나요','방금부분에서질문할내용이있나요',
        '내용에대하여추가설명이필요한가요','어려운부분이있나요',
        '수업내용을잘파악했나요','내용을해석하기버겁나요',
        '방금부분에서질문할내용이있나요',
        '내용에대하여추가설명이필요한가요','바람'],

        # 고정답변전송
        ['어려운부분이있는학생이있나요','질문있는학생',
        '궁금한점있는학생','설명이어려운학생있나요',
        '구체적인설명이필요한학생','하늘'],
    ],
    [
        ['네말해보세요','질문하세요','말씀하세요','어떤것인가요','무엇인가요','무엇이죠','발언하세요','어떤거죠','얘기해보세요','얘기하세요','얘기해요','연필'],
        ['cannot use'],
    ],
    [
        ['또다른질문있나요','또궁금한거있나요','추가질문있나요','다른궁금한점있는학생있나요','다른학생들중질문있나요','다음질문있나요','또이해가지않는부분있나요','추가질문','물병'],

        # 고정답변전송
        ['이해가됬나요','이해됐죠','설명이됬나요','전화'],
    ]
]

thread_list1 = [NULL for i in range(10)]
thread_list2 = {}


recording_index = 0

canRecording = [True,False,False,False,False,False,False,False,False,False,False,False,False]

timeOut = True

def stt(audio):
    res = requests.post(kakao_url, headers=kakao_header,
                                data=audio.get_raw_data())
    # print(res.text)
    line = res.text.splitlines()
    lineRes = line[-2]
    try:
        jsonRes = json.loads(lineRes)
        strRes = jsonRes["value"]
        strRes.replace(" ","")
        print('결과 : ' + jsonRes["value"])
        return strRes.replace(" ","")
    except:
        print('error')

def stopper() :
    global canRecording
    global recording_index
    global timeOut
    print('time out')
    targetThread = thread_list1[recording_index]
    if targetThread != NULL :
        targetThread.raise_exception()
    timeOut = False
    canRecording[recording_index] = False
    recording_index = 0
    canRecording[recording_index] = True

def choseLine(strRes):
    global recording_index

    for i in dataSet2[recording_index][0]:
        
        if i in strRes:
            # 이전 녹음 스레드를  정지
            threadStop()
            
            # print(str(recording_index)+' 번 dataset에 캐치')
                
            if recording_index == 0:
                recording_index = 2
            elif recording_index == 1:
                recording_index = 2
            print('play question')
            server_command.playVideo(room_id)
            return True
    for i in dataSet2[recording_index][1]:        
        if i in strRes:
            # 이전 녹음 스레드를 정지
            # print(str(recording_index)+' 번 dataset에 캐치')
            threadStop()
            print('pixed response')
            server_command.playVideo1(room_id, dataSet1[recording_index])
            if recording_index == 0:
                recording_index = 1
            return True
    
    return False


def threadStop() :
    global thread_list1
    global recording_index
    global canRecording
    canRecording[recording_index] = False
    targetThread = thread_list1[recording_index]
    i = 0
    for targetThread in thread_list1:
        
        if targetThread != NULL:
            targetThread.raise_exception()
            targetThread = NULL
        elif i == recording_index+1:
            break
        i += 1

class recorder(thread_with_exception):

    def __init__(self, name):
        super().__init__(name)

    def run(self):
        if(server_command.isPlaying(room_id) == False):
            global canRecording
            global recording_index
            global timeOut

            print(str(self.name)+ " index recording start")

            r = sr.Recognizer()
            with sr.Microphone(sample_rate=16000) as source:
                audio = r.listen(source)
                
            canRecording[recording_index] = True

            print(str(self.name)+ " index recording end")

            strRes = stt(audio)

            ########################################## 기본 루프

            if strRes != NULL and choseLine(strRes):
                canRecording[recording_index] = True
                t2 = timeStopper(timeoutNum, stopper)
                t2.raise_exception()
                t2.start()
                timeOut = True

                while timeOut == True :
                    if canRecording[recording_index]:
                        t1 = recorder(recording_index)
                        thread_list1[recording_index] = t1
                        t1.start()
                        canRecording[recording_index] = False
                    time.sleep(0.5)
        else:
            canRecording[recording_index] = True
# main
while True:
    if canRecording[0] == True:
        server_command.displayWordCloud(room_id)
        t1 = recorder(recording_index)
        thread_list1[recording_index] = t1
        t1.start()

        canRecording[0] = False
    time.sleep(0.5)
