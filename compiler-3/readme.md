🧮 Task 1 — Lexical Analysis (phase1_lexer.l)

flex -DSTANDALONE phase1_lexer.l
gcc lex.yy.c -o lexer -lfl
./lexer input/test_input.c 

📘 Task 2 — Symbol Table Creation (phase2_symbol_table.py)

python3 phase2_symbol_table.py input/test_input.c > symbols.txt




phase 3 

bison -d phase3_parser.y
flex phase1_lexer.l
gcc phase3_parser.tab.c lex.yy.c -o parser -lfl
./parser input/test_input.c
