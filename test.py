import requests
import json
url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
header = {"Content-Type": "application/octet-stream",
          "Authorization" : "KakaoAK " + "5bdcd793f13bebf5e4e874d636b694c0"
         }
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone(sample_rate=16000) as source:
    print("말해보세요!!")
    audio = r.listen(source)
res = requests.post(url, headers=header, data=audio.get_raw_data())
print(res.text)


