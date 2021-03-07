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
class AST:
  def __init__(self, tag, kids, value = None, id = None):
    self.tag = tag
    self.kids = kids
    if(tag == 'INT' and value != None):
      self.value = value
    if(tag == 'ID' and value != None):
      self.id = id

def parse(text):
    #checks if the lookahead matches the kind of a current token
    def check(kind): return lookahead.kind == kind
    
    #advances the lookahead
    def match(kind):
      nonlocal lookahead
      if(lookahead.kind == kind):
        lookahead = nextToken()
      else:
        print("Expecting ", kind, "at ", lookahead.lexeme)
        sys.exit(1)

    #delivers the next token
    def nextToken():
      nonlocal index 
      if(index >= len(tokens)): #if we ran out of tokens
        return Token('EOF', '<EOF>') #end of file
      else:
        tok = tokens[index]
        index += 1
        return tok

    #TODO recursive parsing functions here: 
    #top level
    def program():
      asts = [] #list of ASTs so far
      while (not check('EOF')):
        asts.append(expr())
        
    def expr():

    #parse setup
    tokens = scan(text)
    index = 0
    lookahead = nextToken()
    value = program()
    if(not check('EOF')): #check the current token, if it's not kind EOF
      print('expecting <EOF>, got', lookahead.lexeme)
      sys.exit(1)
    return value

def scan(text):
    #determines what kind of char(s) we scan and assigns them a kind
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