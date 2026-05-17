#!/usr/bin/env python3
"""
universal_compiler.py
A compiler that handles both simple code and function-style code
Supports int, float, and string types
With fully dynamic grammar analysis based on actual input code
"""

import re
from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass
from enum import Enum

# ==================== PHASE 1: LEXICAL ANALYSIS ====================
class TokenType(Enum):
    # Keywords
    INT = 'INT'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    CHAR = 'CHAR'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    RETURN = 'RETURN'
    VOID = 'VOID'
   
    # Operators
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULT = 'MULT'
    DIV = 'DIV'
    ASSIGN = 'ASSIGN'
    EQ = 'EQ'
    NEQ = 'NEQ'
    LT = 'LT'
    GT = 'GT'
    LTE = 'LTE'
    GTE = 'GTE'
   
    # Punctuation
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    SEMI = 'SEMI'
    COMMA = 'COMMA'
    QUOTE = 'QUOTE'
   
    # Literals
    INTEGER = 'INTEGER'
    FLOATLIT = 'FLOATLIT'
    STRINGLIT = 'STRINGLIT'
    CHARLIT = 'CHARLIT'
    IDENT = 'IDENT'
   
    EOF = 'EOF'

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    col: int
   
    def __repr__(self):
        return f"({self.type.value:8} '{self.value:5}' at {self.line:2}:{self.col:2})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
   
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            ch = self.source[self.pos]
           
            # Skip whitespace
            if ch in ' \t\r':
                self.advance()
                continue
               
            # Newline handling
            if ch == '\n':
                self.line += 1
                self.col = 1
                self.advance()
                continue
           
            # Skip comments
            if ch == '/' and self.peek() == '/':
                self.skip_line_comment()
                continue
               
            if ch == '/' and self.peek() == '*':
                self.skip_block_comment()
                continue
           
            # String literals
            if ch == '"':
                self.read_string()
                continue
               
            # Character literals
            if ch == "'":
                self.read_char()
                continue
           
            # Identifiers and keywords
            if ch.isalpha() or ch == '_':
                self.read_identifier()
                continue
               
            # Numbers
            if ch.isdigit():
                self.read_number()
                continue
               
            # Operators and punctuation
            token = self.read_operator()
            if token:
                self.tokens.append(token)
                continue
               
            raise SyntaxError(f"Unexpected character '{ch}' at {self.line}:{self.col}")
       
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.col))
        return self.tokens
   
    def advance(self, n=1):
        self.pos += n
        self.col += n
   
    def peek(self, n=1):
        if self.pos + n < len(self.source):
            return self.source[self.pos + n]
        return ''
   
    def skip_line_comment(self):
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.advance()
   
    def skip_block_comment(self):
        self.advance(2)  # Skip /*
        while self.pos < len(self.source) - 1:
            if self.source[self.pos] == '*' and self.peek() == '/':
                self.advance(2)
                return
            if self.source[self.pos] == '\n':
                self.line += 1
                self.col = 1
            self.advance()
        raise SyntaxError("Unterminated block comment")
   
    def read_string(self):
        self.advance()  # Skip opening quote
        start = self.pos
        escaped = False
       
        while self.pos < len(self.source):
            ch = self.source[self.pos]
           
            if escaped:
                escaped = False
                self.advance()
                continue
               
            if ch == '\\':
                escaped = True
                self.advance()
                continue
               
            if ch == '"':
                string_lit = self.source[start:self.pos]
                self.tokens.append(Token(TokenType.STRINGLIT, string_lit, self.line, self.col - len(string_lit)))
                self.advance()  # Skip closing quote
                return
               
            if ch == '\n':
                raise SyntaxError("Unterminated string literal")
               
            self.advance()
       
        raise SyntaxError("Unterminated string literal")
   
    def read_char(self):
        self.advance()  # Skip opening quote
        if self.pos >= len(self.source):
            raise SyntaxError("Unterminated character literal")
           
        ch = self.source[self.pos]
        if ch == '\\':  # Escape sequence
            self.advance()
            if self.pos >= len(self.source):
                raise SyntaxError("Unterminated character literal")
            escape_char = self.source[self.pos]
            # Handle common escape sequences
            if escape_char == 'n':
                ch = '\n'
            elif escape_char == 't':
                ch = '\t'
            elif escape_char == '\\':
                ch = '\\'
            elif escape_char == "'":
                ch = "'"
            else:
                ch = escape_char
       
        self.advance()
       
        if self.pos >= len(self.source) or self.source[self.pos] != "'":
            raise SyntaxError("Unterminated character literal")
           
        self.tokens.append(Token(TokenType.CHARLIT, ch, self.line, self.col - 1))
        self.advance()  # Skip closing quote
   
    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.advance()
       
        ident = self.source[start:self.pos]
       
        # Check for keywords
        keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'string': TokenType.STRING,
            'char': TokenType.CHAR,
            'void': TokenType.VOID,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'return': TokenType.RETURN
        }
       
        token_type = keywords.get(ident, TokenType.IDENT)
        self.tokens.append(Token(token_type, ident, self.line, self.col - len(ident)))
   
    def read_number(self):
        start = self.pos
        is_float = False
       
        # Read integer part
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.advance()
       
        # Check for decimal point
        if self.pos < len(self.source) and self.source[self.pos] == '.':
            is_float = True
            self.advance()
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                self.advance()
       
        number = self.source[start:self.pos]
        token_type = TokenType.FLOATLIT if is_float else TokenType.INTEGER
        self.tokens.append(Token(token_type, number, self.line, self.col - len(number)))
   
    def read_operator(self) -> Optional[Token]:
        ch = self.source[self.pos]
        two_char = self.source[self.pos:self.pos+2]
       
        operators = {
            '==': TokenType.EQ, '!=': TokenType.NEQ,
            '<=': TokenType.LTE, '>=': TokenType.GTE,
            '=': TokenType.ASSIGN, '+': TokenType.PLUS, '-': TokenType.MINUS,
            '*': TokenType.MULT, '/': TokenType.DIV, '<': TokenType.LT, '>': TokenType.GT,
            '(': TokenType.LPAREN, ')': TokenType.RPAREN, '{': TokenType.LBRACE,
            '}': TokenType.RBRACE, ';': TokenType.SEMI, ',': TokenType.COMMA
        }
       
        if two_char in operators:
            token = Token(operators[two_char], two_char, self.line, self.col)
            self.advance(2)
            return token
           
        if ch in operators:
            token = Token(operators[ch], ch, self.line, self.col)
            self.advance()
            return token
           
        return None

