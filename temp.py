import Adafruit_DHT as dht
import datetime
from threading import Timer
import threading
import requests
import json
import urllib2
import httplib as http
import time

def printit():
        wtime = datetime.datetime.now()
        humidity, temperature = dht.read_retry(dht.DHT22, 4)
	return wtime, humidity, temperature

while 1:
        wtime, humidity, temperature = printit()
        
        response = requests.get('http://13.59.174.162:7579/temperature')
        req_temp = response.text
        print req_temp

        diff_temp = float(req_temp) - temperature
        state = ""
        if diff_temp > 0 :
                state = "up"
        elif diff_temp < 0 :
                state = "down"
        else :
                state = "..."

        data = "Time:" + str(wtime) + ' Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature,humidity)
        data = json.loads(json.dumps(data))
        print data
        print "{0:0.1f}".format(abs(diff_temp)) + " " + state
        
	r = requests.post('http://13.59.174.162:7579/temperature', json={'data': data})
	print r.text
	time.sleep(10)
