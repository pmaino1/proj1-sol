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
    self.value = value
    self.id = id

  def __str__(self):
    map
    ret = '{"tag":"' +self.tag+ '","kids":'+ str(self.kids)
    if(self.value):
      ret = ret + ',"value":' +self.value 
    if(self.id):
      ret = ret + ',"id":"' +self.id+ '"'
    ret += '}'
    return ret
  def __repr__(self):
    return self.__str__()

def parse(tokens):
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
      return asts

    def expr():
      return add_expr()
    
    def add_expr():
      expr1 = mult_expr()
      while(check('+') or check('-')):
        tok = lookahead #will contain + or - token
        match(tok.kind)
        expr2 = mult_expr()
        kids = []
        kids.append(expr1)
        kids.append(expr2)
        expr1 = AST(tok.kind, kids)
      return expr1

    def mult_expr():
      expr1 = unaryminus_expr()
      while(check('*') or check('/')):
        tok = lookahead #will contain * or / token
        match(tok.kind)
        expr2 = unaryminus_expr()
        kids = []
        kids.append(expr1)
        kids.append(expr2)
        expr1 = AST(tok.kind, kids)
      return expr1

    def unaryminus_expr():
      tok = lookahead
      if(check('-')):
        match('-')
        kids = []
        kids.append(bottom_expr())
        return AST(tok.kind, kids)
      return bottom_expr()

    def bottom_expr():
      tok = lookahead
      if(check('INT')):
        match('INT')
        return AST(tok.kind,[],value=tok.lexeme)
      if(check('ID')):
        match('ID')
        return AST(tok.kind,[],id=tok.lexeme)
      return None
      
    

    #parse setup
    index = 0
    lookahead = nextToken()
    value = program()
    if(not check('EOF')): #check the current token, if it's not kind EOF
      print('expecting <EOF>, got ', lookahead.lexeme)
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
    input = ' \
      123\nHello\nb32\n \
      a * 123\n12 / -b\n \
      a + b*123\n12*-2 - b*4 + c/3\n'

    print("---\n\tInput: \n", input, "\n")
    tokens = scan(input)
    print("Tokens produced: ",tokens)
    print("ASTs produced: ",parse(tokens))
main()