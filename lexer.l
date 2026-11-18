%{
#include <cstdlib>
#include "parser.tab.h"
%}

%option noyywrap

DIGIT       [0-9]
NUMBER      ({DIGIT}+(\.{DIGIT}*)?|\.[0-9]+)

%%

{NUMBER}    {
                yylval.value = atof(yytext);
                return NUMBER;
            }

[ \t\r\n]+  ;       /* Ignore whitespace */

"+"         return '+';
"-"         return '-';
"*"         return '*';
"/"         return '/';
"^"         return '^';
"("         return '(';
")"         return ')';

.           return yytext[0];

%%
