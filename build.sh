#!/bin/sh

echo "AST generating ..."

if [ $# -eq 0 ]; then
    node generate_ast/index.js index.js ast
else
    node generate_ast/index.js $1 ast
fi

echo "Bytecode generating ..."
python3 compiler.py ast ins.json $2

echo "Bytecode in ./ins.json"
