import pika
import psycopg2
import requests
import os
import datetime
from time import sleep
import json

curr_price={}

sleep(60)
connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='rabbit',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='tickets',exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='tickets', queue=queue_name)

def sendData(price_list):
	url = 'http://message:5000/rot'
	data = {'message':price_list}
	rsp=requests.post(url=url,data=data)

def showPrice(price_list):
	flag=0
	str=''
	for row in price_list:
		try:
			if curr_price[row[1]]!=row[2]:
				flag=1
				break
		except KeyError:
			flag=1
			break
	if flag==1:	
		for row in price_list:
			curr_price[row[1]]=row[2]
			str+='*Company*: {}\n*Departure*: {}\n*Arrival*: {}\n*Price: {}* [Buy Ticket]({})\n'.format(row[1],row[5],row[6],row[2],row[8])
	return str

def callback(ch, method, properties, message_body):
	conn = psycopg2.connect(dbname=os.environ.get('POSTGRES_DB'),user=os.environ.get('POSTGRES_USER'),password=os.environ.get('POSTGRES_PASSWORD'),host='db')
	cur = conn.cursor()
	select = "SELECT * FROM tickets_data WHERE event_time > current_timestamp - interval '6' minute order by price"
	cur.execute(select)
	result=cur.fetchall()
	cur.close()
	conn.close()
	result_str=showPrice(result)
	if result_str!='':
		sendData(result_str)


channel.basic_consume(
	queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()