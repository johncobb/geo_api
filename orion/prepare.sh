#!/bin/bash

shopt -s extglob dotglob
cd $1
cp -R !(build|deploy|orion|public-ci) /test

mkdir /publish-ci


