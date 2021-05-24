import requests
import json
import sys
import re
import os
import argparse

##ARGUMENT PARSEING###
parser = argparse.ArgumentParser(prog='ccarchiver', description='Create a local archive of CuriousCat accounts.')
parser.add_argument('-f', '--file', action='store_true', help='use a file containing a list of usernames on seperate lines instead')
parser.add_argument('Username', help='The Username of the account to archive, or file containing usernames')

args = vars(parser.parse_args())

if args['file'] == False:
	usernames = [args['Username']]
else:
	if not os.path.isfile(args['Username']):
		print('The file specified does not exist')
		sys.exit()
	f = open(args['Username'])
	usernames = f.read().splitlines()


#Main Loop
for namecount, username in enumerate(usernames):
	print("Archiving %s, [%d/%d]" % (username,namecount,len(usernames)))

	url = "https://curiouscat.qa/api/v2.1/profile"
	querystring = {"username":username}

	response = requests.request("GET", url, params=querystring)

	fullJson = response.json()

	if 'error' in fullJson.keys():
		print("User '%s' could not be found" % username)
		break

	#Set Directory
	workingdir = os.getcwd()
	workingdir = os.path.join(workingdir, '%sCCArchive' % username)
	if not os.path.exists(workingdir):
	   os.makedirs(workingdir)
	os.chdir(workingdir)

	print ("Downloading Answers for %s..." % username)
	#Get Post Archive
	answercount = fullJson['answers']
	while True:
		try:
			if fullJson['posts'][-1]['type'] == "post":
				lastTimestamp = fullJson['posts'][-1]['post']['timestamp']
			elif fullJson['posts'][-1]['type'] == "status":
				lastTimestamp = fullJson['posts'][-1]['status']['timestamp']
			elif fullJson['posts'][-1]['type'] == "shared_post":
				lastTimestamp = fullJson['posts'][-1]['shared_timestamp']
			else:
				print(json.dumps(fullJson['posts'][-1]))
				raise
		except Exception as e:
			print(json.dumps(fullJson['posts'][-1]))
			raise e
		


		querystring = {"username":username,"max_timestamp":lastTimestamp-1}
		response = requests.request("GET", url, params=querystring)

		if response.json()['posts'] == []:
			break

		fullJson['posts'] = fullJson['posts'] + response.json()['posts']

		print("%d/%d" % (len(fullJson['posts']),answercount))
		pass


	print("Saving Raw Json to file: %sAnswers.json" % username)
	#WriteToFile
	out = open("%sAnswers.json" % username, 'w')
	out.write(json.dumps(fullJson))

	#Check For Local Copy
	while True:
		yesno = input("Would you like to download all media attached to this CuriousCat Profile [y/n]: ")
		if yesno.lower() == "yes" or yesno.lower() == "y":
			break
		if yesno.lower() == "no" or yesno.lower() == "n":
			print("Please view the json file using the provided viewer.html file.")
			quit()
		pass


	print("Extracting Links From Json...")
	#Extracts Links From Raw JSON
	jsonraw = json.dumps(fullJson)

	regexQuery = '(https?://[^ ]*?\.curiouscat.qa/.+?)"'

	alllinks = re.findall(regexQuery, jsonraw)

	links = []

	for link in alllinks:
		if link not in links:
			links.append(link)


	print("Downloading Images...")
	#Download Local Copy of images


	media_directory = os.path.join(workingdir, 'Media')
	if not os.path.exists(media_directory):
	   os.makedirs(media_directory)


	for index, link in enumerate(links):
		linkpath = re.sub('(/|https?://[^ ]*?\.curiouscat.qa/)', '', link)
		response = requests.get(link)

		print("Downloading %d/%d" % (index + 1, len(links)))
		with open('Media/' + linkpath, 'wb') as f:
			f.write(response.content)


	print("Replacing Links...")
	#Create Copy of Json With Links Replaced
	localfile = open("local%sAnswers.json" % (username), 'w')

	localJson = re.split(r'(https?://[^ ]*?\.curiouscat.qa/.+?)"', jsonraw)
	localJson = ''.join(['%sCCArchive/Media/%s"' % (username, re.sub('(https?:/?/?[^ ]*?\.curiouscat.qa)|/', '', string)) if re.match(r'(https?://[^ ]*?\.curiouscat.qa/.+?)', string) != None else string for string in localJson])

	localfile.write(localJson)
	localfile.close()
