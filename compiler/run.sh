#!/bin/bash
echo "=== Running Mini Compiler ==="

# === Cleanup old files ===
rm -f parser/parser.tab.* lex.yy.c parser/parser

# === Generate parser first (creates parser.tab.h) ===
bison -d parser/parser.y -o parser/parser.tab.c

# === Then generate lexer (needs parser.tab.h) ===
lex lexer/lexer.l

# === Compile both together ===
gcc parser/parser.tab.c lex.yy.c -o parser/parser -ll

# === Run parser to create AST ===
./parser/parser < examples/example1.src > build/ast.json

# === Python stages ===
cd python_stages
python3 semantic_analyzer.py ../build/ast.json
python3 intermediate_code.py
python3 optimizer.py
python3 codegen.py
cd ..

echo "=== Compilation Complete! ==="
