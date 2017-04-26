import json
import requests



#Set the header to be used for authentication and data format to be sent.
def setHeaders(ACCESS_TOKEN):         
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}     
	return (spark_header)


#Posts a message to the room
def postMsg(the_header,email,message):
	message = '{"toPersonEmail": "'+email+'", "text":"'+message+'"}'
	uri = 'https://api.ciscospark.com/v1/messages'
	resp = requests.post(uri, data=message, headers=the_header)
	print("postMsg JSON: ", resp.json())


    
