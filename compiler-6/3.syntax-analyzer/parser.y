%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();
extern int yylineno;
extern FILE *yyin;
void yyerror(const char *s);

int syntax_error = 0;
%}

%union {
    int ival;
    float fval;
    char *str;
}

%token <str> IDENTIFIER
%token <ival> NUMBER
%token <fval> FLOAT_NUM
%token INT FLOAT CHAR VOID
%token IF ELSE WHILE FOR RETURN
%token PLUS MINUS MULTIPLY DIVIDE
%token ASSIGN EQ NE LT GT LE GE
%token LPAREN RPAREN LBRACE RBRACE SEMICOLON COMMA

%left PLUS MINUS
%left MULTIPLY DIVIDE
%right ASSIGN

%start program

%%

program:
    statement_list { 
        if (!syntax_error) {
            printf("\n=== SYNTAX ANALYSIS SUCCESSFUL ===\n");
            printf("The source code is syntactically correct!\n");
        }
    }
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    declaration_statement
    | assignment_statement
    | if_statement
    | while_statement
    | for_statement
    | return_statement
    | expression_statement
    | compound_statement
    ;

declaration_statement:
    type IDENTIFIER SEMICOLON { 
        printf("Declaration: %s %s\n", $<str>1, $2); 
        free($2);
    }
    | type IDENTIFIER ASSIGN expression SEMICOLON {
        printf("Declaration with initialization: %s %s\n", $<str>1, $2);
        free($2);
    }
    ;

type:
    INT { $<str>$ = "int"; }
    | FLOAT { $<str>$ = "float"; }
    | CHAR { $<str>$ = "char"; }
    | VOID { $<str>$ = "void"; }
    ;

assignment_statement:
    IDENTIFIER ASSIGN expression SEMICOLON {
        printf("Assignment: %s = expression\n", $1);
        free($1);
    }
    ;

if_statement:
    IF LPAREN expression RPAREN statement {
        printf("If statement\n");
    }
    | IF LPAREN expression RPAREN statement ELSE statement {
        printf("If-Else statement\n");
    }
    ;

while_statement:
    WHILE LPAREN expression RPAREN statement {
        printf("While loop\n");
    }
    ;

for_statement:
    FOR LPAREN assignment_statement expression SEMICOLON IDENTIFIER ASSIGN expression RPAREN statement {
        printf("For loop\n");
        free($6);
    }
    ;

return_statement:
    RETURN expression SEMICOLON {
        printf("Return statement\n");
    }
    | RETURN SEMICOLON {
        printf("Return statement (void)\n");
    }
    ;

expression_statement:
    expression SEMICOLON
    ;

compound_statement:
    LBRACE statement_list RBRACE {
        printf("Compound statement (block)\n");
    }
    | LBRACE RBRACE {
        printf("Empty compound statement\n");
    }
    | LBRACE statement_list error {
        yyerror("Missing closing brace '}'");
        YYABORT;
    }
    | LBRACE error {
        yyerror("Missing closing brace '}'");
        YYABORT;
    }
    ;

expression:
    term
    | expression PLUS term { printf("Addition operation\n"); }
    | expression MINUS term { printf("Subtraction operation\n"); }
    | expression MULTIPLY term { printf("Multiplication operation\n"); }
    | expression DIVIDE term { printf("Division operation\n"); }
    | expression EQ term { printf("Equality comparison\n"); }
    | expression NE term { printf("Not equal comparison\n"); }
    | expression LT term { printf("Less than comparison\n"); }
    | expression GT term { printf("Greater than comparison\n"); }
    | expression LE term { printf("Less or equal comparison\n"); }
    | expression GE term { printf("Greater or equal comparison\n"); }
    ;

term:
    IDENTIFIER { 
        printf("Variable: %s\n", $1);
        free($1);
    }
    | NUMBER { printf("Number: %d\n", $1); }
    | FLOAT_NUM { printf("Float: %f\n", $1); }
    | LPAREN expression RPAREN
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Syntax error at line %d: %s\n", yylineno, s);
    syntax_error = 1;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <source_file>\n", argv[0]);
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (!input) {
        fprintf(stderr, "Error: Cannot open file %s\n", argv[1]);
        return 1;
    }

    printf("=== STARTING SYNTAX ANALYSIS ===\n");
    printf("Analyzing file: %s\n\n", argv[1]);

    yyin = input;
    yyparse();
    fclose(input);

    return syntax_error;
}