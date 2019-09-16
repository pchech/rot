from flask import Flask, request
import os
import requests

token = os.environ.get('TOKEN')
server = Flask(__name__)

	
@server.route('/rot', methods=['POST'])
def sendMessage():
	url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
	data = {
		'chat_id':'125884788',
		'text':'Hello! How are you ?'
	}
	rsp = requests.post(url = url,data=data)
	return "!", 200

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
