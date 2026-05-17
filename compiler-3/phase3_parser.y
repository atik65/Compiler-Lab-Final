%{
#include <stdio.h>
#include <stdlib.h>
int yylex(void);
void yyerror(const char *s);
%}

/* YYSTYPE */
%union {
    int ival;
    char *sval;
}

/* Tokens */
%token INT FLOAT CHAR SEMICOLON ASSIGN PLUS MINUS MUL DIV
%token IF WHILE RETURN
%token <ival> NUMBER
%token <sval> ID
%token <sval> OPERATOR SYMBOL

/* Operator precedence */
%left PLUS MINUS
%left MUL DIV
%nonassoc OPERATOR  /* for comparisons: >, <, >=, <=, ==, != */

%%

program: statement_list ;

statement_list: statement_list statement
              | /* empty */
              ;

statement: declaration SEMICOLON
         | assignment SEMICOLON
         | IF '(' expr ')' '{' statement_list '}'
         | WHILE '(' expr ')' '{' statement_list '}'
         | RETURN expr SEMICOLON
         | expr SEMICOLON       /* function calls */
         ;

declaration: type ID
           | type ID ASSIGN expr
           ;

type: INT | FLOAT | CHAR ;

assignment: ID ASSIGN expr ;

expr: expr PLUS expr
    | expr MINUS expr
    | expr MUL expr
    | expr DIV expr
    | expr OPERATOR expr    /* comparison operators */
    | ID '(' expr ')'       /* function call */
    | ID
    | NUMBER
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Syntax error: %s\n", s);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: ./parser <input_file>\n");
        return 1;
    }
    extern FILE *yyin;
    yyin = fopen(argv[1], "r");
    if (!yyin) {
        perror("File open failed");
        return 1;
    }
    if (!yyparse())
        printf("Syntax OK!\n");
    fclose(yyin);
    return 0;
}
