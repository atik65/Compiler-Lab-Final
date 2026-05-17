%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
%}

%token ID NUM ASSIGN OP SEMI UNKNOWN

%%
program:
      program statement
    | /* empty */
    ;

statement:
      ID ASSIGN expression SEMI   { printf("{\"type\": \"assign\", \"id\": \"%s\"}\n", yytext); }
    ;

expression:
      NUM
    | ID
    | expression OP expression
    ;
%%
int main(void) {
    return yyparse();
}
