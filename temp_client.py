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

ser = serial.Serial('/dev/ttyACM3', 9600, timeout=2)
ser.open

while True:
    print "loop start"
    current_temperature = int(ser.readline(), base=10)
    current_time = str(datetime.datetime.now())

    payload = {'time':current_time,'current_temperature':current_temperature}
    jsonString = json.dumps(payload)
    print (jsonString)
    requests.post('http://13.59.174.162:7579/temperature', data=payload)
    print "request posted"
    time.sleep(2.5)
    print "loop finished"
