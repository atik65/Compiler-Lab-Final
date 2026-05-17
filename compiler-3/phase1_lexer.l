%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "phase3_parser.tab.h"  // Bison-generated token definitions

int line_num = 1;
extern FILE *yyin;

// yylval is defined in parser
#ifdef STANDALONE_LEXER
#define YYSTYPE int  // dummy for standalone
YYSTYPE yylval;
#endif
%}

%%

"int"       { 
#ifdef STANDALONE_LEXER
    printf("LINE %d: KEYWORD(INT)\n", line_num);
#else
    return INT;
#endif
}
"float"     { 
#ifdef STANDALONE_LEXER
    printf("LINE %d: KEYWORD(FLOAT)\n", line_num);
#else
    return FLOAT;
#endif
}
"char"      { 
#ifdef STANDALONE_LEXER
    printf("LINE %d: KEYWORD(CHAR)\n", line_num);
#else
    return CHAR;
#endif
}
"return"    { 
#ifdef STANDALONE_LEXER
    printf("LINE %d: KEYWORD(RETURN)\n", line_num);
#else
    return RETURN;
#endif
}
"if"        { 
#ifdef STANDALONE_LEXER
    printf("LINE %d: KEYWORD(IF)\n", line_num);
#else
    return IF;
#endif
}
"while"     { 
#ifdef STANDALONE_LEXER
    printf("LINE %d: KEYWORD(WHILE)\n", line_num);
#else
    return WHILE;
#endif
}

[0-9]+      {
#ifdef STANDALONE_LEXER
    printf("LINE %d: NUMBER(%s)\n", line_num, yytext);
#else
    yylval.ival = atoi(yytext);
    return NUMBER;
#endif
}

[a-zA-Z_][a-zA-Z0-9_]* {
#ifdef STANDALONE_LEXER
    printf("LINE %d: IDENTIFIER(%s)\n", line_num, yytext);
#else
    yylval.sval = strdup(yytext);
    return ID;
#endif
}

"=="|"!="|"<="|">="|"<"|">"|"="|"+"|"-"|"*"|"/" {
#ifdef STANDALONE_LEXER
    printf("LINE %d: OPERATOR(%s)\n", line_num, yytext);
#else
    yylval.sval = strdup(yytext);
    return OPERATOR;
#endif
}

"{"|"}"|"("|")"|";"|"," {
#ifdef STANDALONE_LEXER
    printf("LINE %d: SYMBOL(%s)\n", line_num, yytext);
#else
    yylval.sval = strdup(yytext);
    return SYMBOL;
#endif
}

[\n]        { line_num++; }
[ \t\r]+    { /* skip whitespace */ }

.           {
#ifdef STANDALONE_LEXER
    printf("LINE %d: UNKNOWN(%s)\n", line_num, yytext);
#else
    yylval.sval = strdup(yytext);
    return SYMBOL;
#endif
}

%%

#ifdef STANDALONE_LEXER
int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: ./lexer <input_file>\n");
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f) {
        perror("File open failed");
        return 1;
    }

    yyin = f;
    yylex();  // Run lexer
    fclose(f);
    return 0;
}
#endif
