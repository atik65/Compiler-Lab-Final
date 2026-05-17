# Generate the lexer
flex lexer.l

# Compile
gcc lex.yy.c -o lexer -lfl

# Run with your source file
./lexer test.c