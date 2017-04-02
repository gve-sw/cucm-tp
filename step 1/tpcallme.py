import requests
import json
from xml.etree import ElementTree



import xml.etree.cElementTree as ET

xml_click = open('clickwidget.xml').read()
xml_string = open('dial.xml').read()


def waitforclick():

	url = 'http://10.80.26.136/getxml?location=/Status'
	headers = {'Content-Type': 'text/xml', 'Authorization': 'Basic c2FsZXM6Y29sYWI='}
	response = requests.request("GET", url, headers=headers)
	response2 = requests.get(url, headers=headers)

	print response2

	file = open("out.xml", "w")
	file.write(response.content)
	file.close()

waitforclick()

def callme():

	url = 'http://10.80.26.136/putxml'
	headers = {'Content-Type': 'text/xml', 'Authorization': 'Basic c2FsZXM6Y29sYWI='}
	response = requests.request("POST", url, data=xml_string, headers=headers)

if __name__ == '__main__':
	callme()
