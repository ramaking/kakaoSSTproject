import threading
import requests
import json
import speech_recognition as sr

url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
header = {
        #"Transfer-Encoding: chunked"
        "Content-Type": "application/octet-stream",
        "Authorization" : "KakaoAK " + "5bdcd793f13bebf5e4e874d636b694c0"
         }
canRecording = True

def record():
    global canRecording
    print("recording start")
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        audio = r.listen(source)
    canRecording = True
    res = requests.post(url, headers=header, data=audio.get_raw_data())
    line = res.text.splitlines()
    strRes = line[-2]
    jsonRes = json.loads(strRes)
    print('결과 : ' + jsonRes["value"])

while True:
    if canRecording == True:
        t = threading.Thread(target=record)
        t.start()
        canRecording = False







