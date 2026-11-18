%{
#include <iostream>
#include <cstdlib>
#include <cmath>

using namespace std;

int yylex();
void yyerror(const char *message);
%}

%define parse.error verbose

%union {
    double value;
}

%token <value> NUMBER
%type <value> expression

%left '+' '-'
%left '*' '/'
%right '^'
%precedence UMINUS

%%

input:
      expression {
          cout << "Valid expression!" << endl;
          cout << "Result: " << $1 << endl;
      }
    ;

expression:
      NUMBER                    { $$ = $1; }
    | expression '+' expression { $$ = $1 + $3; }
    | expression '-' expression { $$ = $1 - $3; }
    | expression '*' expression { $$ = $1 * $3; }
    | expression '/' expression {
          if ($3 == 0) {
              cout << "Division by zero is not allowed." << endl;
              YYERROR;
          }
          $$ = $1 / $3;
      }
    | expression '^' expression { $$ = pow($1, $3); }
    | '-' expression %prec UMINUS { $$ = -$2; }
    | '(' expression ')'        { $$ = $2; }
    ;

%%

void yyerror(const char *message) {
    cout << "Syntax error: " << message << endl;
}

int main() {
    cout << "Input: ";
    if (yyparse() == 0) {
        return 0;
    }
    return 1;
}
