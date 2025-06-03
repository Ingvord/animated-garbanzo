#!/bin/sh

mongoimport --host localhost --db dacat --collection Dataset --file Dataset.json --jsonArray
