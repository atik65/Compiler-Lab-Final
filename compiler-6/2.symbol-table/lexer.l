%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"

extern int line_no;
%}

%option noyywrap

DIGIT    [0-9]
LETTER   [a-zA-Z_]
ID       {LETTER}({LETTER}|{DIGIT})*
INTEGER  {DIGIT}+
FLOAT    {DIGIT}+"."{DIGIT}+
STRING   \"([^\\\"]|\\.)*\"
CHAR     \'([^\\\']|\\.)?\'

%%

"int"           { yylval.str = strdup(yytext); return INT; }
"float"         { yylval.str = strdup(yytext); return FLOAT_TYPE; }
"char"          { yylval.str = strdup(yytext); return CHAR_TYPE; }
"double"        { yylval.str = strdup(yytext); return DOUBLE; }
"void"          { yylval.str = strdup(yytext); return VOID; }
"if"            { return IF; }
"else"          { return ELSE; }
"while"         { return WHILE; }
"for"           { return FOR; }
"return"        { return RETURN; }
"printf"        { return PRINTF; }
"scanf"         { return SCANF; }

{ID}            { yylval.str = strdup(yytext); return IDENTIFIER; }
{INTEGER}       { yylval.str = strdup(yytext); return INT_CONST; }
{FLOAT}         { yylval.str = strdup(yytext); return FLOAT_CONST; }
{STRING}        { yylval.str = strdup(yytext); return STRING_CONST; }
{CHAR}          { yylval.str = strdup(yytext); return CHAR_CONST; }

"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return MULT; }
"/"             { return DIV; }
"="             { return ASSIGN; }
"=="            { return EQ; }
"!="            { return NE; }
"<"             { return LT; }
">"             { return GT; }
"<="            { return LE; }
">="            { return GE; }
"&&"            { return AND; }
"||"            { return OR; }
"!"             { return NOT; }

"("             { return LPAREN; }
")"             { return RPAREN; }
"{"             { return LBRACE; }
"}"             { return RBRACE; }
"["             { return LBRACKET; }
"]"             { return RBRACKET; }
";"             { return SEMICOLON; }
","             { return COMMA; }

[ \t]+          { }
\n              { line_no++; }
"//".*          { }
"/*"([^*]|\*+[^*/])*\*+"/" { 
                  int i;
                  for(i = 0; i < strlen(yytext); i++) {
                    if(yytext[i] == '\n') line_no++;
                  }
                }

.               { printf("Unexpected character: %s\n", yytext); }

%%