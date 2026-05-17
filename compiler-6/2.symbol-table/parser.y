%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
void yyerror(const char *s);
extern FILE *yyin;
int line_no = 1;

char current_type[20] = "";
int mem_address = 1000;

typedef struct SymbolEntry {
    char token[100];
    char data_type[20];
    char token_type[20];
    char token_value[100];
    int line;
    char dimension[20];
    char address[20];
    struct SymbolEntry *next;
} SymbolEntry;

SymbolEntry *symbol_table = NULL;

void insert_symbol(char *token, char *data_type, char *token_type, char *token_value, int line, char *dimension, char *address);
void print_symbol_table();
SymbolEntry* lookup_symbol(char *token);
%}

%union {
    char *str;
    int num;
}

%token <str> IDENTIFIER INT_CONST FLOAT_CONST STRING_CONST CHAR_CONST
%token <str> INT FLOAT_TYPE CHAR_TYPE DOUBLE VOID
%token IF ELSE WHILE FOR RETURN PRINTF SCANF
%token PLUS MINUS MULT DIV ASSIGN
%token EQ NE LT GT LE GE AND OR NOT
%token LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET SEMICOLON COMMA

%type <str> type

%start program

%%

program:
    external_declaration
    | program external_declaration
    ;

external_declaration:
    function_definition
    | declaration
    ;

function_definition:
    type IDENTIFIER LPAREN RPAREN compound_statement {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol($2, $1, "FUNCTION", "-", line_no, "0", addr);
    }
    | type IDENTIFIER LPAREN parameter_list RPAREN compound_statement {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol($2, $1, "FUNCTION", "-", line_no, "0", addr);
    }
    ;

parameter_list:
    type IDENTIFIER {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol($2, $1, "PARAMETER", "-", line_no, "0", addr);
    }
    | parameter_list COMMA type IDENTIFIER {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol($4, $3, "PARAMETER", "-", line_no, "0", addr);
    }
    ;

compound_statement:
    LBRACE RBRACE
    | LBRACE statement_list RBRACE
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    declaration
    | assignment
    | if_statement
    | loop_statement
    | function_call
    | return_statement
    | compound_statement
    ;

declaration:
    type IDENTIFIER SEMICOLON {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol($2, $1, "IDENTIFIER", "-", line_no, "0", addr);
        strcpy(current_type, $1);
    }
    | type IDENTIFIER ASSIGN expression SEMICOLON {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol($2, $1, "IDENTIFIER", "-", line_no, "0", addr);
        strcpy(current_type, $1);
    }
    | type IDENTIFIER LBRACKET INT_CONST RBRACKET SEMICOLON {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += (atoi($4) * 4);
        insert_symbol($2, $1, "ARRAY", "-", line_no, $4, addr);
    }
    ;

type:
    INT { $$ = strdup("int"); }
    | FLOAT_TYPE { $$ = strdup("float"); }
    | CHAR_TYPE { $$ = strdup("char"); }
    | DOUBLE { $$ = strdup("double"); }
    | VOID { $$ = strdup("void"); }
    ;

assignment:
    IDENTIFIER ASSIGN expression SEMICOLON {
        SymbolEntry *entry = lookup_symbol($1);
        if (!entry) {
            char addr[20];
            sprintf(addr, "%d", mem_address);
            mem_address += 4;
            insert_symbol($1, "unknown", "IDENTIFIER", "-", line_no, "0", addr);
        }
    }
    | IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression SEMICOLON
    ;

expression:
    term
    | expression PLUS term
    | expression MINUS term
    ;

term:
    factor
    | term MULT factor
    | term DIV factor
    ;

factor:
    IDENTIFIER {
        SymbolEntry *entry = lookup_symbol($1);
        if (!entry) {
            char addr[20];
            sprintf(addr, "%d", mem_address);
            mem_address += 4;
            insert_symbol($1, "unknown", "IDENTIFIER", "-", line_no, "0", addr);
        }
    }
    | INT_CONST {
        insert_symbol($1, "int", "CONSTANT", $1, line_no, "0", "-");
    }
    | FLOAT_CONST {
        insert_symbol($1, "float", "CONSTANT", $1, line_no, "0", "-");
    }
    | STRING_CONST {
        insert_symbol($1, "string", "CONSTANT", $1, line_no, "0", "-");
    }
    | CHAR_CONST {
        insert_symbol($1, "char", "CONSTANT", $1, line_no, "0", "-");
    }
    | LPAREN expression RPAREN
    ;

