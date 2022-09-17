#!/bin/sh

./build.sh $1 $2
echo '--------'
node build/out.js
