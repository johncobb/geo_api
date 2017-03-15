#!/bin/bash

CONTAINER=$1-ci

if [[ "$(docker ps -q -f name=$CONTAINER 2> /dev/null)" != "" ]]; then
	docker kill $CONTAINER 
fi

if [[ "$(docker ps -qa -f name=$CONTAINER 2> /dev/null)" != "" ]]; then
	docker rm $CONTAINER 
fi

rm -rf ../publish-ci


