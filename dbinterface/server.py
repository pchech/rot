import pika
import psycopg2
import os
import datetime
from time import sleep
import json

sleep(60)
connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='rabbit',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='tickets',exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='tickets', queue=queue_name)


def callback(ch, method, properties, message_body):
	body = json.loads(message_body)
	conn = psycopg2.connect(dbname=os.environ.get('POSTGRES_DB'),user=os.environ.get('POSTGRES_USER'),password=os.environ.get('POSTGRES_PASSWORD'),host='db')
	cur = conn.cursor()
	select = "INSERT INTO tickets_data(company_id,price,departure_place,arrival_place,departure_date,arrival_date,event_time,url) values (%s,%s,%s,%s,%s,%s,%s,%s);"
	for key,value in body.items():	
		data = (key,value['price'],value['dep'],value['arr'],value['start'],value['end'],datetime.datetime.now(),value['url'])
		cur.execute(select,data)
	conn.commit()
	cur.close()
	conn.close()


channel.basic_consume(
	queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()