#!/bin/sh

./build.sh $1

echo '--------'

node debug_vm.js ins.json
