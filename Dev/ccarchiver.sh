#!/bin/sh

echo "installing dependancies...";
sudo apt-get -sqqy install zip curl python3 > /dev/null;

echo "Downloading Answers";
python3 curiouscatarchive.py $1;

echo "Retriving Links";
links=$(grep -Poh 'https://(([^ ]+?\.)?curiouscat.qa)[^ ]+?\"' $1Answers.json | sed 's/.$//' | sort | uniq);

echo "Downloading Images";
IFS='
'
count=0
totalimages=$(echo "$links" | wc -l)
for link in $links
do
  count=$((count+1))
  echo "$count / $totalimages	[$link]";
  path=$(echo $link | sed "s/https:\/\//Media\//")
  curl -s -o $1$path --create-dirs $link > /dev/null
done


echo "Creating Local Copy local$1Answers.json";
cat $1Answers.json | sed "s/https:\/\//$1Media\//" > local$1Answers.json;

echo "Compressing into Zip";
zip -r $1CuriousCatArchive.zip local$1Answers.json viewer.html $1Media;
chmod 777 $1CuriousCatArchive.zip;

echo "Removing Temp Files";
rm -r local$1Answers.json $1Answers.json $1Media;

#echo "Copying to Web";
#cp $1CuriousCatArchive.zip /home/neko/www/curiouscatarchiver/;

#echo "The Archive can Be downloaded from https://nyan.ca/curiouscatarchiver/$1CuriousCatArchive.zip";