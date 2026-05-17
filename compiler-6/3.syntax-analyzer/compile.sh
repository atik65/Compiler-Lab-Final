#!/bin/bash

echo "=== Building Mini Compiler ==="

# Clean old files
rm -f lex.yy.c y.tab.c y.tab.h parser.tab.c parser.tab.h compiler

# Generate parser with header file
echo "Generating parser with Bison..."
bison -d -o parser.tab.c parser.y

if [ $? -ne 0 ]; then
    echo "Error: Bison failed"
    exit 1
fi

# Create symbolic links for compatibility
ln -sf parser.tab.c y.tab.c
ln -sf parser.tab.h y.tab.h

# Generate lexer
echo "Generating lexer with Lex..."
lex lexer.l

if [ $? -ne 0 ]; then
    echo "Error: Lex failed"
    exit 1
fi

# Compile everything
echo "Compiling..."
gcc lex.yy.c parser.tab.c -o compiler -lfl -lm

if [ $? -ne 0 ]; then
    echo "Error: Compilation failed"
    echo "Trying with alternative flex library..."
    gcc lex.yy.c parser.tab.c -o compiler
    if [ $? -ne 0 ]; then
        echo "Error: Compilation still failed"
        exit 1
    fi
fi

echo "=== Build Successful! ==="
echo ""
echo "Usage: ./compiler <source_file>"
echo ""
echo "Example:"
echo "  ./compiler test_program.c"