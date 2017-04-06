__author__ = "Kiara Montalvo, Annett Samuels, Eduardo Miralles"
__email__ = "kmontalv@cisco.com"
__status__ = "Development"


import requests 
import json
import websocket
import ssl
import thread
import time
from flask import Flask, abort, request

import tpcallme 

from lxml import etree
from xml.etree import ElementTree
import xml.etree.cElementTree as ET


xml_click = open('httpfeedback.xml').read()

user = 'sales'
password = 'colab'


def authenticated(user,password):
	url = "http://10.80.26.136/xmlapi/session/begin"
	response = requests.request("POST", url, auth=(user,password))

	cookie = response.cookies
	print cookie

	cookie2 = str(response.cookies)[37:101]
	print cookie2

	cookie3 = {str(response.cookies)[27:36] : str(response.cookies)[37:101]}
	print cookie3

	return cookie

def test(cookie3):
	url = "http://10.80.26.136/getxml?location=/Status/Audio"
	#headers = {'Cookie': cookie}
	#headers = {'Authorization': 'Basic c2FsZXM6Y29sYWI='}
	#response = requests.request("GET", url, headers=headers)
	response = requests.request("GET", url, cookies=cookie3)

	root = etree.fromstring(str(response.text))
	print etree.tostring(root, pretty_print=True)
	print response

def feedback():

	url = 'http://10.80.26.136/putxml'
	headers = {'Content-Type': 'text/xml'}
	response = requests.request("POST", url, data=xml_click, cookies=cookie3)

	root = etree.fromstring(str(response.text))
	print etree.tostring(root, pretty_print=True)
	print response



app = Flask(__name__)


@app.route('/foo', methods=['POST']) 
def foo():
	
	data = request.get_data()
	#data = request.stream.read()
	print data
	print 'Hello'
	root = etree.fromstring(str(data))

	#print root
	widget_id = root[1][0][0][0][0].text
	print widget_id
	status = root[1][0][0][0][2].text
	print status
	print type(status)

	if widget_id == "coffee" and status == "clicked":
		tpcallme.callme()
		print 'ok'
	elif widget_id == "security" and status == "clicked":
		tpcallme.callsec()
		print 'ok'
	elif status != '':
		print 'No'


	return data
	return status


if __name__ == '__main__':

	#authenticated(user,password)
	cookie3 = authenticated(user,password)
	#authenticated()
	test(cookie3)
	feedback()
	
	app.run(host='0.0.0.0', port=5001, debug=True)
	
