#!/bin/sh
if [ $# -eq 0 ]; then
    node debug_vm.js out.ins
else
    node debug_vm.js $1
fi

