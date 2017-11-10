#!/usr/bin/python
# coding=utf8
import Adafruit_DHT as dht
import datetime
from threading import Timer
import threading
import requests
import json
import urllib2
import httplib as http
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
ser.open

global previous_temperature

def temp_print(previous_temperature, current_temperature):
    #제대로 센서가 값을 읽어왔을 때
    if current_temperature > 20 and current_temperature < 30:
        if previous_temperature is current_temperature :
            print "Previous Temperature: " + str(previous_temperature) + " Current Temperature: " + str(current_temperature)
            print "Not Changed"
        else :
            temperature = "Previous Temperature: " + str(previous_temperature) + " Current Temperature: " + str(current_temperature)
            print temperature
            
def temp_on(current_temperature, previous_temperature, req_temp):
    #에러 체크 - previous 온도와 current 온도가 10도 이상 차이나면 오류 발생
    if abs(current_temperature - previous_temperature) > 10:
        print False
    #request 온도가 20도 이하가 되면 히터 켜줌
    elif req_temp <= 20 :
        print "Turn heat on"
    #request 온도가 30도 이상이 되면 에어컨 켜줌
    elif req_temp >= 30 :
        print "Turn cool on"
    else :
        print "Do not touch"

previous_temperature = int(ser.readline())

while True:
    print "loop start"
    current_temperature = int(ser.readline(), base=10)
    current_time = str(datetime.datetime.now())
    #에어컨의 희망 온도 받아오기
    response = requests.get('http://13.59.174.162:7579/temperature')
    req_temp = int(response.text)
    print req_temp
    
    temp_print(previous_temperature, current_temperature)
    temp_on(current_temperature, previous_temperature, req_temp)

    print "\n"
    payload = {'time':current_time,'current_temperature':current_temperature}
    jsonString = json.dumps(payload)
    print (jsonString)
    requests.post('http://13.59.174.162:7579/temperature', data=payload)
    print "request posted"
    previous_temperature = current_temperature
    time.sleep(2.5)
    print "loop finished"
