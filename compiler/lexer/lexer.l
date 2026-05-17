%{
#include <stdio.h>
#include "parser.tab.h"   // share token definitions with Bison
%}

%%
[0-9]+              { yylval = atoi(yytext); return NUM; }
[a-zA-Z_][a-zA-Z0-9_]*  { return ID; }
"="                 { return ASSIGN; }
";"                 { return SEMI; }
"+"|"-"|"*"|"/"     { return OP; }
[ \t\n]             ; // ignore whitespace
.                   { return UNKNOWN; }
%%

int yywrap(void) { return 1; }
