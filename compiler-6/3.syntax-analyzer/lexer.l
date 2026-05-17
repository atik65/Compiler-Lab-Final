%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"

extern int yylineno;
%}

%option yylineno

%%

[ \t]+                  { /* Skip whitespace */ }
\n                      { /* Skip newlines */ }

"int"                   { return INT; }
"float"                 { return FLOAT; }
"char"                  { return CHAR; }
"if"                    { return IF; }
"else"                  { return ELSE; }
"while"                 { return WHILE; }
"for"                   { return FOR; }
"return"                { return RETURN; }
"void"                  { return VOID; }

[a-zA-Z_][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+                  { yylval.ival = atoi(yytext); return NUMBER; }
[0-9]+\.[0-9]+          { yylval.fval = atof(yytext); return FLOAT_NUM; }

"+"                     { return PLUS; }
"-"                     { return MINUS; }
"*"                     { return MULTIPLY; }
"/"                     { return DIVIDE; }
"="                     { return ASSIGN; }
"=="                    { return EQ; }
"!="                    { return NE; }
"<"                     { return LT; }
">"                     { return GT; }
"<="                    { return LE; }
">="                    { return GE; }

"("                     { return LPAREN; }
")"                     { return RPAREN; }
"{"                     { return LBRACE; }
"}"                     { return RBRACE; }
";"                     { return SEMICOLON; }
","                     { return COMMA; }

.                       { printf("Unexpected character: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}