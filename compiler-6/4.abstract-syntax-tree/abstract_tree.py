import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Any

# Token Types
class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    
    # Keywords
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    VAR = "VAR"
    PRINT = "PRINT"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    
    # Special
    EOF = "EOF"
    NEWLINE = "NEWLINE"

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

# Lexer
class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'function': TokenType.FUNCTION,
            'return': TokenType.RETURN,
            'var': TokenType.VAR,
            'print': TokenType.PRINT
        }
    
    def current_char(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset=1):
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self):
        num = ''
        start_col = self.column
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num += self.current_char()
            self.advance()
        return Token(TokenType.NUMBER, float(num) if '.' in num else int(num), self.line, start_col)
    
    def read_string(self):
        start_col = self.column
        quote = self.current_char()
        self.advance()  # Skip opening quote
        string = ''
        while self.current_char() and self.current_char() != quote:
            string += self.current_char()
            self.advance()
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string, self.line, start_col)
    
    def read_identifier(self):
        start_col = self.column
        ident = ''
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(ident, TokenType.IDENTIFIER)
        return Token(token_type, ident, self.line, start_col)
    
    def tokenize(self):
        while self.pos < len(self.source):
            self.skip_whitespace()
            self.skip_comment()
            
            if self.pos >= len(self.source):
                break
            
            char = self.current_char()
            col = self.column
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings
            elif char in '"\'':
                self.tokens.append(self.read_string())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, col))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line, col))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, col))
                self.advance()
            elif char == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL, '==', self.line, col))
                self.advance()
                self.advance()
            elif char == '!':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', self.line, col))
                    self.advance()
                    self.advance()
            elif char == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, col))
                self.advance()
                self.advance()
            elif char == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, col))
                self.advance()
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS, '<', self.line, col))
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER, '>', self.line, col))
                self.advance()
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, col))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, col))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, col))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, col))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, col))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, col))
                self.advance()
            else:
                print(f"Unknown character '{char}' at line {self.line}, column {col}")
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

# AST Node Types
@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class NumberLiteral(ASTNode):
    value: float

@dataclass
class StringLiteral(ASTNode):
    value: str

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class VarDeclaration(ASTNode):
    name: str
    value: Optional[ASTNode]

@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]]

@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class FunctionDecl(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode]

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List[ASTNode]

@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode]

@dataclass
class PrintStatement(ASTNode):
    expression: ASTNode

