import requests
import json
from xml.etree import ElementTree
import xml.etree.cElementTree as ET


#Send an HTTP Post Request to call a user from the CODEC. The function uses the variable user_email as an input attribute. This variable is defined in the wrapper API.

def call(user_email):

	url = 'http://10.80.26.136/putxml'
	headers = {'Content-Type': 'text/xml', 'Authorization': 'Basic c2FsZXM6Y29sYWI='}
	data = '<Command><Dial command="True"><Number>"'+user_email+'"</Number><Protocol>Sip</Protocol></Dial></Command>'
	response = requests.request("POST", url, data=data, headers=headers)


if __name__ == '__main__':
	call(coffee_email)