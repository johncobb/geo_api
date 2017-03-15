#!/bin/bash

cd ..
header="Authorization: Bearer $1"
rm -r unison-ci
git -c http.extraheader="$header" clone https://cphandheld.visualstudio.com/Project919/_git/unison-ci
