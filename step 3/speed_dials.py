__author__ = "Kiara Montalvo, Annett Samuels, Eduardo Miralles"
__email__ = "kmontalv@cisco.com"
__status__ = "Development"


import requests
from lxml import etree
from xml.etree import ElementTree
import xml.etree.cElementTree as ET

xml_getPhone = open('speed_dials.xml').read()


user = 'administrator'
password = 'ciscopsdt'

def feedback(user,password):
	url = 'https://10.10.20.1:8443/axl/'
	headers = {'Content-Type': 'text/xml'}
	response = requests.request("POST", url, auth=(user,password), data=xml_getPhone, headers=headers, verify=False)

	root = etree.fromstring(str(response.text))
	print etree.tostring(root, pretty_print=True)
	print response
	
if __name__ == '__main__':


	user = 'administrator'
	password = 'ciscopsdt'
	
	feedback(user,password)