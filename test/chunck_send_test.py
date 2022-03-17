import http.client
import threading
import requests
import json
import speech_recognition as sr
import httplib

def chunk_data(data, chunk_size):
    dl = len(data)
    ret = ""
    for i in range(dl // chunk_size):
        ret += "%s\r\n" % (hex(chunk_size)[2:])
        ret += "%s\r\n\r\n" % (data[i * chunk_size : (i + 1) * chunk_size])

    if len(data) % chunk_size != 0:
        ret += "%s\r\n" % (hex(len(data) % chunk_size)[2:])
        ret += "%s\r\n" % (data[-(len(data) % chunk_size):])

    ret += "0\r\n\r\n"
    return ret

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

def chunk_data(data, chunk_size):
    dl = len(data)
    ret = ""
    for i in range(dl // chunk_size):
        ret += "%s\r\n" % (hex(chunk_size)[2:])
        ret += "%s\r\n\r\n" % (data[i * chunk_size : (i + 1) * chunk_size])

    if len(data) % chunk_size != 0:
        ret += "%s\r\n" % (hex(len(data) % chunk_size)[2:])
        ret += "%s\r\n" % (data[-(len(data) % chunk_size):])

    ret += "0\r\n\r\n"
    return ret

def record():
    global canRecording
    print("recording start")
    r = sr.Recognizer()
    #마이크 말고 스테레오 믹스
    with sr.Microphone(device_index=device_index,sample_rate=16000) as source:
        audio = r.listen(source)
    canRecording = True

    # res = requests.post(url, headers=header, data=audio.get_raw_data())
    # #res = requests.post(url, headers=header, data=get_chunks(audio))
    # #print(res.text)
    # line = res.text.splitlines()
    # strRes = line[-2]
    # jsonRes = json.loads(strRes)
    # print('결과 : ' + jsonRes["value"])

    host = 'kakaoi-newtone-openapi.kakao.com';
    url1 = '/v1/recognize';
    conn = http.client.HTTPConnection(host)
    conn.putrequest('POST', url1)
    conn.putheader('Transfer-Encoding', 'chunked')
    conn.putheader('Content-Type', 'application/octet-stream')
    conn.putheader('Authorization', 'KakaoAK 5bdcd793f13bebf5e4e874d636b694c0')
    conn.endheaders()
    conn.send(chunk_data(audio.get_raw_data(), 1024).encode('utf-8'))

    resp = conn.getresponse()
    print(resp.status, resp.reason)
    conn.close()

while True:
    if canRecording == True:
        t = threading.Thread(target=record)
        t.start()
        canRecording = False


