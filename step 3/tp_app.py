__author__ = "Kiara Montalvo, Annett Samuels, Eduardo Miralles"
__email__ = "kmontalv@cisco.com"
__status__ = "Development"


#Import all libraries needed for application.
import requests 
import json
import ssl
import time
from flask import Flask, abort, request
from lxml import etree
from xml.etree import ElementTree
import xml.etree.cElementTree as ET

#Import python applications to Call/Send Spark Message when Widget action in the CODEC is detected.
import tpcallme
import spark_message


#Open the XML file containing the body of the request needed to subscribe a server to CODEC Feedback.
xml_click = open('httpfeedback.xml').read()

#Credentials for CODEC
user = 'sales'
password = 'colab'

#Variables needed to send Call/Spark Messages
ACCESS_TOKEN = "YzYwZjMxYjAtMmU3NS00ZTkzLTllZjMtNTdkZTk0NmQ3MjQ0YTRlNWYxYjAtZjdk" #Put your access token between the quotes
coffee_message = "Can I have coffee for 10 people in Room X Please? Thanks!"  #Put the message that you want to send when you request coffee. 
security_message = "Emergency! Requesting Security to come to Room X."  #Put the message that you want to send when you call security.
DEST_EMAIL = "annesamu@cisco.com" #Indicate the destination e-mail for coffee.
DEST_EMAIL2 = "edmirall@cisco.com" #Indicate the destination e-mail for security.




#Authenticates credentials for CODEC, opens session with CODEC and retrieves cookie for that session. This cookie is used when making other HTTP Requests,
#without the need of opening a new session in each request.
def authenticated(user,password):
	url = "http://10.80.26.136/xmlapi/session/begin"
	response = requests.request("POST", url, auth=(user,password))
	cookie = response.cookies
	print cookie
	return cookie

#Get initial status of Audio Configuration Settings of CODEC. 
def test(cookie3):
	url = "http://10.80.26.136/getxml?location=/Status/Audio"
	response = requests.request("GET", url, cookies=cookie3)
	root = etree.fromstring(str(response.text))
	print etree.tostring(root, pretty_print=True)
	print response

#Sends HTTP Request to Subscribe to CODEC Feedback. Every time a widget is clicked, POST Request will be sent to web server with XML body describing the event
#related to the widget.
def feedback():

	url = 'http://10.80.26.136/putxml'
	headers = {'Content-Type': 'text/xml'}
	response = requests.request("POST", url, data=xml_click, cookies=cookie3)
	root = etree.fromstring(str(response.text))
	print etree.tostring(root, pretty_print=True)
	print response


#Defines flask application to serve as Web Server receiving all the feedback from the CODEC upon the events detected (Widget actions).
app = Flask(__name__)


@app.route('/foo', methods=['POST']) 
def foo():
	
	#Get all requests being posted in the web server (flask application)
	data = request.get_data()
	print data
	print 'Hello'
	root = etree.fromstring(str(data))

	#Parse through HTTP responses Posted on web server and retrieve Widget ID. 
	widget_id = root[1][0][0][0][0].text
	print widget_id
	status = root[1][0][0][0][2].text
	print status
	print type(status)

	#If the widget clicked in the TP is the coffee widget, call the python applications to call (tpcallme.py)/send Spark message (spark_message.py) to coffee recipient. 
	if widget_id == "coffee" and status == "clicked":
		tpcallme.call(DEST_EMAIL)
		header=spark_message.setHeaders(ACCESS_TOKEN)
		spark_message.postMsg(header,DEST_EMAIL,coffee_message)
		print 'ok'
	#If the widget clicked in the TP is the security widget, call the python applications to call (tpcallme.py)/send Spark message (spark_message.py) to security recipient.
	elif widget_id == "security" and status == "clicked":
		tpcallme.call(DEST_EMAIL2)
		header=spark_message.setHeaders(ACCESS_TOKEN)
		spark_message.postMsg(header,DEST_EMAIL2,security_message)
		print 'ok'
	elif status != '':
		print 'No'


	return data
	return status


if __name__ == '__main__':

	cookie3 = authenticated(user,password)
	test(cookie3)
	feedback()
	
	app.run(host='0.0.0.0', port=5001, debug=True)
	
