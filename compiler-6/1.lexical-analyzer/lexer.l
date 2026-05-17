%{
#include <stdio.h>
#include <string.h>

int line_num = 1;
int token_count = 0;

void print_token(const char* token_type, const char* lexeme) {
    printf("%-15s %-20s Line: %d\n", token_type, lexeme, line_num);
    token_count++;
}
%}

/* Regular expression definitions */
DIGIT       [0-9]
LETTER      [a-zA-Z]
IDENTIFIER  {LETTER}({LETTER}|{DIGIT}|_)*
INTEGER     {DIGIT}+
FLOAT       {DIGIT}+\.{DIGIT}+
STRING      \"([^\\\"]|\\.)*\"
CHAR        \'([^\\\']|\\.)?\'

%%

    /* Keywords */
"int"       { print_token("KEYWORD", yytext); }
"float"     { print_token("KEYWORD", yytext); }
"char"      { print_token("KEYWORD", yytext); }
"double"    { print_token("KEYWORD", yytext); }
"void"      { print_token("KEYWORD", yytext); }
"if"        { print_token("KEYWORD", yytext); }
"else"      { print_token("KEYWORD", yytext); }
"while"     { print_token("KEYWORD", yytext); }
"for"       { print_token("KEYWORD", yytext); }
"do"        { print_token("KEYWORD", yytext); }
"return"    { print_token("KEYWORD", yytext); }
"break"     { print_token("KEYWORD", yytext); }
"continue"  { print_token("KEYWORD", yytext); }
"switch"    { print_token("KEYWORD", yytext); }
"case"      { print_token("KEYWORD", yytext); }
"default"   { print_token("KEYWORD", yytext); }
"struct"    { print_token("KEYWORD", yytext); }
"sizeof"    { print_token("KEYWORD", yytext); }

    /* Operators */
"+"         { print_token("OPERATOR", yytext); }
"-"         { print_token("OPERATOR", yytext); }
"*"         { print_token("OPERATOR", yytext); }
"/"         { print_token("OPERATOR", yytext); }
"%"         { print_token("OPERATOR", yytext); }
"="         { print_token("OPERATOR", yytext); }
"=="        { print_token("OPERATOR", yytext); }
"!="        { print_token("OPERATOR", yytext); }
"<"         { print_token("OPERATOR", yytext); }
">"         { print_token("OPERATOR", yytext); }
"<="        { print_token("OPERATOR", yytext); }
">="        { print_token("OPERATOR", yytext); }
"&&"        { print_token("OPERATOR", yytext); }
"||"        { print_token("OPERATOR", yytext); }
"!"         { print_token("OPERATOR", yytext); }
"++"        { print_token("OPERATOR", yytext); }
"--"        { print_token("OPERATOR", yytext); }
"+="        { print_token("OPERATOR", yytext); }
"-="        { print_token("OPERATOR", yytext); }
"*="        { print_token("OPERATOR", yytext); }
"/="        { print_token("OPERATOR", yytext); }

    /* Delimiters */
";"         { print_token("DELIMITER", yytext); }
","         { print_token("DELIMITER", yytext); }
"("         { print_token("DELIMITER", yytext); }
")"         { print_token("DELIMITER", yytext); }
"{"         { print_token("DELIMITER", yytext); }
"}"         { print_token("DELIMITER", yytext); }
"["         { print_token("DELIMITER", yytext); }
"]"         { print_token("DELIMITER", yytext); }

    /* Literals */
{INTEGER}   { print_token("INTEGER", yytext); }
{FLOAT}     { print_token("FLOAT", yytext); }
{STRING}    { print_token("STRING", yytext); }
{CHAR}      { print_token("CHAR", yytext); }

    /* Identifiers */
{IDENTIFIER} { print_token("IDENTIFIER", yytext); }

    /* Comments */
"//".*      { /* Single-line comment - ignore */ }
"/*"([^*]|\*+[^*/])*\*+"/" { 
    /* Multi-line comment - count newlines */
    for (int i = 0; i < yyleng; i++) {
        if (yytext[i] == '\n') line_num++;
    }
}

    /* Whitespace */
[ \t]+      { /* Ignore spaces and tabs */ }
\n          { line_num++; }

    /* Invalid characters */
.           { printf("LEXICAL ERROR: Unrecognized character '%s' at line %d\n", yytext, line_num); }

%%

int yywrap() {
    return 1;
}

int main(int argc, char **argv) {
    FILE *file;
    
    if (argc < 2) {
        printf("Usage: %s <source_file>\n", argv[0]);
        return 1;
    }
    
    file = fopen(argv[1], "r");
    if (!file) {
        printf("Error: Cannot open file '%s'\n", argv[1]);
        return 1;
    }
    
    printf("===== LEXICAL ANALYSIS =====\n");
    printf("%-15s %-20s %s\n", "TOKEN TYPE", "LEXEME", "LINE");
    printf("------------------------------------------------------------\n");
    
    yyin = file;
    yylex();
    
    printf("------------------------------------------------------------\n");
    printf("Total tokens: %d\n", token_count);
    printf("Total lines: %d\n", line_num);
    
    fclose(file);
    return 0;
}