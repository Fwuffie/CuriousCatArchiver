import requests
import json
import sys
import re
import os
import argparse
import datetime
import time

###Setvars
url = "https://curiouscat.qa/api/v2.1/profile"
concurrentUserDownloads = 5

initialdir = os.getcwd()
downloadLocal = None


##ARGUMENT PARSEING###
parser = argparse.ArgumentParser(prog='ccarchiver', description='Create a local archive of CuriousCat accounts.')
parser.add_argument('-f', '--file', action='store_true', help='use a file containing a list of usernames on seperate lines instead')
parser.add_argument('-v', '--verbose', action='store_true', help='Display verbose Output')
parser.add_argument('-l', '--local', action='store_true', help='Automatically Download Local Copys')
parser.add_argument('Username', help='The Username of the account to archive, or file containing usernames')

args = vars(parser.parse_args())

if args['local'] == True:
	downloadLocal = True

if args['file'] == False:
	usernames = [args['Username']]
else:
	if not os.path.isfile(args['Username']):
		print('The file specified does not exist')
		sys.exit()
	f = open(args['Username'])
	usernames = f.read().splitlines()


#Print only if verbose
def vprint(string):
	if args['verbose']:
		print(string)
	else:
		print(string + "                          ", end='\r')
	return

#Main Function to downloadUserAnswers
def downloadUserAnswers(username):
	#Get The Main Content Of A User Profile
	querystring = {"username":username}
	response = requests.request("GET", url, params=querystring)
	fullJson = response.json()
	if 'error_code' in fullJson.keys():
		if fullJson['error_code'] == 'profile_does_not_exist':
			print("User '%s' could not be found, skipping." % username)
		elif fullJson['error_code'] == 'ratelimited':
			time.sleep(20)
			downloadUserAnswers(username)
		return

	vprint("Archiving %s" % (username))

	#Set Directory
	workingdir = os.path.join(initialdir, 'CCArchive%s' % username)
	if not os.path.exists(workingdir):
	   os.makedirs(workingdir)
	
	while not os.path.exists(workingdir):
		time.sleep(1)

	os.chdir(workingdir)

	#Get Post Archive
	answercount = fullJson['answers']
	while True and answercount > 0:
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

		vprint("Downloading Answers for %s [%d/%d]" % (username,len(fullJson['posts']),answercount))
		pass

	
	#WriteToFile
	vprint("Saving %s's Raw Json to file: %sAnswers.json" % (username, username))
	out = open("%sAnswers.json" % username, 'w')
	out.write(json.dumps(fullJson))

	#Check For Local Copy
	if downloadLocal == False:
		return


	
	#Extracts Links From Raw JSON
	vprint("Extracting %s's Links From Json..." % (username))
	jsonraw = json.dumps(fullJson)

	regexQuery = '(https?://[^ ]*?\.curiouscat.qa/.+?)"'

	alllinks = re.findall(regexQuery, jsonraw)

	links = []

	for link in alllinks:
		if link not in links:
			links.append(link)


	#Download Local Copy of images
	media_directory = os.path.join(workingdir, 'Media')
	if not os.path.exists(media_directory):
	   os.makedirs(media_directory)


	for index, link in enumerate(links):
		linkpath = re.sub('(/|https?://[^ ]*?\.curiouscat.qa/)', '', link)
		response = requests.get(link)

		vprint("Downloading %s's Images [%d/%d]..." % (username, index + 1, len(links)))
		with open('Media/' + linkpath, 'wb') as f:
			f.write(response.content)


	#Create Copy of Json With Links Replaced
	vprint("Creating Local Copy Of %s's File..." % (username))
	localfile = open("local%sAnswers.json" % (username), 'w')

	localJson = re.split(r'(https?://[^ ]*?\.curiouscat.qa/.+?)"', jsonraw)
	localJson = ''.join(['CCArchive%s/Media/%s"' % (username, re.sub('(https?:/?/?[^ ]*?\.curiouscat.qa)|/', '', string)) if re.match(r'(https?://[^ ]*?\.curiouscat.qa/.+?)', string) != None else string for string in localJson])

	localfile.write(localJson)
	localfile.close()
	return


#def run_parallel():
#	'''
#	Run functions in parallel
#	'''
#	from multiprocessing import Process
#	processes = []
#	for namecount, username in enumerate(usernames):
#		print("Archiving %s, [%d/%d]" % (username,namecount + 1,len(usernames)))
#		proc = Process(target=downloadUserAnswers, args=(username,))		
#		processes.append(proc)
#		proc.start()
#	for p in processes:
#		p.join()

def downloadUserAnswersCatcher(username):
	try:
		downloadUserAnswers(username)
		pass
	except KeyboardInterrupt:
		quit()


if __name__ == '__main__':
	while downloadLocal == None:
		yesno = input("Would you like to download all media attached to the CuriousCat Profile [y/n]: ")
		if yesno.lower() == "yes" or yesno.lower() == "y":
			downloadLocal = True
		if yesno.lower() == "no" or yesno.lower() == "n":
			print("Please view the json file using the provided viewer.html file.")
			downloadLocal = False
		pass


	from multiprocessing import Pool
	try:
		pool = Pool(processes=concurrentUserDownloads)
		pool.map(downloadUserAnswers, usernames)
		#run_parallel()
	except KeyboardInterrupt:
		pool.close()
		pool.terminate()
		pool.join()
		print('Exited By User')
		quit()


#Main Loop
#for namecount, username in enumerate(usernames):
#	print("Archiving %s, [%d/%d]" % (username,namecount + 1,len(usernames)))
#	downloadUserAnswers(username)

#print("Archives can now be viewed using viewer.html")