import requests 
import json
import websocket
import ssl
import thread
import time

from lxml import etree

from xml.etree import ElementTree



import xml.etree.cElementTree as ET

xml_click = open('httpfeedback.xml').read()

def authenticated():
	url = "http://10.80.26.136/xmlapi/session/begin"
	headers = {'Authorization': 'Basic c2FsZXM6Y29sYWI='}
	response = requests.request("POST", url, headers=headers)
	print str(response.cookies)[27:101]
	return str(response.cookies)[27:101]


def test(cookie):
	#url = "http://10.80.26.136/getxml?location=event/Audio"
	url = "http://10.80.26.136/getxml?location=/Status/Audio"
	#headers = {'Cookie': cookie}
	headers = {'Authorization': 'Basic c2FsZXM6Y29sYWI='}
	response = requests.request("GET", url, headers=headers)

	root = etree.fromstring(str(response.text))
	print etree.tostring(root, pretty_print=True)
	print response

def feedback():

	url = 'http://10.80.26.136/putxml'
	headers = {'Content-Type': 'text/xml', 'Authorization': 'Basic c2FsZXM6Y29sYWI='}
	response = requests.request("POST", url, data=xml_click, headers=headers)

	root = etree.fromstring(str(response.text))
	print etree.tostring(root, pretty_print=True)
	print response



#this works --listens on the open websocket for subscribed events



if __name__ == '__main__':
	cookie = authenticated()
	test(cookie)
	feedback()
	#url = "ws://127.0.0.1:8088/examples/websocket/echoProgrammatic"
	#url = 'ws://localhost:5000/websocket'
	#print url

		#opening the websocket with the API token
	#ws = websocket.WebSocketApp(url)#(sslopt={"cert_reqs": ssl.CERT_NONE})
	#ws.run_forever()
	#ws.connect(url)
	# #ws.connect("ws://127.0.0.1:8000")
	#thread.start_new_thread(listen, (ws,))
	#test(authenticated())
	#print "\n\n\n\n\n"
	#authenticated()
	#test()
	#feedback()