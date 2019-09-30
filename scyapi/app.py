import requests
import json
import traceback
from datetime import datetime
from utils import showPrice
import scyapi
from time import sleep
import os

def sendData(price_list):
	url = 'http://tg:5000/rot'
	data = {'message':price_list}
	rsp=requests.post(url=url,data=data)

if __name__=="__main__":
	session=scyapi.getSession()
	scyapi.pollData(session)
	sendData(showPrice(scyapi.price_list))
	#print(showPrice(scyapi.price_list))
	while True:
		scyapi.changed=0
		sleep(300)
		#sendData("Start {}".format(datetime.now()))
		try:
			session=scyapi.getSession()
			scyapi.pollData(session)
			#sendData("Changed {}".format(scyapi.changed))
			if scyapi.changed:
				sendData(showPrice(scyapi.price_list))
		except Exception as e:
 			sendData(traceback.format_exc())