# ==================== GRAMMAR ANALYSIS ====================
class GrammarAnalyzer:
    def __init__(self, tokens: List[Token] = None):
        self.tokens = tokens or []
        self.used_terminals = set()
        self.used_non_terminals = set()
       
    def analyze_actual_usage(self):
        """Analyze which grammar elements are actually used in the source code"""
        if not self.tokens:
            return
           
        for token in self.tokens:
            # Map tokens to grammar terminals
            if token.type in [TokenType.INTEGER, TokenType.FLOATLIT]:
                self.used_terminals.add('number')
            elif token.type == TokenType.STRINGLIT:
                self.used_terminals.add('string')
            elif token.type == TokenType.CHARLIT:
                self.used_terminals.add('char')
            elif token.type == TokenType.IDENT:
                self.used_terminals.add('id')
            elif token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV,
                              TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT,
                              TokenType.LTE, TokenType.GTE]:
                self.used_terminals.add(token.value)
            elif token.type == TokenType.LPAREN:
                self.used_terminals.add('(')
            elif token.type == TokenType.RPAREN:
                self.used_terminals.add(')')
   
    def get_dynamic_grammar(self):
        """Generate grammar based on actual tokens used"""
        # Base grammar structure
        grammar = {
            'Expression': ['Term Expression\''],
            'Expression\'': [],
            'Term': ['Factor Term\''],
            'Term\'': [],
            'Factor': []
        }
       
        # Add productions based on actual operators found
        has_add_sub = any(t.type in [TokenType.PLUS, TokenType.MINUS] for t in self.tokens)
        has_mul_div = any(t.type in [TokenType.MULT, TokenType.DIV] for t in self.tokens)
       
        if has_add_sub:
            grammar['Expression\''].extend(['+ Term Expression\'', '- Term Expression\''])
       
        if has_mul_div:
            grammar['Term\''].extend(['* Factor Term\'', '/ Factor Term\''])
       
        # Add epsilon productions if needed
        if grammar['Expression\'']:
            grammar['Expression\''].append('ε')
        else:
            grammar['Expression\''] = ['ε']
           
        if grammar['Term\'']:
            grammar['Term\''].append('ε')
        else:
            grammar['Term\''] = ['ε']
       
        # Factor productions based on actual literals and identifiers
        factor_productions = []
        if any(t.type in [TokenType.LPAREN] for t in self.tokens):
            factor_productions.append('( Expression )')
        if any(t.type in [TokenType.INTEGER, TokenType.FLOATLIT] for t in self.tokens):
            factor_productions.append('number')
        if any(t.type in [TokenType.STRINGLIT] for t in self.tokens):
            factor_productions.append('string')
        if any(t.type in [TokenType.CHARLIT] for t in self.tokens):
            factor_productions.append('char')
        if any(t.type in [TokenType.IDENT] for t in self.tokens):
            factor_productions.append('id')
           
        grammar['Factor'] = factor_productions if factor_productions else ['number', 'id']
       
        return grammar, has_add_sub, has_mul_div
   
    def get_dynamic_first_sets(self):
        """Generate FIRST sets based on actual grammar usage"""
        dynamic_grammar, has_add_sub, has_mul_div = self.get_dynamic_grammar()
       
        first_sets = {
            'Expression': [],
            'Expression\'': [],
            'Term': [],
            'Term\'': [],
            'Factor': []
        }
       
        # Factor FIRST set
        for prod in dynamic_grammar['Factor']:
            if prod.startswith('('):
                first_sets['Factor'].append('(')
            elif prod in ['number', 'string', 'char', 'id']:
                first_sets['Factor'].append(prod)
       
        # Remove duplicates and sort
        first_sets['Factor'] = sorted(list(set(first_sets['Factor'])))
       
        # Term FIRST set (same as Factor)
        first_sets['Term'] = first_sets['Factor'].copy()
       
        # Expression FIRST set (same as Term)
        first_sets['Expression'] = first_sets['Term'].copy()
       
        # Expression' FIRST set
        for prod in dynamic_grammar['Expression\'']:
            if prod.startswith('+'):
                first_sets['Expression\''].append('+')
            elif prod.startswith('-'):
                first_sets['Expression\''].append('-')
            elif prod == 'ε':
                first_sets['Expression\''].append('ε')
       
        # Remove duplicates and sort
        first_sets['Expression\''] = sorted(list(set(first_sets['Expression\''])))
       
        # Term' FIRST set
        for prod in dynamic_grammar['Term\'']:
            if prod.startswith('*'):
                first_sets['Term\''].append('*')
            elif prod.startswith('/'):
                first_sets['Term\''].append('/')
            elif prod == 'ε':
                first_sets['Term\''].append('ε')
       
        # Remove duplicates and sort
        first_sets['Term\''] = sorted(list(set(first_sets['Term\''])))
           
        return first_sets
   
    def get_dynamic_follow_sets(self):
        """Generate FOLLOW sets based on actual grammar structure"""
        dynamic_grammar, has_add_sub, has_mul_div = self.get_dynamic_grammar()
       
        follow_sets = {
            'Expression': ['$', ')'],
            'Expression\'': ['$', ')'],
            'Term': [],
            'Term\'': [],
            'Factor': []
        }
       
        # Term FOLLOW set
        term_follow = ['$', ')']
        if has_add_sub:
            term_follow.extend(['+', '-'])
        follow_sets['Term'] = sorted(term_follow)
       
        # Term' FOLLOW set (same as Term)
        follow_sets['Term\''] = follow_sets['Term'].copy()
       
        # Factor FOLLOW set
        factor_follow = ['$', ')']
        if has_add_sub:
            factor_follow.extend(['+', '-'])
        if has_mul_div:
            factor_follow.extend(['*', '/'])
        follow_sets['Factor'] = sorted(factor_follow)
       
        return follow_sets
   
    def display_grammar_analysis(self):
        print("\n" + "="*60)
        print("GRAMMAR ANALYSIS: LEFT RECURSION ELIMINATION & FIRST/FOLLOW SETS")
        print("="*60)
       
        # Analyze actual token usage
        self.analyze_actual_usage()
        dynamic_grammar, has_add_sub, has_mul_div = self.get_dynamic_grammar()
        dynamic_first = self.get_dynamic_first_sets()
        dynamic_follow = self.get_dynamic_follow_sets()
       
        # Build original grammar based on actual usage
        original_grammar = {
            'Expression': [],
            'Term': [],
            'Factor': []
        }
       
        # Add productions to original grammar based on what's actually used
        if has_add_sub:
            original_grammar['Expression'].extend(['Expression + Term', 'Expression - Term'])
        if has_mul_div:
            original_grammar['Term'].extend(['Term * Factor', 'Term / Factor'])
       
        # Always include the base case
        original_grammar['Expression'].append('Term')
        original_grammar['Term'].append('Factor')
       
        # Factor productions
        factor_productions = []
        if any(t.type in [TokenType.LPAREN] for t in self.tokens):
            factor_productions.append('( Expression )')
        if any(t.type in [TokenType.INTEGER, TokenType.FLOATLIT] for t in self.tokens):
            factor_productions.append('number')
        if any(t.type in [TokenType.STRINGLIT] for t in self.tokens):
            factor_productions.append('string')
        if any(t.type in [TokenType.CHARLIT] for t in self.tokens):
            factor_productions.append('char')
        if any(t.type in [TokenType.IDENT] for t in self.tokens):
            factor_productions.append('id')
           
        original_grammar['Factor'] = factor_productions if factor_productions else ['number', 'id']
       
        print("\n1. ORIGINAL GRAMMAR (WITH LEFT RECURSION):")
        print("-" * 50)
        for non_terminal, productions in original_grammar.items():
            if productions:
                print(f"{non_terminal:12} → {' | '.join(productions)}")
       
        print("\n2. AFTER LEFT RECURSION ELIMINATION:")
        print("-" * 50)
        for non_terminal, productions in dynamic_grammar.items():
            if productions:
                print(f"{non_terminal:12} → {' | '.join(productions)}")
       
        print("\n3. FIRST SETS (BASED ON ACTUAL CODE):")
        print("-" * 50)
        for non_terminal, first_set in dynamic_first.items():
            if first_set:
                print(f"FIRST({non_terminal:12}) = {{{', '.join(first_set)}}}")
       
        print("\n4. FOLLOW SETS (BASED ON ACTUAL CODE):")
        print("-" * 50)
        for non_terminal, follow_set in dynamic_follow.items():
            if follow_set:
                print(f"FOLLOW({non_terminal:11}) = {{{', '.join(follow_set)}}}")
       
        print("\n5. ACTUAL TERMINALS USED IN SOURCE CODE:")
        print("-" * 50)
        used_terminals = sorted(list(self.used_terminals))
        print(f"Terminals found: {{{', '.join(used_terminals)}}}")
       
        print("\n6. EXPLANATION:")
        print("-" * 50)
        print("• Grammar analysis adapts to actual source code content")
        print("• Only productions/sets relevant to input are shown")
        print("• Left recursion eliminated using standard transformation")
        print("• ε represents empty string")
        print("• Dynamic analysis shows what the parser actually needs")
        print(f"• Detected operators: +-:{has_add_sub} */:{has_mul_div}")

