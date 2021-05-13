import requests
import json
import sys

username = str(sys.argv[1])

url = "https://curiouscat.qa/api/v2.1/profile"
querystring = {"username":username}

response = requests.request("GET", url, params=querystring)

fullJson = response.json()

if 'error' in fullJson.keys():
	print("User could not be found.")
	quit()


postcount = fullJson['answers']


#Get Post Archive
while True:
	lastTimestamp = fullJson['posts'][-1]['post']['timestamp']
	querystring = {"username":username,"max_timestamp":lastTimestamp-1}
	response = requests.request("GET", url, params=querystring)

	if response.json()['posts'] == []:
		break

	fullJson['posts'] = fullJson['posts'] + response.json()['posts']

	print("%d/%d" % (len(fullJson['posts']),postcount))
	pass

#WriteToFile
out = open("%sAnswers.json" % username, 'w')
out.write(json.dumps(fullJson))

print("Saving Json to file: %sAnswers.json" % username)

while True:
	yesno = input("Would you like to download all media attached to this CuriousCat Profile [y/n]: ")
	if yesno.lower() == "yes" or yesno.lower() == "y":
		break
	if yesno.lower() == "no" or yesno.lower() == "n":
		quit()
	pass