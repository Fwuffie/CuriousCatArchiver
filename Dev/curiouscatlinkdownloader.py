import requests
import json
import re
import sys
import os

print("Extracting Links...")

#Extracts Links From Raw JSON
fileArg = str(sys.argv[1])
file = open(fileArg, "r")
jsonraw = file.read()
file.close()

regexQuery = '(https?://[^ ]*?\.curiouscat.qa/.+?)"'

alllinks = re.findall(regexQuery, jsonraw)

links = []

for link in alllinks:
	if link not in links:
		links.append(link)


print("Downloading Images...")
#Download Local Copy of images

workingdir = os.getcwd()
final_directory = os.path.join(workingdir, 'Media')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)


for index, link in enumerate(links):
	linkpath = re.sub('(/|https?://[^ ]*?\.curiouscat.qa/)', '', link)
	response = requests.get(link)

	print("Downloading %d/%d" % (index + 1, len(links)))
	with open('Media/' + linkpath, 'wb') as f:
		f.write(response.content)


print("Replacing Links...")
#Create Copy of Json With Links Replaced
localfile = open("local%s" % (fileArg), 'w')

localJson = re.split(r'(https?://[^ ]*?\.curiouscat.qa/.+?)"', jsonraw)
localJson = ''.join(['Media/%s"' % re.sub('(https?:/?/?[^ ]*?\.curiouscat.qa)|/', '', string) if re.match(r'(https?://[^ ]*?\.curiouscat.qa/.+?)', string) != None else string for string in localJson])

localfile.write(localJson)