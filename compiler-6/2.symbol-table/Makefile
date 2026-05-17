CC = gcc
YACC = bison
LEX = flex

all: compiler

compiler: lex.yy.c parser.tab.c
	$(CC) -o compiler lex.yy.c parser.tab.c -lfl

lex.yy.c: lexer.l parser.tab.h
	$(LEX) lexer.l

parser.tab.c parser.tab.h: parser.y
	$(YACC) -d parser.y

clean:
	rm -f lex.yy.c parser.tab.c parser.tab.h compiler

test: compiler
	./compiler test_program.c