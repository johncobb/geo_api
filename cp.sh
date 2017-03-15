#!/bin/bash

while [[ $# -gt 0 ]]
do
	key="$1"
	
	case $key in
		dbuild)
		docker build -t cpht/geo-engine:dev .
		;;

		drun)
		docker run -it --rm -p 8000:8000 -e ROUTE_PREFIX=/geo-engine cpht/geo-engine:dev
		;;

		*)
		echo "valid options: dbuild or drun"
		;;
	esac
	shift
done
