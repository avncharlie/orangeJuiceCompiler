#!/bin/sh

echo "AST generating ..."

if [ $# -eq 0 ]; then
    node generate_ast/index.js index.js ast
else
    node generate_ast/index.js $1 ast
fi

echo "Bytecode generating ..."
python3 compiler.py ast out.ins silent

echo "Bytecode in ./out.ins"
