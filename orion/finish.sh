#!/bin/bash

cd /test
shopt -s extglob dotglob
cp -R !(build|deploy|orion|publish-ci) /publish-ci


