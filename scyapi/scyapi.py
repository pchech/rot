import requests
import json
from datetime import datetime
from datetime import timedelta
import os
token = os.environ.get('TOKEN')
host = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com'
price_list = {}
originPlace='MOSC-sky'
destinationPlace='LED-sky'


def getSession():
	session_path = 'apiservices/pricing/v1.0'
	session_url = '{}/{}'.format(host,session_path)
	
	
	outboundDate=(datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d')
	payload = "cabinClass=economy&children=0&infants=0&country=RU&currency=RUB&locale=ru-RU&originPlace={}&destinationPlace={}&outboundDate={}&adults=1".format(originPlace,destinationPlace,outboundDate)
	headers = {
		'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
		'x-rapidapi-key': token,
		'content-type': "application/x-www-form-urlencoded"
		}

	response = requests.request("POST", session_url, data=payload, headers=headers)
	location = response.headers['Location'][-36:]
	return location
def pollData(session):
	poll_path = 'apiservices/pricing/uk2/v1.0'
	poll_url = '{}/{}/{}'.format(host,poll_path,session)

	carrier_list = ['su','s7','u6','dp']
	for car in carrier_list:
		querystring = {"sortType":"price","sortOrder":"asc","stops":"0","pageSize":1,"pageIndex":0,'includecarriers':car}

		headers = {
			'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
			'x-rapidapi-key': token
			}

		response = requests.request("GET", poll_url, headers=headers, params=querystring)

		d = json.loads(response.text)
		if d['Itineraries'] == []:
			price_list.pop(car)
		for leg in d['Itineraries']:
			price_o={}
			price = leg['PricingOptions'][0]['Price']
			url = leg['PricingOptions'][0]['DeeplinkUrl']
			price_o['price']=price
			price_o['url']=url
			for l in d['Legs']:
				if l['Id']==leg['OutboundLegId']:
					start=l['Departure']
					end=l['Arrival']
					price_o['start']=datetime.strptime(start,'%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
					price_o['end']=datetime.strptime(end,'%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
					price_o['dep']=originPlace
					price_o['arr']=destinationPlace
				price_list[car]=price_o
			#try:
				
			#	if price != price_list[car]['price'] or (datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d')!=datetime.strptime(price_list[car]['start'],'%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d'):
			#		changed = 1        
				#	price_list[car]=price_o
			#except KeyError:
			#	changed = 1 
				#price_list[car]=price_o
		
