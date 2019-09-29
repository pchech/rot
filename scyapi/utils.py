def showPrice(price_list):
	price_list = dict(sorted(list(price_list.items()),key = lambda x:x[1]['price']))
	str=''
	for key,value in price_list.items():
		str+='*Company*: {}\n*Departure*: {}\n*Arrival*: {}\n*Price: {}* [Buy Ticket]({})\n'.format(key.upper(),value['start'],value['end'],value['price'],value['url'])
	return str