from concurrent.futures.process import _get_chunks
import threading
import requests
import json
import speech_recognition as sr

url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
header = {
        #"Transfer-Encoding": "chunked",
        "Content-Type": "application/octet-stream",
        "Authorization" : "KakaoAK " + "5bdcd793f13bebf5e4e874d636b694c0"
         }
canRecording = True
device_index = 0
for device_index, name in enumerate(sr.Microphone.list_microphone_names()):
    #print(f'{device_index}, {name}')
    if name == '스테레오 믹스(Realtek(R) Audio)':
        break

def record():
    global canRecording
    print("recording start")
    r = sr.Recognizer()
    #마이크 말고 스테레오 믹스
    with sr.Microphone(device_index=device_index,sample_rate=16000,chunk_size=1024) as source:
        audio = r.listen(source)
    canRecording = True
    res = requests.post(url, headers=header, data=audio.get_raw_data())
    #res = requests.post(url, headers=header, data=get_chunks(audio))
    #print(res.text)
    line = res.text.splitlines()
    strRes = line[-2]
    jsonRes = json.loads(strRes)
    print('결과 : ' + jsonRes["value"])

while True:
    if canRecording == True:
        t = threading.Thread(target=record)
        t.start()
        canRecording = False


