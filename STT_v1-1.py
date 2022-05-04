import requests
import json
import speech_recognition as sr
import server_command
url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
header = {"Content-Type": "application/octet-stream",
          "Authorization" : "KakaoAK " + "5bdcd793f13bebf5e4e874d636b694c0"
         }
r = sr.Recognizer()
ROOMID=12345

while True:
    with sr.Microphone(sample_rate=16000) as source:
        print("catching. . .")
        audio = r.listen(source)

    res = requests.post(url, headers=header, data=audio.get_raw_data())

    line = res.text.splitlines()
    #print(res.txt)
    #json_string = requests.get(line).text

    strRes = line[-2]
    jsonRes = json.loads(strRes)
    #data = json.loads(json_string)

    #print(data)
    w = jsonRes["value"]
    #s = res.text
    print(w)
    # print(res.text)
    #print(line.count("내리실"))
    if '질문' in w:
        # play_video.playVideo(ROOMID)
        print('등록된 질문이 있습니다.')
    else: print('질문단어 캐치x')