# ==================== PHASE 2: SYNTAX ANALYSIS ====================
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

class Function(ASTNode):
    def __init__(self, return_type: str, name: str, body: List[ASTNode]):
        self.return_type = return_type
        self.name = name
        self.body = body

class VarDecl(ASTNode):
    def __init__(self, type_: str, name: str, init: Optional[ASTNode] = None):
        self.type = type_
        self.name = name
        self.init = init

class Assignment(ASTNode):
    def __init__(self, name: str, expr: ASTNode):
        self.name = name
        self.expr = expr

class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value: str, type_: str = 'int'):
        self.value = value
        self.type = type_

class String(ASTNode):
    def __init__(self, value: str):
        self.value = value
        self.type = 'string'

class Char(ASTNode):
    def __init__(self, value: str):
        self.value = value
        self.type = 'char'

class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name

class IfStmt(ASTNode):
    def __init__(self, cond: ASTNode, then_body: List[ASTNode], else_body: Optional[List[ASTNode]] = None):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body or []

class WhileStmt(ASTNode):
    def __init__(self, cond: ASTNode, body: List[ASTNode]):
        self.cond = cond
        self.body = body

class ReturnStmt(ASTNode):
    def __init__(self, expr: Optional[ASTNode] = None):
        self.expr = expr

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else Token(TokenType.EOF, '', 1, 1)
   
    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type} at {self.current_token.line}:{self.current_token.col}")
   
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, '', 1, 1)
   
    def parse(self) -> Program:
        statements = []
        while self.current_token.type != TokenType.EOF:
            # Check if this is a function definition
            if self.is_function_definition():
                statements.append(self.parse_function())
            else:
                statements.append(self.parse_statement())
        return Program(statements)
   
    def is_function_definition(self) -> bool:
        """Check if the current tokens indicate a function definition"""
        save_pos = self.pos
        try:
            # Look for pattern: type identifier ( ) {
            if self.current_token.type not in (TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.CHAR, TokenType.VOID):
                return False
           
            self.advance()
            if self.current_token.type != TokenType.IDENT:
                return False
           
            self.advance()
            if self.current_token.type != TokenType.LPAREN:
                return False
           
            self.advance()
            if self.current_token.type != TokenType.RPAREN:
                return False
           
            self.advance()
            if self.current_token.type != TokenType.LBRACE:
                return False
           
            return True
        finally:
            self.pos = save_pos
            self.current_token = self.tokens[self.pos]
   
    def parse_function(self) -> Function:
        return_type = self.current_token.value
        self.eat(self.current_token.type)  # int, float, string, char, or void
       
        name = self.current_token.value
        self.eat(TokenType.IDENT)
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
       
        body = []
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            body.append(self.parse_statement())
        self.eat(TokenType.RBRACE)
       
        return Function(return_type, name, body)
   
    def parse_statement(self) -> ASTNode:
        if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.CHAR):
            return self.parse_var_decl()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_stmt()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while_stmt()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return_stmt()
        elif self.current_token.type == TokenType.IDENT:
            return self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.type}")
   
    def parse_var_decl(self) -> VarDecl:
        type_token = self.current_token
        self.eat(type_token.type)
       
        name = self.current_token.value
        self.eat(TokenType.IDENT)
       
        init = None
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            init = self.parse_expression()
       
        self.eat(TokenType.SEMI)
        return VarDecl(type_token.value, name, init)
   
    def parse_assignment(self) -> Assignment:
        name = self.current_token.value
        self.eat(TokenType.IDENT)
        self.eat(TokenType.ASSIGN)
        expr = self.parse_expression()
        self.eat(TokenType.SEMI)
        return Assignment(name, expr)
   
    def parse_if_stmt(self) -> IfStmt:
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        cond = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
       
        then_body = []
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            then_body.append(self.parse_statement())
        self.eat(TokenType.RBRACE)
       
        else_body = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            else_body = []
            while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
                else_body.append(self.parse_statement())
            self.eat(TokenType.RBRACE)
       
        return IfStmt(cond, then_body, else_body)
   
    def parse_while_stmt(self) -> WhileStmt:
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        cond = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
       
        body = []
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            body.append(self.parse_statement())
        self.eat(TokenType.RBRACE)
       
        return WhileStmt(cond, body)
   
    def parse_return_stmt(self) -> ReturnStmt:
        self.eat(TokenType.RETURN)
        expr = None
        if self.current_token.type != TokenType.SEMI:
            expr = self.parse_expression()
        self.eat(TokenType.SEMI)
        return ReturnStmt(expr)
   
    def parse_expression(self) -> ASTNode:
        return self.parse_equality()
   
    def parse_equality(self) -> ASTNode:
        node = self.parse_comparison()
       
        while self.current_token.type in (TokenType.EQ, TokenType.NEQ):
            op = self.current_token.value
            self.eat(self.current_token.type)
            node = BinaryOp(node, op, self.parse_comparison())
       
        return node
   
    def parse_comparison(self) -> ASTNode:
        node = self.parse_term()
       
        while self.current_token.type in (TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.current_token.value
            self.eat(self.current_token.type)
            node = BinaryOp(node, op, self.parse_term())
       
        return node
   
    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
       
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self.eat(self.current_token.type)
            node = BinaryOp(node, op, self.parse_factor())
       
        return node
   
    def parse_factor(self) -> ASTNode:
        node = self.parse_unary()
       
        while self.current_token.type in (TokenType.MULT, TokenType.DIV):
            op = self.current_token.value
            self.eat(self.current_token.type)
            node = BinaryOp(node, op, self.parse_unary())
       
        return node
   
    def parse_unary(self) -> ASTNode:
        if self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self.eat(self.current_token.type)
            return BinaryOp(Number('0', 'int'), op, self.parse_unary())
        return self.parse_primary()
   
    def parse_primary(self) -> ASTNode:
        token = self.current_token
       
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Number(token.value, 'int')
        elif token.type == TokenType.FLOATLIT:
            self.eat(TokenType.FLOATLIT)
            return Number(token.value, 'float')
        elif token.type == TokenType.STRINGLIT:
            self.eat(TokenType.STRINGLIT)
            return String(token.value)
        elif token.type == TokenType.CHARLIT:
            self.eat(TokenType.CHARLIT)
            return Char(token.value)
        elif token.type == TokenType.IDENT:
            self.eat(TokenType.IDENT)
            return Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token.type}")

