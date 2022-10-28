#!/bin/sh

# usage: ./build.sh assembler index

echo "Generating AST ..."
node generate_ast/index.js $1 build/ast
echo "Compiling ..."
python3 compiler.py build/ast build/ins.json
echo "Graphing ..."
python3 assemblers/grapher/assembler.py build/ins.json $2
echo "Done."
