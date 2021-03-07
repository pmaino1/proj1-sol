import re
import sys
from collections import namedtuple
import json

"""
program                      # [ (def|expr)* ]
  : def program
  | expr program
  | #empty
  ;

def
  : 'def' id '(' formals ')' expr   # ast: DEF(id, formals, expr)
  ;

formals
  : id  ( ',' id )*   # ast: FORMALS(id*)
  | #empty            # ast: FORMALS()
  ;

expr
  : expr '?' expr ':' expr   # ast: ?:(expr, expr, expr)
  | expr '<' expr            # ast: <(expr, expr)
  | expr '<=' expr           # ast: <=(expr, expr)
  | expr '>' expr            # ast: >(expr, expr)
  | expr '>=' expr           # ast: >=(expr, expr)
  | expr '==' expr           # ast: ==(expr, expr)
  | expr '!=' expr           # ast: !=(expr, expr)
  | expr '+' expr            # ast: +(expr, expr)
  | expr '-' expr            # ast: -(expr, expr)
  | expr '*' expr            # ast: *(expr, expr)
  | expr '/' expr            # ast: /(expr, expr)
  | '-' expr                 # ast: -(expr)
  | integer                  # ast: integer
  | id                       # ast: id
  | '(' expr ')'             # ast: expr
  | id '(' actuals ')'       # ast: APP(id, actuals)
  ;

actuals
  : expr ( ',' expr )*       # ast: ACTUALS(expr*)
  | #empty                   # ast: ACTUALS()
  ;
integer
  : INT                      # ast: INT() @value: integer value
  ;

id
  : ID                       # ast: ID() @id: lexeme for ID
  ;
"""

#predefined tuple for Tokens
Token = namedtuple('Token', ['kind', 'lexeme'])


def parse(text):
    return

def scan(text):
    def next_match(text):
        m = re.compile(r'^(\s+)|(#.*)').match(text)
        if(m): return (m, None) #whitespace
        m = re.compile(r'^(def)').match(text)
        if(m): return (m, 'DEF') #def keyword
        m = re.compile(r'^(<=)|(>=)|(==)|(!=)').match(text)
        if(m): return (m, m.group()) #multi-char operators
        m = re.compile(r'^\d+').match(text)
        if(m): return (m, 'INT') #int matching
        m = re.compile(r'^\w+').match(text)
        if(m): return (m, 'ID') #id matching
        m = re.compile(r'^(\()|(\))|(\?)|(\:)|(\<)|(\>)|(\+)|(\-)|(\*)|(\/)').match(text)
        if(m): return (m, m.group()) #single-char operators
        m = re.compile(r'^.').match(text) #will match anything remaining
        print("\n\t\t!Non-standard token found and created.\n")
        if (m): return (m, m.group()) #but we shouldn't get here

    tokens = []
    while(len(text) > 0):
      (match, kind) = next_match(text) #get the matching RE and kind
      lexeme = match.group() #get the actual matching chars
      if(kind): #if it's not whitespace or a comment
        tokens.append(Token(kind, lexeme))
      text = text[len(lexeme):] #iterate through the text = the size of matching chars
    return tokens

def main():
    #implement file reading and or standard input shit
    input = "bee1 123 + 6 <= ?\ndef #this is a comment\nyeah"

    print("---\n\tInput: \n", input, "\n")
    print("Tokens produced: ",scan(input))
main()