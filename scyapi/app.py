import requests
import json
import traceback
from datetime import datetime
from utils import showPrice
from scyapi import *
from time import sleep
import os

def sendData(price_list):
	url = 'http://tg:5000/rot'
	data = {'message':price_list}
	rsp=requests.post(url=url,data=data)

if __name__=="__main__":
	session=getSession()
	pollData(session)
	sendData(showPrice(price_list))
	#print(showPrice(price_list))
	while True:
		print("Start {}".format(datetime.now()))
		changed=0
		sleep(1800)
		try:
			session=getSession()
			pollData(session)
			if changed:
				sendData(showPrice(price_list))
		except Exception as e:
 			sendData(traceback.format_exc())