# ==================== PHASE 3: SEMANTIC ANALYSIS ====================
class SymbolTable:
    def __init__(self):
        self.scopes = [{}]
        self.current_scope = 0
   
    def enter_scope(self):
        self.scopes.append({})
        self.current_scope += 1
   
    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope -= 1
   
    def declare(self, name: str, type_: str, kind: str = "var"):
        if name in self.scopes[-1]:
            raise RuntimeError(f"Symbol '{name}' already declared in current scope")
        self.scopes[-1][name] = {'type': type_, 'kind': kind, 'scope': self.current_scope}
   
    def lookup(self, name: str) -> Optional[Dict]:
        for i in range(len(self.scopes) - 1, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None
   
    def get_all_symbols(self) -> Dict:
        all_symbols = {}
        for i, scope in enumerate(self.scopes):
            for name, info in scope.items():
                all_symbols[f"{name}@{i}"] = info  # Add scope level to key
        return all_symbols

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function = None
        self.has_main_function = False
   
    def analyze(self, node: ASTNode) -> bool:
        try:
            self.visit(node)
            return len(self.errors) == 0
        except Exception as e:
            self.errors.append(str(e))
            return False
   
    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
   
    def generic_visit(self, node: ASTNode):
        raise RuntimeError(f"No visit method for {type(node).__name__}")
   
    def visit_Program(self, node: Program):
        # Global scope
        for stmt in node.statements:
            self.visit(stmt)
       
        # Check if we have a main function for standalone code
        if not self.has_main_function and any(isinstance(stmt, ReturnStmt) for stmt in node.statements):
            # Allow return in global scope for simple programs
            pass
   
    def visit_Function(self, node: Function):
        # Declare function in current scope
        self.symbol_table.declare(node.name, node.return_type, "function")
        if node.name == "main":
            self.has_main_function = True
       
        self.current_function = node.name
       
        # Enter function scope
        self.symbol_table.enter_scope()
       
        # Process function body
        for stmt in node.body:
            self.visit(stmt)
       
        # Exit function scope
        self.symbol_table.exit_scope()
        self.current_function = None
   
    def visit_VarDecl(self, node: VarDecl):
        self.symbol_table.declare(node.name, node.type, "variable")
        if node.init:
            init_type = self.visit(node.init)
            # Basic type checking
            if init_type and init_type != node.type:
                self.errors.append(f"Type mismatch: cannot assign {init_type} to {node.type} variable '{node.name}'")
   
    def visit_Assignment(self, node: Assignment):
        var_info = self.symbol_table.lookup(node.name)
        if not var_info:
            self.errors.append(f"Undeclared variable '{node.name}'")
            return
       
        expr_type = self.visit(node.expr)
        if expr_type and var_info['type'] != expr_type:
            self.errors.append(f"Type mismatch: cannot assign {expr_type} to {var_info['type']} variable '{node.name}'")
   
    def visit_BinaryOp(self, node: BinaryOp):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
       
        # Type checking for operations
        if left_type != right_type:
            self.errors.append(f"Type mismatch in binary operation: {left_type} {node.op} {right_type}")
            return left_type or right_type or 'int'  # Return best guess
       
        # String concatenation support
        if node.op == '+' and left_type == 'string' and right_type == 'string':
            return 'string'
       
        return left_type
   
    def visit_Number(self, node: Number):
        return node.type
   
    def visit_String(self, node: String):
        return 'string'
   
    def visit_Char(self, node: Char):
        return 'char'
   
    def visit_Identifier(self, node: Identifier):
        var_info = self.symbol_table.lookup(node.name)
        if not var_info:
            self.errors.append(f"Undeclared variable '{node.name}'")
            return 'int'  # Default to int for error recovery
        return var_info['type']
   
    def visit_IfStmt(self, node: IfStmt):
        cond_type = self.visit(node.cond)
        if cond_type != 'int':  # Conditions should be integer types (or boolean, but we use int)
            self.errors.append(f"Condition expression must be integer type, got {cond_type}")
       
        # Then branch
        self.symbol_table.enter_scope()
        for stmt in node.then_body:
            self.visit(stmt)
        self.symbol_table.exit_scope()
       
        # Else branch
        if node.else_body:
            self.symbol_table.enter_scope()
            for stmt in node.else_body:
                self.visit(stmt)
            self.symbol_table.exit_scope()
   
    def visit_WhileStmt(self, node: WhileStmt):
        cond_type = self.visit(node.cond)
        if cond_type != 'int':
            self.errors.append(f"Condition expression must be integer type, got {cond_type}")
       
        self.symbol_table.enter_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.symbol_table.exit_scope()
   
    def visit_ReturnStmt(self, node: ReturnStmt):
        if not self.current_function:
            # Allow return in global scope for simple programs
            if node.expr:
                self.visit(node.expr)
            return
       
        # Get function return type
        func_info = self.symbol_table.lookup(self.current_function)
        if not func_info:
            return
       
        return_type = func_info['type']
       
        if node.expr:
            expr_type = self.visit(node.expr)
            if expr_type != return_type and return_type != 'void':
                self.errors.append(f"Return type mismatch: function returns {return_type}, got {expr_type}")
        elif return_type != 'void':
            self.errors.append(f"Non-void function '{self.current_function}' must return a value")

# ==================== PHASE 4: INTERMEDIATE CODE GENERATION ====================
@dataclass
class ThreeAddressCode:
    op: str
    arg1: Optional[str] = None
    arg2: Optional[str] = None
    result: Optional[str] = None
   
    def __str__(self):
        if self.op in ("LABEL", "GOTO", "IF_FALSE"):
            return f"{self.op} {self.result}"
        if self.arg2 is not None:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        if self.arg1 is not None:
            return f"{self.result} = {self.arg1}" if self.op == "=" else f"{self.result} = {self.op} {self.arg1}"
        return f"{self.result} = {self.op}"

class TACGenerator:
    def __init__(self):
        self.tac_code: List[ThreeAddressCode] = []
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table = SymbolTable()
        self.in_function = False
        self.current_function = None
        self.string_counter = 0
   
    def generate(self, node: ASTNode) -> List[ThreeAddressCode]:
        self.visit(node)
        return self.tac_code
   
    def new_temp(self) -> str:
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
   
    def new_label(self) -> str:
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
   
    def new_string_label(self) -> str:
        label = f"str_{self.string_counter}"
        self.string_counter += 1
        return label
   
    def emit(self, op: str, arg1: Optional[str] = None, arg2: Optional[str] = None, result: Optional[str] = None):
        self.tac_code.append(ThreeAddressCode(op, arg1, arg2, result))
   
    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
   
    def generic_visit(self, node: ASTNode):
        raise RuntimeError(f"No TAC visit method for {type(node).__name__}")
   
    def visit_Program(self, node: Program):
        # Check if we have functions or just global statements
        has_functions = any(isinstance(stmt, Function) for stmt in node.statements)
       
        if not has_functions:
            # Treat as simple program without functions
            self.emit("LABEL", None, None, "_start")
            for stmt in node.statements:
                self.visit(stmt)
            # Add default exit if no return
            if not any(isinstance(instr, ThreeAddressCode) and instr.op == "RETURN" for instr in self.tac_code):
                self.emit("=", "0", None, "exit_code")
                self.emit("RETURN", "exit_code", None, None)
        else:
            # Process functions
            for stmt in node.statements:
                self.visit(stmt)
   
    def visit_Function(self, node: Function):
        # Declare function
        self.symbol_table.declare(node.name, node.return_type, "function")
        self.in_function = True
        self.current_function = node.name
       
        # Enter function scope
        self.symbol_table.enter_scope()
       
        # Emit function label
        if node.name == "main":
            self.emit("LABEL", None, None, "_start")
        else:
            self.emit("LABEL", None, None, f"func_{node.name}")
       
        # Process function body
        for stmt in node.body:
            self.visit(stmt)
       
        # If no return at end, add default return
        if not any(isinstance(instr, ThreeAddressCode) and instr.op == "RETURN" for instr in self.tac_code[-5:]):
            if node.return_type != 'void':
                self.emit("=", "0", None, "default_return")
                self.emit("RETURN", "default_return", None, None)
            else:
                self.emit("RETURN", None, None, None)
       
        # Exit function scope
        self.symbol_table.exit_scope()
        self.in_function = False
        self.current_function = None
        return ""
   
    def visit_VarDecl(self, node: VarDecl):
        self.symbol_table.declare(node.name, node.type, "variable")
        if node.init:
            temp = self.visit(node.init)
            self.emit("=", temp, None, node.name)
        else:
            # Initialize with default value
            if node.type == 'int':
                default_value = "0"
            elif node.type == 'float':
                default_value = "0.0"
            elif node.type == 'string':
                default_value = '""'
            elif node.type == 'char':
                default_value = "0"
            else:
                default_value = "0"
            self.emit("=", default_value, None, node.name)
        return ""
   
    def visit_Assignment(self, node: Assignment):
        temp = self.visit(node.expr)
        self.emit("=", temp, None, node.name)
        return ""
   
    def visit_BinaryOp(self, node: BinaryOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.new_temp()
       
        # Handle string concatenation
        if node.op == '+' and isinstance(node.left, String) and isinstance(node.right, String):
            self.emit("STRCAT", left, right, result)
        else:
            self.emit(node.op, left, right, result)
        return result
   
    def visit_Number(self, node: Number):
        return node.value
   
    def visit_String(self, node: String):
        # Create a string label for the string literal
        string_label = self.new_string_label()
        self.emit("STRING", f'"{node.value}"', None, string_label)
        return string_label
   
    def visit_Char(self, node: Char):
        return str(ord(node.value))  # Convert char to ASCII value
   
    def visit_Identifier(self, node: Identifier):
        return node.name
   
    def visit_IfStmt(self, node: IfStmt):
        else_label = self.new_label()
        end_label = self.new_label()
       
        cond_temp = self.visit(node.cond)
        self.emit("IF_FALSE", cond_temp, None, else_label)
       
        # Then branch
        self.symbol_table.enter_scope()
        for stmt in node.then_body:
            self.visit(stmt)
        self.symbol_table.exit_scope()
       
        self.emit("GOTO", None, None, end_label)
       
        # Else branch
        self.emit("LABEL", None, None, else_label)
        if node.else_body:
            self.symbol_table.enter_scope()
            for stmt in node.else_body:
                self.visit(stmt)
            self.symbol_table.exit_scope()
       
        self.emit("LABEL", None, None, end_label)
        return ""
   
    def visit_WhileStmt(self, node: WhileStmt):
        start_label = self.new_label()
        end_label = self.new_label()
       
        self.emit("LABEL", None, None, start_label)
        cond_temp = self.visit(node.cond)
        self.emit("IF_FALSE", cond_temp, None, end_label)
       
        # Body
        self.symbol_table.enter_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.symbol_table.exit_scope()
       
        self.emit("GOTO", None, None, start_label)
        self.emit("LABEL", None, None, end_label)
        return ""
   
    def visit_ReturnStmt(self, node: ReturnStmt):
        if node.expr:
            temp = self.visit(node.expr)
            self.emit("RETURN", temp, None, None)
        else:
            self.emit("RETURN", None, None, None)
        return ""

# ==================== PHASE 5: CODE OPTIMIZATION ====================
class Optimizer:
    def optimize(self, tac_code: List[ThreeAddressCode]) -> List[ThreeAddressCode]:
        optimized = []
       
        # Constant folding
        for instr in tac_code:
            if instr.op in ('+', '-', '*', '/') and instr.arg1 and instr.arg2:
                if self.is_constant(instr.arg1) and self.is_constant(instr.arg2):
                    try:
                        result = eval(f"{instr.arg1} {instr.op} {instr.arg2}")
                        optimized.append(ThreeAddressCode("=", str(result), None, instr.result))
                        continue
                    except:
                        pass
            optimized.append(instr)
       
        return optimized
   
    def is_constant(self, val: str) -> bool:
        return val.replace('.', '').replace('-', '').isdigit()

# ==================== PHASE 6: TARGET CODE GENERATION ====================
class CodeGenerator:
    def generate(self, tac_code: List[ThreeAddressCode], symbol_table: SymbolTable) -> str:
        asm = ["section .data"]
       
        # Data section - collect all variables and strings
        all_vars = set()
        string_data = []
        symbols = symbol_table.get_all_symbols()
       
        # Add user variables
        for name, info in symbols.items():
            if info['kind'] == 'var':
                var_name = name.split('@')[0]  # Remove scope info
                all_vars.add(var_name)
       
        # Add temporaries and collect strings
        for instr in tac_code:
            if instr.result and instr.result.startswith('t'):
                all_vars.add(instr.result)
            if instr.arg1 and instr.arg1.startswith('t'):
                all_vars.add(instr.arg1)
            if instr.arg2 and instr.arg2.startswith('t'):
                all_vars.add(instr.arg2)
           
            # Handle string literals
            if instr.op == "STRING":
                string_data.append(f'{instr.result} db "{instr.arg1}", 0')
                all_vars.add(instr.result)
       
        # Also check for variables used in instructions
        for instr in tac_code:
            if instr.arg1 and not instr.arg1.startswith('t') and not self.is_constant(instr.arg1) and instr.arg1 not in ['+', '-', '*', '/'] and not instr.arg1.startswith('"'):
                all_vars.add(instr.arg1)
            if instr.arg2 and not instr.arg2.startswith('t') and not self.is_constant(instr.arg2) and instr.arg2 not in ['+', '-', '*', '/'] and not instr.arg2.startswith('"'):
                all_vars.add(instr.arg2)
            if instr.result and not instr.result.startswith('t') and not self.is_constant(instr.result) and instr.result not in ['+', '-', '*', '/'] and not instr.result.startswith('"'):
                all_vars.add(instr.result)
       
        # Remove special labels and constants
        all_vars = {v for v in all_vars if not v.startswith('L') and not v.startswith('func_') and v != '_start'}
       
        # Emit variable declarations
        for var in sorted(all_vars):
            if var.startswith('str_'):
                # Strings are already handled above
                continue
            asm.append(f"    {var} dd 0")
       
        # Add string data
        asm.extend(string_data)
       
        asm.extend(["", "section .text", "global _start", "_start:"])
       
        # Text section
        for instr in tac_code:
            if instr.op == "=":
                asm.append(f"    ; {instr.result} = {instr.arg1}")
                if self.is_constant(instr.arg1):
                    asm.append(f"    mov dword [{instr.result}], {instr.arg1}")
                else:
                    asm.append(f"    mov eax, [{instr.arg1}]")
                    asm.append(f"    mov [{instr.result}], eax")
           
            elif instr.op in ('+', '-', '*', '/'):
                asm.append(f"    ; {instr.result} = {instr.arg1} {instr.op} {instr.arg2}")
                asm.append(f"    mov eax, [{instr.arg1}]")
               
                if instr.op == '+':
                    asm.append(f"    add eax, [{instr.arg2}]")
                elif instr.op == '-':
                    asm.append(f"    sub eax, [{instr.arg2}]")
                elif instr.op == '*':
                    asm.append(f"    imul eax, [{instr.arg2}]")
                elif instr.op == '/':
                    asm.append("    cdq")
                    asm.append(f"    idiv dword [{instr.arg2}]")
               
                asm.append(f"    mov [{instr.result}], eax")
           
            elif instr.op == "STRCAT":
                asm.append(f"    ; {instr.result} = strcat({instr.arg1}, {instr.arg2})")
                asm.append(f"    ; Note: String concatenation would require runtime library")
                asm.append(f"    mov dword [{instr.result}], 0")  # Placeholder
           
            elif instr.op in ('==', '!=', '<', '>', '<=', '>='):
                asm.append(f"    ; {instr.result} = {instr.arg1} {instr.op} {instr.arg2}")
                asm.append(f"    mov eax, [{instr.arg1}]")
                asm.append(f"    cmp eax, [{instr.arg2}]")
                asm.append("    mov eax, 0")
               
                op_map = {
                    '==': 'sete', '!=': 'setne',
                    '<': 'setl', '>': 'setg',
                    '<=': 'setle', '>=': 'setge'
                }
                asm.append(f"    {op_map[instr.op]} al")
                asm.append("    movzx eax, al")
                asm.append(f"    mov [{instr.result}], eax")
           
            elif instr.op == "IF_FALSE":
                asm.append(f"    ; if false goto {instr.result}")
                asm.append(f"    cmp dword [{instr.arg1}], 0")
                asm.append(f"    je {instr.result}")
           
            elif instr.op == "GOTO":
                asm.append(f"    jmp {instr.result}")
           
            elif instr.op == "LABEL":
                asm.append(f"{instr.result}:")
           
            elif instr.op == "RETURN":
                if instr.arg1:
                    asm.append(f"    mov eax, [{instr.arg1}]")
                # For simple programs, exit after return
                asm.extend([
                    "    ; Exit program",
                    "    mov ebx, eax",  # Use return value as exit code
                    "    mov eax, 1",
                    "    int 0x80"
                ])
       
        # If no return statement found, add default exit
        if not any(instr.op == "RETURN" for instr in tac_code):
            asm.extend([
                "    ; Exit program (default)",
                "    mov eax, 1",
                "    mov ebx, 0",
                "    int 0x80"
            ])
       
        return "\n".join(asm)
   
    def is_constant(self, val: str) -> bool:
        return val.replace('.', '').replace('-', '').isdigit()

# ==================== AST DISPLAY ====================
def ast_to_string(node: ASTNode, indent: int = 0) -> str:
    pad = "  " * indent
   
    if isinstance(node, Program):
        s = pad + "Program\n"
        for stmt in node.statements:
            s += ast_to_string(stmt, indent + 1)
        return s
   
    elif isinstance(node, Function):
        s = pad + f"Function({node.return_type} {node.name})\n"
        for stmt in node.body:
            s += ast_to_string(stmt, indent + 1)
        return s
   
    elif isinstance(node, VarDecl):
        s = pad + f"VarDecl({node.type} {node.name})\n"
        if node.init:
            s += ast_to_string(node.init, indent + 1)
        return s
   
    elif isinstance(node, Assignment):
        s = pad + f"Assignment({node.name})\n"
        s += ast_to_string(node.expr, indent + 1)
        return s
   
    elif isinstance(node, BinaryOp):
        s = pad + f"BinaryOp({node.op})\n"
        s += ast_to_string(node.left, indent + 1)
        s += ast_to_string(node.right, indent + 1)
        return s
   
    elif isinstance(node, Number):
        return pad + f"Number({node.value}, {node.type})\n"
   
    elif isinstance(node, String):
        return pad + f"String('{node.value}')\n"
   
    elif isinstance(node, Char):
        return pad + f"Char('{node.value}')\n"
   
    elif isinstance(node, Identifier):
        return pad + f"Identifier({node.name})\n"
   
    elif isinstance(node, IfStmt):
        s = pad + "IfStmt\n"
        s += pad + "  Condition:\n"
        s += ast_to_string(node.cond, indent + 2)
        s += pad + "  Then:\n"
        for stmt in node.then_body:
            s += ast_to_string(stmt, indent + 2)
        if node.else_body:
            s += pad + "  Else:\n"
            for stmt in node.else_body:
                s += ast_to_string(stmt, indent + 2)
        return s
   
    elif isinstance(node, WhileStmt):
        s = pad + "WhileStmt\n"
        s += pad + "  Condition:\n"
        s += ast_to_string(node.cond, indent + 2)
        s += pad + "  Body:\n"
        for stmt in node.body:
            s += ast_to_string(stmt, indent + 2)
        return s
   
    elif isinstance(node, ReturnStmt):
        s = pad + "ReturnStmt\n"
        if node.expr:
            s += ast_to_string(node.expr, indent + 1)
        return s
   
    return pad + f"Unknown({type(node)})\n"

# ==================== MAIN COMPILER ====================
class Compiler:
    def __init__(self):
        pass  # No fixed grammar analyzer anymore
   
    def compile(self, source: str):
        print("COMPILING C++ STYLE PROGRAM:")
        print("=" * 60)
        print("SOURCE CODE:")
        print("-" * 30)
        print(source)
        print("-" * 30)
       
        try:
            # Phase 1: Lexical Analysis
            print("\n1. LEXICAL ANALYSIS (SCANNING):")
            print("-" * 50)
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            print(f"Generated {len(tokens)} tokens")
            print("First 10 tokens:")
            for i, token in enumerate(tokens[:10]):
                print(f"  {i:2d}: {token}")
            if len(tokens) > 10:
                print(f"  ... and {len(tokens) - 10} more tokens")
           
            # Create grammar analyzer with actual tokens
            grammar_analyzer = GrammarAnalyzer(tokens)
           
            # Show grammar analysis after lexical analysis
            grammar_analyzer.display_grammar_analysis()
           
            # Phase 2: Syntax Analysis
            print("\n2. SYNTAX ANALYSIS (PARSING):")
            print("-" * 50)
            parser = Parser(tokens)
            ast = parser.parse()
            print("✓ AST generated successfully")
            print("\nGenerated Abstract Syntax Tree:")
            print(ast_to_string(ast))
           
            # Phase 3: Semantic Analysis
            print("\n3. SEMANTIC ANALYSIS:")
            print("-" * 50)
            semantic_analyzer = SemanticAnalyzer()
            semantic_success = semantic_analyzer.analyze(ast)
           
            if semantic_success:
                print("✓ Semantic analysis passed")
                print("✓ Type checking completed")
                print("✓ Symbol table validated")
            else:
                print("✗ Semantic errors found:")
                for error in semantic_analyzer.errors:
                    print(f"  - {error}")
                # Continue despite semantic errors for demonstration
                print("Continuing with compilation despite semantic errors...")
           
            print(f"\nSymbol Table: {semantic_analyzer.symbol_table.get_all_symbols()}")
           
            # Phase 4: Intermediate Code Generation
            print("\n4. INTERMEDIATE CODE GENERATION:")
            print("-" * 50)
            tac_generator = TACGenerator()
            tac_code = tac_generator.generate(ast)
            print(f"Generated {len(tac_code)} Three-Address Code instructions:")
            for i, tac in enumerate(tac_code):
                print(f"  {i:2d}: {tac}")
           
            # Phase 5: Code Optimization
            print("\n5. CODE OPTIMIZATION:")
            print("-" * 50)
            optimizer = Optimizer()
            optimized_tac = optimizer.optimize(tac_code)
            print(f"Optimized to {len(optimized_tac)} TAC instructions:")
            for i, tac in enumerate(optimized_tac):
                print(f"  {i:2d}: {tac}")
           
            # Phase 6: Target Code Generation
            print("\n6. TARGET CODE GENERATION:")
            print("-" * 50)
            code_generator = CodeGenerator()
            assembly = code_generator.generate(optimized_tac, tac_generator.symbol_table)
           
            # Phase 7: Output
            print("\n7. FINAL OUTPUT:")
            print("-" * 50)
            print("Generated Assembly Code:")
            print(assembly)
           
            print("\n" + "=" * 60)
            if semantic_success:
                print("🎉 COMPILATION COMPLETED SUCCESSFULLY!")
            else:
                print("⚠️  COMPILATION COMPLETED WITH WARNINGS!")
            print("=" * 60)
           
        except Exception as e:
            print(f"\n❌ COMPILATION FAILED: {str(e)}")
            import traceback
            traceback.print_exc()

# ==================== TEST WITH DIFFERENT SOURCE CODES ====================
def main():
    compiler = Compiler()
   
    # Test with function-style code
    function_code = """
int main() {
    int a = 8;
    int b = 3;
    int result;
   
    if (a > b) {
        result = (a - b) * 2;
    } else {
        result = (a + b) / 2;
    }
   
    int i = 0;
    while (i < 3) {
        result = result + i;
        i = i + 1;
    }
   
    return result;
}
"""
   
    print("TESTING WITH FUNCTION-STYLE CODE:")
    compiler.compile(function_code)
   
    print("\n" + "="*80)
    print("TESTING WITH SIMPLE CODE:")
    print("="*80)
   
    # Test with simple code (no function)
    simple_code = """
int a = 1;
int b = 2;
int c = 3;
return a + b + c;
"""
    compiler.compile(simple_code)
   
    print("\n" + "="*80)
    print("TESTING WITH STRING SUPPORT:")
    print("="*80)
   
    # Test with string support
    string_code = """
string name = "Hello";
string world = "World";
string greeting = name + " " + world;
return 0;  // Can't return string in this simple version, but shows string support
"""
    compiler.compile(string_code)
   
    print("\n" + "="*80)
    print("TESTING WITH FLOAT SUPPORT:")
    print("="*80)
   
    # Test with float support
    float_code = """
float pi = 3.14159;
float radius = 5.0;
float area = pi * radius * radius;
return area;
"""
    compiler.compile(float_code)
   
    print("\n" + "="*80)
    print("TESTING WITH MINIMAL CODE:")
    print("="*80)
   
    # Test with minimal code
    minimal_code = """
return 42;
"""
    compiler.compile(minimal_code)

if __name__ == '__main__':
    main()