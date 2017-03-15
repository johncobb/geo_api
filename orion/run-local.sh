#!/bin/bash

docker run 	--rm -it		\
		-p 8000:8000		\
		-e DB_URI="mysql+pymysql://dev_scanner_user:password@db.orion.cpht.io/DevScanner" \
		-e DB_ENV="mysql"	\
		cpht/scanner-api:orion