# Parser
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset=1):
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type: TokenType):
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type} at line {token.line}")
        self.advance()
        return token
    
    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self):
        token = self.current_token()
        
        if token.type == TokenType.VAR:
            return self.parse_var_declaration()
        elif token.type == TokenType.IF:
            return self.parse_if_statement()
        elif token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif token.type == TokenType.FUNCTION:
            return self.parse_function_declaration()
        elif token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif token.type == TokenType.PRINT:
            return self.parse_print_statement()
        elif token.type == TokenType.IDENTIFIER:
            if self.peek_token().type == TokenType.ASSIGN:
                return self.parse_assignment()
            elif self.peek_token().type == TokenType.LPAREN:
                stmt = self.parse_function_call()
                self.expect(TokenType.SEMICOLON)
                return stmt
        
        # Try parsing as expression statement
        expr = self.parse_expression()
        if self.current_token().type == TokenType.SEMICOLON:
            self.advance()
        return expr
    
    def parse_var_declaration(self):
        self.expect(TokenType.VAR)
        name = self.expect(TokenType.IDENTIFIER).value
        value = None
        
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
        
        self.expect(TokenType.SEMICOLON)
        return VarDeclaration(name, value)
    
    def parse_assignment(self):
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Assignment(name, value)
    
    def parse_if_statement(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        then_branch = self.parse_block()
        else_branch = None
        
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            else_branch = self.parse_block()
        
        return IfStatement(condition, then_branch, else_branch)
    
    def parse_while_statement(self):
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return WhileStatement(condition, body)
    
    def parse_function_declaration(self):
        self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        
        params = []
        while self.current_token().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return FunctionDecl(name, params, body)
    
    def parse_return_statement(self):
        self.expect(TokenType.RETURN)
        value = None
        if self.current_token().type != TokenType.SEMICOLON:
            value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(value)
    
    def parse_print_statement(self):
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        expr = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return PrintStatement(expr)
    
    def parse_block(self):
        self.expect(TokenType.LBRACE)
        statements = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.RBRACE)
        return statements
    
    def parse_function_call(self):
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        
        arguments = []
        while self.current_token().type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        return FunctionCall(name, arguments)
    
    def parse_expression(self):
        return self.parse_comparison()
    
    def parse_comparison(self):
        left = self.parse_term()
        
        while self.current_token().type in [TokenType.EQUAL, TokenType.NOT_EQUAL, 
                                            TokenType.LESS, TokenType.GREATER,
                                            TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL]:
            op = self.current_token().value
            self.advance()
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_term(self):
        left = self.parse_factor()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.parse_factor()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_factor(self):
        left = self.parse_primary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token().value
            self.advance()
            right = self.parse_primary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_primary(self):
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberLiteral(token.value)
        
        elif token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(token.value)
        
        elif token.type == TokenType.IDENTIFIER:
            if self.peek_token().type == TokenType.LPAREN:
                return self.parse_function_call()
            self.advance()
            return Identifier(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")

# AST Visualizer
def print_ast(node, prefix="", is_last=True, is_root=True):
    """Print AST in a tree structure with proper branches"""
    
    # Determine the connector symbols
    if is_root:
        connector = ""
        extension = ""
    else:
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
    
    if isinstance(node, Program):
        print(f"{prefix}{connector}Program")
        for i, stmt in enumerate(node.statements):
            print_ast(stmt, prefix + extension, i == len(node.statements) - 1, False)
    
    elif isinstance(node, NumberLiteral):
        print(f"{prefix}{connector}NumberLiteral: {node.value}")
    
    elif isinstance(node, StringLiteral):
        print(f"{prefix}{connector}StringLiteral: '{node.value}'")
    
    elif isinstance(node, Identifier):
        print(f"{prefix}{connector}Identifier: {node.name}")
    
    elif isinstance(node, BinaryOp):
        print(f"{prefix}{connector}BinaryOp: '{node.operator}'")
        print_ast(node.left, prefix + extension, False, False)
        print_ast(node.right, prefix + extension, True, False)
    
    elif isinstance(node, VarDeclaration):
        print(f"{prefix}{connector}VarDeclaration: {node.name}")
        if node.value:
            print_ast(node.value, prefix + extension, True, False)
    
    elif isinstance(node, Assignment):
        print(f"{prefix}{connector}Assignment: {node.name}")
        print_ast(node.value, prefix + extension, True, False)
    
    elif isinstance(node, IfStatement):
        print(f"{prefix}{connector}IfStatement")
        # Condition
        print(f"{prefix}{extension}├── Condition")
        print_ast(node.condition, prefix + extension + "│   ", True, False)
        # Then branch
        has_else = node.else_branch is not None
        print(f"{prefix}{extension}{'├' if has_else else '└'}── Then")
        for i, stmt in enumerate(node.then_branch):
            print_ast(stmt, prefix + extension + ("│   " if has_else else "    "), 
                     i == len(node.then_branch) - 1, False)
        # Else branch
        if node.else_branch:
            print(f"{prefix}{extension}└── Else")
            for i, stmt in enumerate(node.else_branch):
                print_ast(stmt, prefix + extension + "    ", 
                         i == len(node.else_branch) - 1, False)
    
    elif isinstance(node, WhileStatement):
        print(f"{prefix}{connector}WhileStatement")
        print(f"{prefix}{extension}├── Condition")
        print_ast(node.condition, prefix + extension + "│   ", True, False)
        print(f"{prefix}{extension}└── Body")
        for i, stmt in enumerate(node.body):
            print_ast(stmt, prefix + extension + "    ", i == len(node.body) - 1, False)
    
    elif isinstance(node, FunctionDecl):
        print(f"{prefix}{connector}FunctionDecl: {node.name}")
        print(f"{prefix}{extension}├── Parameters: [{', '.join(node.params)}]")
        print(f"{prefix}{extension}└── Body")
        for i, stmt in enumerate(node.body):
            print_ast(stmt, prefix + extension + "    ", i == len(node.body) - 1, False)
    
    elif isinstance(node, FunctionCall):
        print(f"{prefix}{connector}FunctionCall: {node.name}")
        if node.arguments:
            print(f"{prefix}{extension}└── Arguments")
            for i, arg in enumerate(node.arguments):
                print_ast(arg, prefix + extension + "    ", i == len(node.arguments) - 1, False)
    
    elif isinstance(node, ReturnStatement):
        print(f"{prefix}{connector}ReturnStatement")
        if node.value:
            print_ast(node.value, prefix + extension, True, False)
    
    elif isinstance(node, PrintStatement):
        print(f"{prefix}{connector}PrintStatement")
        print_ast(node.expression, prefix + extension, True, False)

# Main function
def compile_source(filename):
    try:
        with open(filename, 'r') as f:
            source = f.read()
        
        print("=" * 60)
        print("SOURCE CODE:")
        print("=" * 60)
        print(source)
        print()
        
        # Lexical Analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        print("=" * 60)
        print("TOKENS:")
        print("=" * 60)
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"{token.type.value:15} | {token.value}")
        print()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        print("=" * 60)
        print("ABSTRACT SYNTAX TREE:")
        print("=" * 60)
        print_ast(ast)
        print()
        
        return ast
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        compile_source(sys.argv[1])
    else:
        # Example source code for testing
        example_source = """
var x = 10;
var y = 20;
var result = x + y * 2;

function add(a, b) {
    return a + b;
}

var sum = add(x, y);
print(sum);

if (result > 30) {
    print("Result is large");
} else {
    print("Result is small");
}

while (x < 15) {
    x = x + 1;
    print(x);
}
"""
        
        print("No source file provided. Using example code.")
        print("Usage: python compiler.py <source_file>")
        print()
        
        # Save example to file and compile
        with open('example.txt', 'w') as f:
            f.write(example_source)
        
        compile_source('example.txt')