if_statement:
    IF LPAREN condition RPAREN statement
    | IF LPAREN condition RPAREN statement ELSE statement
    ;

loop_statement:
    WHILE LPAREN condition RPAREN statement
    | FOR LPAREN assignment condition SEMICOLON assignment RPAREN statement
    | FOR LPAREN declaration condition SEMICOLON assignment RPAREN statement
    ;

condition:
    expression relational_op expression
    | condition AND condition
    | condition OR condition
    | NOT condition
    | LPAREN condition RPAREN
    ;

relational_op:
    EQ | NE | LT | GT | LE | GE
    ;

function_call:
    IDENTIFIER LPAREN argument_list RPAREN SEMICOLON
    | PRINTF LPAREN argument_list RPAREN SEMICOLON
    | SCANF LPAREN argument_list RPAREN SEMICOLON
    ;

argument_list:
    /* empty */
    | expression
    | argument_list COMMA expression
    ;

return_statement:
    RETURN expression SEMICOLON
    | RETURN SEMICOLON
    ;

%%

void insert_symbol(char *token, char *data_type, char *token_type, char *token_value, int line, char *dimension, char *address) {
    if (strcmp(token_type, "IDENTIFIER") == 0 || strcmp(token_type, "ARRAY") == 0 || strcmp(token_type, "FUNCTION") == 0) {
        SymbolEntry *curr = symbol_table;
        while (curr != NULL) {
            if (strcmp(curr->token, token) == 0 && 
                (strcmp(curr->token_type, "IDENTIFIER") == 0 || 
                 strcmp(curr->token_type, "ARRAY") == 0 || 
                 strcmp(curr->token_type, "FUNCTION") == 0)) {
                return;
            }
            curr = curr->next;
        }
    }
    
    SymbolEntry *new_entry = (SymbolEntry *)malloc(sizeof(SymbolEntry));
    strcpy(new_entry->token, token);
    strcpy(new_entry->data_type, data_type);
    strcpy(new_entry->token_type, token_type);
    strcpy(new_entry->token_value, token_value);
    new_entry->line = line;
    strcpy(new_entry->dimension, dimension);
    strcpy(new_entry->address, address);
    new_entry->next = symbol_table;
    symbol_table = new_entry;
}

SymbolEntry* lookup_symbol(char *token) {
    SymbolEntry *curr = symbol_table;
    while (curr != NULL) {
        if (strcmp(curr->token, token) == 0 && 
            (strcmp(curr->token_type, "IDENTIFIER") == 0 || 
             strcmp(curr->token_type, "ARRAY") == 0 || 
             strcmp(curr->token_type, "FUNCTION") == 0)) {
            return curr;
        }
        curr = curr->next;
    }
    return NULL;
}

void print_symbol_table() {
    printf("\n\n==================== SYMBOL TABLE ====================\n");
    printf("%-15s %-12s %-15s %-15s %-8s %-12s %-10s\n", 
           "Token", "Data Type", "Token Type", "Token Value", "Line", "Dimension", "Address");
    printf("======================================================\n");
    
    SymbolEntry *curr = symbol_table;
    while (curr != NULL) {
        printf("%-15s %-12s %-15s %-15s %-8d %-12s %-10s\n",
               curr->token, curr->data_type, curr->token_type, 
               curr->token_value, curr->line, curr->dimension, curr->address);
        curr = curr->next;
    }
    printf("======================================================\n\n");
}

void yyerror(const char *s) {
    fprintf(stderr, "Error at line %d: %s\n", line_no, s);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            printf("Could not open file %s\n", argv[1]);
            return 1;
        }
        yyin = file;
    }
    
    printf("Parsing...\n");
    yyparse();
    
    print_symbol_table();
    
    if (argc > 1) {
        fclose(yyin);
    }
    
    return 0;
}