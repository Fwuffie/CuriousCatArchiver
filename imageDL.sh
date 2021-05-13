#!/bin/sh

echo "Retriving Links";
links=$(grep -Poh 'https://(([^ ]+?\.)?curiouscat.qa)[^ ]+?\"' $1 | sed 's/.$//' | sort | uniq);



echo "Downloading Images";
IFS='
'
count=0
totalimages=$(echo "$links" | wc -l)
for link in $links
do
  count=$((count+1))
  echo "$count / $totalimages	[$link]";
  path=$(echo $link | sed 's/https:\/\//Media\//')
  curl -s -o $path --create-dirs $link > /dev/null
done


echo "Creating Local Copy";
cat $1 | sed 's/https:\/\//Media\//' > local$1
