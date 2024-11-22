#!/bin/sh

for FILE_NAME in $(ls *.json)
do
    mongoimport --host localhost --db dacat --collection ${FILE_NAME%.*} --file $FILE_NAME --jsonArray
done
