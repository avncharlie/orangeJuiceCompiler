#!/bin/sh

# usage: ./build.sh assembler index

echo "Generating AST ..."
node generate_ast/index.js $2 build/ast
echo "Compiling ..."
python3 compiler.py build/ast build/ins.json $3
echo "Assembling ..."
python3 assemblers/$1/assembler.py build/ins.json assemblers/$1/template_vm.js build/out.js

echo "Output in build/out.js"
