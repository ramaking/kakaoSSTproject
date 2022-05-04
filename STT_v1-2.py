from concurrent.futures.process import _get_chunks
import sys
import threading
from tracemalloc import start
import requests
import json
import speech_recognition as sr
import time
import server_command

room_id = 12345

kakao_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
kakao_header = {
    #"Transfer-Encoding": "chunked",
    "Content-Type": "application/octet-stream",
    "Authorization": "KakaoAK " + "5bdcd793f13bebf5e4e874d636b694c0"
}
canRecording = True
device_index = 0

# for device_index, name in enumerate(sr.Microphone.list_microphone_names()):
#     #print(f'{device_index}, {name}')
#     if name == '스테레오 믹스(Realtek(R) Audio)':
#         break


def Reset():
    print("reset")


dataSet1 = ['1111-1111', '2222-2222', '3333-3333']
dataSet2 = [
    ['질문하세요', '궁금한게 있는 사람'],
    ['질문하세요', '질문이 뭔가요?'],
    ['끝났나요?', '더 이상 질문 없나요?']
]


def record(recordLine):
    global canRecording
    print("recording start")
    r = sr.Recognizer()
    #마이크 말고 스테레오 믹스
    # with sr.Microphone(device_index=device_index,sample_rate=16000) as source:
    with sr.Microphone(sample_rate=16000) as source:
        audio = r.listen(source)

    canRecording = True
    res = requests.post(kakao_url, headers=kakao_header,
                        data=audio.get_raw_data())
    line = res.text.splitlines()
    strRes = line[-2]
    jsonRes = json.loads(strRes)
    w = jsonRes["value"]
    print('결과 : ' + jsonRes["value"])
    # for i in dataSet2[recordLine]:
    if recordLine in w:
        canRecording = False
        server_command.playVideo(room_id)
            # play_video.playselectiveVideo(room_id, requestNum)

            # 10초 이내에 이후에 문답을 이어갈 맨트를 받음
            # threading.Timer(10,Reset).start()

        print('등록된 질문이 있습니다.')
    else:
        print('질문단어 캐치x')
    sys.exit(0)


while True:
    if canRecording == True:
        recordLine = 0
        t = threading.Thread(target=record, args='질문')
        t.start()
        canRecording = False
    time.sleep(0.5)
