import requests
import json
import traceback
from datetime import datetime
from utils import showPrice
import scyapi
from time import sleep
import os
import pika

#def sendData(price_list):
#	url = 'http://message:5000/rot'
#	data = {'message':price_list}
#	rsp=requests.post(url=url,data=data)

def sendData(price_list):
	connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='rabbit',port=5672))
	channel = connection.channel()

	channel.exchange_declare(exchange='tickets',exchange_type='fanout')

	channel.basic_publish(exchange='tickets', routing_key='', body=price_list)
	connection.close()

if __name__=="__main__":
	sleep(60)
	session=scyapi.getSession()
	scyapi.pollData(session)
	sendData(json.dumps(scyapi.price_list))
	#print(scyapi.price_list)
	while True:
		sleep(300)
		#sendData("Start {}".format(datetime.now()))
		try:
			session=scyapi.getSession()
			scyapi.pollData(session)
			#sendData("Changed {}".format(scyapi.changed))
			sendData(json.dumps(scyapi.price_list))
		except Exception as e:
 			#sendData(traceback.format_exc())
			pass
