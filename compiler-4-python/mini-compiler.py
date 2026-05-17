import sys
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

# ============================================================================
# TASK 1: LEXICAL ANALYSIS (TOKENIZATION)
# ============================================================================

class TokenType(Enum):
    # Keywords
    INT = "int"
    FLOAT = "float"
    CHAR = "char"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    FOR = "for"
    RETURN = "return"
    VOID = "void"
    
    # Identifiers and Literals
    IDENTIFIER = "IDENTIFIER"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    CHAR_LITERAL = "CHAR_LITERAL"
    
    # Operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    ASSIGN = "="
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    AND = "&&"
    OR = "||"
    NOT = "!"
    INCREMENT = "++"
    DECREMENT = "--"
    
    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    SEMICOLON = ";"
    COMMA = ","
    
    # Special
    EOF = "EOF"
    NEWLINE = "NEWLINE"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        self.keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'char': TokenType.CHAR,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'return': TokenType.RETURN,
            'void': TokenType.VOID,
        }
    
    def current_char(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek(self, offset=1):
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
        if self.current_char() == '/' and self.peek() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '/' and self.peek() == '*':
            self.advance()
            self.advance()
            while self.current_char():
                if self.current_char() == '*' and self.peek() == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()
    
    def read_number(self):
        start_col = self.column
        num_str = ''
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    break
                is_float = True
            num_str += self.current_char()
            self.advance()
        
        token_type = TokenType.FLOAT_LITERAL if is_float else TokenType.INTEGER_LITERAL
        return Token(token_type, num_str, self.line, start_col)
    
    def read_identifier(self):
        start_col = self.column
        id_str = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(id_str, TokenType.IDENTIFIER)
        return Token(token_type, id_str, self.line, start_col)
    
    def read_string(self):
        start_col = self.column
        self.advance()  # Skip opening quote
        string_val = ''
        
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
                    string_val += self.current_char()
                    self.advance()
            else:
                string_val += self.current_char()
                self.advance()
        
        if self.current_char() == '"':
            self.advance()
        
        return Token(TokenType.STRING_LITERAL, string_val, self.line, start_col)
    
    def read_char(self):
        start_col = self.column
        self.advance()  # Skip opening quote
        char_val = ''
        
        if self.current_char() and self.current_char() != "'":
            char_val = self.current_char()
            self.advance()
        
        if self.current_char() == "'":
            self.advance()
        
        return Token(TokenType.CHAR_LITERAL, char_val, self.line, start_col)
    
    def tokenize(self):
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.current_char() is None:
                break
            
            # Comments
            if self.current_char() == '/' and (self.peek() == '/' or self.peek() == '*'):
                self.skip_comment()
                continue
            
            start_col = self.column
            char = self.current_char()
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            # String literals
            elif char == '"':
                self.tokens.append(self.read_string())
            # Char literals
            elif char == "'":
                self.tokens.append(self.read_char())
            # Operators and delimiters
            elif char == '+':
                self.advance()
                if self.current_char() == '+':
                    self.advance()
                    self.tokens.append(Token(TokenType.INCREMENT, '++', self.line, start_col))
                else:
                    self.tokens.append(Token(TokenType.PLUS, '+', self.line, start_col))
            elif char == '-':
                self.advance()
                if self.current_char() == '-':
                    self.advance()
                    self.tokens.append(Token(TokenType.DECREMENT, '--', self.line, start_col))
                else:
                    self.tokens.append(Token(TokenType.MINUS, '-', self.line, start_col))
            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, start_col))
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, start_col))
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.MODULO, '%', self.line, start_col))
            elif char == '=':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQ, '==', self.line, start_col))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, start_col))
            elif char == '!':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NE, '!=', self.line, start_col))
                else:
                    self.tokens.append(Token(TokenType.NOT, '!', self.line, start_col))
            elif char == '<':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LE, '<=', self.line, start_col))
                else:
                    self.tokens.append(Token(TokenType.LT, '<', self.line, start_col))
            elif char == '>':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GE, '>=', self.line, start_col))
                else:
                    self.tokens.append(Token(TokenType.GT, '>', self.line, start_col))
            elif char == '&':
                self.advance()
                if self.current_char() == '&':
                    self.advance()
                    self.tokens.append(Token(TokenType.AND, '&&', self.line, start_col))
            elif char == '|':
                self.advance()
                if self.current_char() == '|':
                    self.advance()
                    self.tokens.append(Token(TokenType.OR, '||', self.line, start_col))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, start_col))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, start_col))
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, start_col))
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, start_col))
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', self.line, start_col))
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', self.line, start_col))
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, start_col))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, start_col))
            else:
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens

# ============================================================================
# TASK 2: SYMBOL TABLE CREATION
# ============================================================================

@dataclass
class SymbolInfo:
    name: str
    type: str
    scope: str
    line: int
    value: Optional[str] = None

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, SymbolInfo] = {}
        self.current_scope = "global"
    
    def add_symbol(self, name: str, sym_type: str, line: int, value: Optional[str] = None):
        key = f"{self.current_scope}:{name}"
        if key not in self.symbols:
            self.symbols[key] = SymbolInfo(name, sym_type, self.current_scope, line, value)
    
    def lookup(self, name: str):
        key = f"{self.current_scope}:{name}"
        if key in self.symbols:
            return self.symbols[key]
        key = f"global:{name}"
        return self.symbols.get(key)
    
    def print_table(self):
        print("\n" + "="*80)
        print("TASK 2: SYMBOL TABLE")
        print("="*80)
        print(f"{'Name':<15} {'Type':<15} {'Scope':<15} {'Line':<10} {'Value':<15}")
        print("-"*80)
        for symbol in self.symbols.values():
            value_str = symbol.value if symbol.value else "N/A"
            print(f"{symbol.name:<15} {symbol.type:<15} {symbol.scope:<15} {symbol.line:<10} {value_str:<15}")
        print()

# ============================================================================
# TASK 3 & 4: SYNTAX ANALYSIS AND PARSER (AST)
# ============================================================================

class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    declarations: List[ASTNode]

@dataclass
class FunctionDecl(ASTNode):
    return_type: str
    name: str
    params: List[Tuple[str, str]]
    body: 'Block'
    line: int

@dataclass
class VarDecl(ASTNode):
    var_type: str
    name: str
    init_value: Optional[ASTNode]
    line: int

@dataclass
class Block(ASTNode):
    statements: List[ASTNode]

@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_block: ASTNode
    else_block: Optional[ASTNode]
    line: int

@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode
    body: ASTNode
    line: int

@dataclass
class ForStmt(ASTNode):
    init: Optional[ASTNode]
    condition: Optional[ASTNode]
    update: Optional[ASTNode]
    body: ASTNode
    line: int

@dataclass
class ReturnStmt(ASTNode):
    value: Optional[ASTNode]
    line: int

@dataclass
class ExprStmt(ASTNode):
    expression: ASTNode

@dataclass
class Assignment(ASTNode):
    target: str
    value: ASTNode
    line: int

@dataclass
class BinaryOp(ASTNode):
    operator: str
    left: ASTNode
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class Literal(ASTNode):
    value: str
    lit_type: str

@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]

class Parser:
    def __init__(self, tokens: List[Token], symbol_table: SymbolTable):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = symbol_table
        self.syntax_errors = []
        self.syntax_ok_lines = set()
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]
    
    def peek(self, offset=1):
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
    
    def expect(self, token_type: TokenType):
        token = self.current_token()
        if token.type != token_type:
            self.syntax_errors.append(f"Line {token.line}: Expected {token_type.value}, got {token.value}")
            return False
        self.advance()
        return True
    
    def parse(self):
        try:
            return self.parse_program()
        except Exception as e:
            self.syntax_errors.append(f"Parse error: {str(e)}")
            return None
    
    def parse_program(self):
        declarations = []
        while self.current_token().type != TokenType.EOF:
            try:
                decl = self.parse_declaration()
                if decl:
                    declarations.append(decl)
            except Exception as e:
                self.syntax_errors.append(f"Line {self.current_token().line}: {str(e)}")
                while self.current_token().type not in [TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF]:
                    self.advance()
                if self.current_token().type == TokenType.SEMICOLON:
                    self.advance()
        return Program(declarations)
    
    def parse_declaration(self):
        token = self.current_token()
        line = token.line
        
        if token.type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.VOID]:
            var_type = token.value
            self.advance()
            
            if self.current_token().type != TokenType.IDENTIFIER:
                self.syntax_errors.append(f"Line {line}: Expected identifier")
                return None
            
            name = self.current_token().value
            self.advance()
            
            if self.current_token().type == TokenType.LPAREN:
                self.symbol_table.add_symbol(name, f"function:{var_type}", line)
                return self.parse_function(var_type, name, line)
            else:
                self.symbol_table.add_symbol(name, var_type, line)
                init_value = None
                
                if self.current_token().type == TokenType.ASSIGN:
                    self.advance()
                    init_value = self.parse_expression()
                
                if self.expect(TokenType.SEMICOLON):
                    self.syntax_ok_lines.add(line)
                
                return VarDecl(var_type, name, init_value, line)
        
        # Handle top-level statements (not inside functions)
        elif token.type in [TokenType.IF, TokenType.WHILE, TokenType.FOR, TokenType.RETURN]:
            return self.parse_statement()
        
        # Handle expression statements (like function calls or assignments)
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_statement()
        
        return None
    
    def parse_function(self, return_type: str, name: str, line: int):
        self.expect(TokenType.LPAREN)
        params = []
        
        old_scope = self.symbol_table.current_scope
        self.symbol_table.current_scope = name
        
        while self.current_token().type != TokenType.RPAREN:
            if self.current_token().type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR]:
                param_type = self.current_token().value
                self.advance()
                
                if self.current_token().type == TokenType.IDENTIFIER:
                    param_name = self.current_token().value
                    params.append((param_type, param_name))
                    self.symbol_table.add_symbol(param_name, param_type, self.current_token().line)
                    self.advance()
                
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
        
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        
        self.symbol_table.current_scope = old_scope
        
        if body:
            self.syntax_ok_lines.add(line)
        
        return FunctionDecl(return_type, name, params, body, line)
    
    def parse_block(self):
        if not self.expect(TokenType.LBRACE):
            return None
        
        statements = []
        while self.current_token().type != TokenType.RBRACE and self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        self.expect(TokenType.RBRACE)
        return Block(statements)
    
    def parse_statement(self):
        token = self.current_token()
        line = token.line
        
        if token.type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR]:
            var_type = token.value
            self.advance()
            
            if self.current_token().type != TokenType.IDENTIFIER:
                self.syntax_errors.append(f"Line {line}: Expected identifier")
                return None
            
            name = self.current_token().value
            self.symbol_table.add_symbol(name, var_type, line)
            self.advance()
            
            init_value = None
            if self.current_token().type == TokenType.ASSIGN:
                self.advance()
                init_value = self.parse_expression()
            
            if self.expect(TokenType.SEMICOLON):
                self.syntax_ok_lines.add(line)
            
            return VarDecl(var_type, name, init_value, line)
        
        elif token.type == TokenType.IF:
            self.advance()
            self.expect(TokenType.LPAREN)
            condition = self.parse_expression()
            self.expect(TokenType.RPAREN)
            then_block = self.parse_block() if self.current_token().type == TokenType.LBRACE else self.parse_statement()
            else_block = None
            
            if self.current_token().type == TokenType.ELSE:
                self.advance()
                else_block = self.parse_block() if self.current_token().type == TokenType.LBRACE else self.parse_statement()
            
            self.syntax_ok_lines.add(line)
            return IfStmt(condition, then_block, else_block, line)
        
        elif token.type == TokenType.WHILE:
            self.advance()
            self.expect(TokenType.LPAREN)
            condition = self.parse_expression()
            self.expect(TokenType.RPAREN)
            body = self.parse_block() if self.current_token().type == TokenType.LBRACE else self.parse_statement()
            self.syntax_ok_lines.add(line)
            return WhileStmt(condition, body, line)
        
        elif token.type == TokenType.FOR:
            self.advance()
            self.expect(TokenType.LPAREN)
            
            init = None
            if self.current_token().type != TokenType.SEMICOLON:
                init = self.parse_expression()
            self.expect(TokenType.SEMICOLON)
            
            condition = None
            if self.current_token().type != TokenType.SEMICOLON:
                condition = self.parse_expression()
            self.expect(TokenType.SEMICOLON)
            
            update = None
            if self.current_token().type != TokenType.RPAREN:
                update = self.parse_expression()
            self.expect(TokenType.RPAREN)
            
            body = self.parse_block() if self.current_token().type == TokenType.LBRACE else self.parse_statement()
            self.syntax_ok_lines.add(line)
            return ForStmt(init, condition, update, body, line)
        
        elif token.type == TokenType.RETURN:
            self.advance()
            value = None
            if self.current_token().type != TokenType.SEMICOLON:
                value = self.parse_expression()
            if self.expect(TokenType.SEMICOLON):
                self.syntax_ok_lines.add(line)
            return ReturnStmt(value, line)
        
        elif token.type == TokenType.LBRACE:
            return self.parse_block()
        
        else:
            expr = self.parse_expression()
            if self.expect(TokenType.SEMICOLON):
                self.syntax_ok_lines.add(line)
            return ExprStmt(expr) if expr else None
    
    def parse_expression(self):
        return self.parse_assignment()
    
    def parse_assignment(self):
        left = self.parse_logical_or()
        
        if self.current_token().type == TokenType.ASSIGN:
            if isinstance(left, Identifier):
                self.advance()
                right = self.parse_assignment()
                return Assignment(left.name, right, self.current_token().line)
        
        return left
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        
        while self.current_token().type == TokenType.OR:
            op = self.current_token().value
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_logical_and(self):
        left = self.parse_equality()
        
        while self.current_token().type == TokenType.AND:
            op = self.current_token().value
            self.advance()
            right = self.parse_equality()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_equality(self):
        left = self.parse_relational()
        
        while self.current_token().type in [TokenType.EQ, TokenType.NE]:
            op = self.current_token().value
            self.advance()
            right = self.parse_relational()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_relational(self):
        left = self.parse_additive()
        
        while self.current_token().type in [TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE]:
            op = self.current_token().value
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.current_token().value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_unary(self):
        if self.current_token().type in [TokenType.MINUS, TokenType.NOT, TokenType.INCREMENT, TokenType.DECREMENT]:
            op = self.current_token().value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self):
        left = self.parse_primary()
        
        while self.current_token().type in [TokenType.INCREMENT, TokenType.DECREMENT]:
            op = self.current_token().value
            self.advance()
            left = UnaryOp(op, left)
        
        return left
    
    def parse_primary(self):
        token = self.current_token()
        
        if token.type == TokenType.INTEGER_LITERAL:
            self.advance()
            return Literal(token.value, "int")
        elif token.type == TokenType.FLOAT_LITERAL:
            self.advance()
            return Literal(token.value, "float")
        elif token.type == TokenType.STRING_LITERAL:
            self.advance()
            return Literal(token.value, "string")
        elif token.type == TokenType.CHAR_LITERAL:
            self.advance()
            return Literal(token.value, "char")
        
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            
            if self.current_token().type == TokenType.LPAREN:
                self.advance()
                args = []
                
                while self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    if self.current_token().type == TokenType.COMMA:
                        self.advance()
                
                self.expect(TokenType.RPAREN)
                return FunctionCall(name, args)
            
            return Identifier(name)
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        return None
    
    def print_syntax_analysis(self):
        print("\n" + "="*80)
        print("TASK 3: SYNTAX ANALYSIS")
        print("="*80)
        
        if self.syntax_errors:
            for error in self.syntax_errors:
                print(error)
        
        all_lines = set()
        for token in self.tokens:
            if token.type != TokenType.EOF:
                all_lines.add(token.line)
        
        for line in sorted(all_lines):
            if line in self.syntax_ok_lines and not any(str(line) in err for err in self.syntax_errors):
                print(f"Line {line}: Syntax OK")
        print()

# ============================================================================
# TASK 4: PRINT AST (TREE STYLE)
# ============================================================================

class ASTPrinter:
    def __init__(self, ast: Program):
        self.ast = ast
    
    def print_tree(self):
        print("\n" + "="*80)
        print("TASK 4: ABSTRACT SYNTAX TREE (AST)")
        print("="*80)
        self.print_node(self.ast, "", True)
        print()
    
    def print_node(self, node, prefix, is_last):
        if node is None:
            return
        
        connector = "└── " if is_last else "├── "
        print(prefix + connector + self.node_name(node))
        
        children = self.get_children(node)
        child_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, child in enumerate(children):
            self.print_node(child, child_prefix, i == len(children) - 1)
    
    def node_name(self, node):
        if isinstance(node, Program):
            return "Program"
        elif isinstance(node, FunctionDecl):
            params = ", ".join([f"{t} {n}" for t, n in node.params])
            return f"FunctionDecl: {node.return_type} {node.name}({params})"
        elif isinstance(node, VarDecl):
            return f"VarDecl: {node.var_type} {node.name}"
        elif isinstance(node, Block):
            return "Block"
        elif isinstance(node, IfStmt):
            return "IfStmt"
        elif isinstance(node, WhileStmt):
            return "WhileStmt"
        elif isinstance(node, ForStmt):
            return "ForStmt"
        elif isinstance(node, ReturnStmt):
            return "ReturnStmt"
        elif isinstance(node, ExprStmt):
            return "ExprStmt"
        elif isinstance(node, Assignment):
            return f"Assignment: {node.target} ="
        elif isinstance(node, BinaryOp):
            return f"BinaryOp: {node.operator}"
        elif isinstance(node, UnaryOp):
            return f"UnaryOp: {node.operator}"
        elif isinstance(node, Identifier):
            return f"Identifier: {node.name}"
        elif isinstance(node, Literal):
            return f"Literal: {node.value} ({node.lit_type})"
        elif isinstance(node, FunctionCall):
            return f"FunctionCall: {node.name}()"
        else:
            return str(type(node).__name__)
    
    def get_children(self, node):
        children = []
        
        if isinstance(node, Program):
            children = node.declarations
        elif isinstance(node, FunctionDecl):
            children = [node.body]
        elif isinstance(node, VarDecl):
            if node.init_value:
                children = [node.init_value]
        elif isinstance(node, Block):
            children = node.statements
        elif isinstance(node, IfStmt):
            children = [node.condition, node.then_block]
            if node.else_block:
                children.append(node.else_block)
        elif isinstance(node, WhileStmt):
            children = [node.condition, node.body]
        elif isinstance(node, ForStmt):
            if node.init:
                children.append(node.init)
            if node.condition:
                children.append(node.condition)
            if node.update:
                children.append(node.update)
            children.append(node.body)
        elif isinstance(node, ReturnStmt):
            if node.value:
                children = [node.value]
        elif isinstance(node, ExprStmt):
            children = [node.expression]
        elif isinstance(node, Assignment):
            children = [node.value]
        elif isinstance(node, BinaryOp):
            children = [node.left, node.right]
        elif isinstance(node, UnaryOp):
            children = [node.operand]
        elif isinstance(node, FunctionCall):
            children = node.args
        
        return children

# ============================================================================
# TASK 5: INTERMEDIATE CODE GENERATION (THREE-ADDRESS CODE)
# ============================================================================

class IntermediateCodeGenerator:
    def __init__(self, ast: Program):
        self.ast = ast
        self.code = []
        self.temp_count = 0
        self.label_count = 0
    
    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def generate(self):
        self.visit_program(self.ast)
        return self.code
    
    def emit(self, instruction):
        self.code.append(instruction)
    
    def visit_program(self, node):
        for decl in node.declarations:
            if isinstance(decl, FunctionDecl):
                self.visit_function_decl(decl)
            elif isinstance(decl, VarDecl):
                self.visit_var_decl(decl)
    
    def visit_function_decl(self, node):
        self.emit(f"FUNC {node.name}:")
        for param_type, param_name in node.params:
            self.emit(f"  PARAM {param_name}")
        self.visit_block(node.body)
        self.emit(f"ENDFUNC {node.name}")
        self.emit("")
    
    def visit_var_decl(self, node):
        if node.init_value:
            result = self.visit_expression(node.init_value)
            self.emit(f"  {node.name} = {result}")
        else:
            self.emit(f"  DECLARE {node.var_type} {node.name}")
    
    def visit_block(self, node):
        for stmt in node.statements:
            self.visit_statement(stmt)
    
    def visit_statement(self, node):
        if isinstance(node, VarDecl):
            self.visit_var_decl(node)
        elif isinstance(node, IfStmt):
            self.visit_if_stmt(node)
        elif isinstance(node, WhileStmt):
            self.visit_while_stmt(node)
        elif isinstance(node, ForStmt):
            self.visit_for_stmt(node)
        elif isinstance(node, ReturnStmt):
            self.visit_return_stmt(node)
        elif isinstance(node, ExprStmt):
            self.visit_expression(node.expression)
        elif isinstance(node, Block):
            self.visit_block(node)
    
    def visit_if_stmt(self, node):
        condition = self.visit_expression(node.condition)
        else_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"  IFFALSE {condition} GOTO {else_label}")
        self.visit_statement(node.then_block)
        self.emit(f"  GOTO {end_label}")
        self.emit(f"{else_label}:")
        
        if node.else_block:
            self.visit_statement(node.else_block)
        
        self.emit(f"{end_label}:")
    
    def visit_while_stmt(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"{start_label}:")
        condition = self.visit_expression(node.condition)
        self.emit(f"  IFFALSE {condition} GOTO {end_label}")
        self.visit_statement(node.body)
        self.emit(f"  GOTO {start_label}")
        self.emit(f"{end_label}:")
    
    def visit_for_stmt(self, node):
        if node.init:
            self.visit_expression(node.init)
        
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"{start_label}:")
        
        if node.condition:
            condition = self.visit_expression(node.condition)
            self.emit(f"  IFFALSE {condition} GOTO {end_label}")
        
        self.visit_statement(node.body)
        
        if node.update:
            self.visit_expression(node.update)
        
        self.emit(f"  GOTO {start_label}")
        self.emit(f"{end_label}:")
    
    def visit_return_stmt(self, node):
        if node.value:
            result = self.visit_expression(node.value)
            self.emit(f"  RETURN {result}")
        else:
            self.emit(f"  RETURN")
    
    def visit_expression(self, node):
        if isinstance(node, Assignment):
            result = self.visit_expression(node.value)
            self.emit(f"  {node.target} = {result}")
            return node.target
        
        elif isinstance(node, BinaryOp):
            left = self.visit_expression(node.left)
            right = self.visit_expression(node.right)
            temp = self.new_temp()
            self.emit(f"  {temp} = {left} {node.operator} {right}")
            return temp
        
        elif isinstance(node, UnaryOp):
            operand = self.visit_expression(node.operand)
            temp = self.new_temp()
            self.emit(f"  {temp} = {node.operator}{operand}")
            return temp
        
        elif isinstance(node, Identifier):
            return node.name
        
        elif isinstance(node, Literal):
            return node.value
        
        elif isinstance(node, FunctionCall):
            for arg in node.args:
                arg_result = self.visit_expression(arg)
                self.emit(f"  PUSH {arg_result}")
            temp = self.new_temp()
            self.emit(f"  {temp} = CALL {node.name}, {len(node.args)}")
            return temp
        
        return None
    
    def print_code(self):
        print("\n" + "="*80)
        print("TASK 5: INTERMEDIATE CODE (Three-Address Code)")
        print("="*80)
        for line in self.code:
            print(line)
        print()

# ============================================================================
# TASK 6: CODE OPTIMIZATION
# ============================================================================

class CodeOptimizer:
    def __init__(self, intermediate_code):
        self.code = intermediate_code
        self.optimized_code = []
    
    def optimize(self):
        self.constant_folding()
        self.dead_code_elimination()
        self.common_subexpression_elimination()
        return self.optimized_code
    
    def constant_folding(self):
        constants = {}
        
        for line in self.code:
            line = line.strip()
            
            if '=' in line and not any(op in line for op in ['IFFALSE', 'GOTO', 'CALL', 'RETURN']):
                parts = line.split('=')
                if len(parts) == 2:
                    lhs = parts[0].strip()
                    rhs = parts[1].strip()
                    
                    if rhs.isdigit() or (rhs.startswith('-') and rhs[1:].isdigit()):
                        constants[lhs] = rhs
                    
                    elif any(op in rhs for op in ['+', '-', '*', '/', '%']):
                        for op in ['+', '-', '*', '/', '%']:
                            if op in rhs:
                                operands = rhs.split(op)
                                if len(operands) == 2:
                                    left = operands[0].strip()
                                    right = operands[1].strip()
                                    
                                    if left in constants:
                                        left = constants[left]
                                    if right in constants:
                                        right = constants[right]
                                    
                                    if left.lstrip('-').isdigit() and right.lstrip('-').isdigit():
                                        try:
                                            left_val = int(left)
                                            right_val = int(right)
                                            
                                            if op == '+':
                                                result = left_val + right_val
                                            elif op == '-':
                                                result = left_val - right_val
                                            elif op == '*':
                                                result = left_val * right_val
                                            elif op == '/' and right_val != 0:
                                                result = left_val // right_val
                                            elif op == '%' and right_val != 0:
                                                result = left_val % right_val
                                            else:
                                                result = None
                                            
                                            if result is not None:
                                                line = f"{lhs} = {result}  // Optimized: constant folding"
                                                constants[lhs] = str(result)
                                        except:
                                            pass
            
            self.optimized_code.append(line if line else "")
    
    def dead_code_elimination(self):
        used_vars = set()
        temp_code = []
        
        for line in self.optimized_code:
            if '=' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    rhs = parts[1]
                    tokens = re.findall(r'\b[a-zA-Z_]\w*\b', rhs)
                    used_vars.update(tokens)
            elif 'RETURN' in line or 'IFFALSE' in line or 'PUSH' in line:
                tokens = re.findall(r'\b[a-zA-Z_]\w*\b', line)
                used_vars.update(tokens)
        
        result = []
        for line in self.optimized_code:
            keep = True
            
            if '=' in line and not any(keyword in line for keyword in ['CALL', 'PARAM']):
                parts = line.split('=')
                if len(parts) == 2:
                    lhs = parts[0].strip()
                    if lhs.startswith('t') and lhs not in used_vars:
                        keep = False
            
            if keep:
                result.append(line)
        
        self.optimized_code = result
    
    def common_subexpression_elimination(self):
        expr_map = {}
        result = []
        
        for line in self.optimized_code:
            if '=' in line and not any(keyword in line for keyword in ['CALL', 'PARAM', 'DECLARE']):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    lhs = parts[0].strip()
                    rhs = parts[1].split('//')[0].strip()
                    
                    if rhs in expr_map and not rhs.isdigit():
                        prev_var = expr_map[rhs]
                        result.append(f"{lhs} = {prev_var}  // Optimized: CSE")
                        expr_map[rhs] = lhs
                    else:
                        result.append(line)
                        if not lhs.startswith('t') or any(var in rhs for var in expr_map.values()):
                            expr_map[rhs] = lhs
            else:
                result.append(line)
        
        self.optimized_code = result
    
    def print_code(self):
        print("\n" + "="*80)
        print("TASK 6: OPTIMIZED CODE")
        print("="*80)
        for line in self.optimized_code:
            print(line)
        print()

# ============================================================================
# TASK 7: ASSEMBLY CODE GENERATION
# ============================================================================

class AssemblyGenerator:
    def __init__(self, optimized_code):
        self.code = optimized_code
        self.assembly = []
        self.register_map = {}
        self.register_count = 0
    
    def get_register(self, var):
        if var not in self.register_map:
            self.register_map[var] = f"R{self.register_count}"
            self.register_count += 1
        return self.register_map[var]
    
    def generate(self):
        self.assembly.append("; Assembly Code Generated from Optimized Intermediate Code")
        self.assembly.append(".data")
        self.assembly.append("")
        self.assembly.append(".text")
        self.assembly.append(".globl main")
        self.assembly.append("")
        
        for line in self.code:
            line = line.strip()
            
            if not line or line.startswith('//'):
                continue
            
            if '//' in line:
                line = line.split('//')[0].strip()
            
            if line.startswith('FUNC'):
                func_name = line.split()[1].rstrip(':')
                self.assembly.append(f"{func_name}:")
                self.assembly.append("    PUSH BP")
                self.assembly.append("    MOV BP, SP")
            
            elif line.startswith('ENDFUNC'):
                self.assembly.append("    MOV SP, BP")
                self.assembly.append("    POP BP")
                self.assembly.append("    RET")
                self.assembly.append("")
            
            elif line.startswith('PARAM'):
                param = line.split()[1]
                reg = self.get_register(param)
                self.assembly.append(f"    ; Parameter {param} in {reg}")
            
            elif line.startswith('DECLARE'):
                parts = line.split()
                if len(parts) >= 3:
                    var_name = parts[2]
                    self.assembly.append(f"    ; Declare {var_name}")
            
            elif '=' in line and 'CALL' not in line:
                parts = line.split('=')
                if len(parts) == 2:
                    lhs = parts[0].strip()
                    rhs = parts[1].strip()
                    
                    lhs_reg = self.get_register(lhs)
                    
                    if rhs.lstrip('-').isdigit():
                        self.assembly.append(f"    MOV {lhs_reg}, {rhs}")
                    
                    elif rhs.replace('_', '').isalnum() and not any(op in rhs for op in ['+', '-', '*', '/', '%', '<', '>', '!', '&', '|']):
                        rhs_reg = self.get_register(rhs)
                        self.assembly.append(f"    MOV {lhs_reg}, {rhs_reg}")
                    
                    elif '+' in rhs:
                        operands = rhs.split('+')
                        if len(operands) == 2:
                            left = operands[0].strip()
                            right = operands[1].strip()
                            
                            if left.lstrip('-').isdigit():
                                self.assembly.append(f"    MOV {lhs_reg}, {left}")
                            else:
                                left_reg = self.get_register(left)
                                self.assembly.append(f"    MOV {lhs_reg}, {left_reg}")
                            
                            if right.lstrip('-').isdigit():
                                self.assembly.append(f"    ADD {lhs_reg}, {right}")
                            else:
                                right_reg = self.get_register(right)
                                self.assembly.append(f"    ADD {lhs_reg}, {right_reg}")
                    
                    elif '-' in rhs and not rhs.startswith('-'):
                        operands = rhs.split('-')
                        if len(operands) == 2:
                            left = operands[0].strip()
                            right = operands[1].strip()
                            
                            if left.lstrip('-').isdigit():
                                self.assembly.append(f"    MOV {lhs_reg}, {left}")
                            else:
                                left_reg = self.get_register(left)
                                self.assembly.append(f"    MOV {lhs_reg}, {left_reg}")
                            
                            if right.lstrip('-').isdigit():
                                self.assembly.append(f"    SUB {lhs_reg}, {right}")
                            else:
                                right_reg = self.get_register(right)
                                self.assembly.append(f"    SUB {lhs_reg}, {right_reg}")
                    
                    elif '*' in rhs:
                        operands = rhs.split('*')
                        if len(operands) == 2:
                            left = operands[0].strip()
                            right = operands[1].strip()
                            
                            if left.lstrip('-').isdigit():
                                self.assembly.append(f"    MOV {lhs_reg}, {left}")
                            else:
                                left_reg = self.get_register(left)
                                self.assembly.append(f"    MOV {lhs_reg}, {left_reg}")
                            
                            if right.lstrip('-').isdigit():
                                self.assembly.append(f"    MUL {lhs_reg}, {right}")
                            else:
                                right_reg = self.get_register(right)
                                self.assembly.append(f"    MUL {lhs_reg}, {right_reg}")
                    
                    elif '/' in rhs:
                        operands = rhs.split('/')
                        if len(operands) == 2:
                            left = operands[0].strip()
                            right = operands[1].strip()
                            
                            if left.lstrip('-').isdigit():
                                self.assembly.append(f"    MOV {lhs_reg}, {left}")
                            else:
                                left_reg = self.get_register(left)
                                self.assembly.append(f"    MOV {lhs_reg}, {left_reg}")
                            
                            if right.lstrip('-').isdigit():
                                self.assembly.append(f"    DIV {lhs_reg}, {right}")
                            else:
                                right_reg = self.get_register(right)
                                self.assembly.append(f"    DIV {lhs_reg}, {right_reg}")
                    
                    elif any(op in rhs for op in ['==', '!=', '<=', '>=', '<', '>']):
                        for op in ['==', '!=', '<=', '>=', '<', '>']:
                            if op in rhs:
                                operands = rhs.split(op)
                                if len(operands) == 2:
                                    left = operands[0].strip()
                                    right = operands[1].strip()
                                    
                                    left_reg = self.get_register(left) if not left.lstrip('-').isdigit() else left
                                    right_reg = self.get_register(right) if not right.lstrip('-').isdigit() else right
                                    
                                    if left.lstrip('-').isdigit():
                                        self.assembly.append(f"    MOV {lhs_reg}, {left}")
                                        self.assembly.append(f"    CMP {lhs_reg}, {right_reg if not right.lstrip('-').isdigit() else right}")
                                    else:
                                        self.assembly.append(f"    CMP {left_reg}, {right_reg if not right.lstrip('-').isdigit() else right}")
                                    
                                    if op == '==':
                                        self.assembly.append(f"    SETE {lhs_reg}")
                                    elif op == '!=':
                                        self.assembly.append(f"    SETNE {lhs_reg}")
                                    elif op == '<':
                                        self.assembly.append(f"    SETL {lhs_reg}")
                                    elif op == '<=':
                                        self.assembly.append(f"    SETLE {lhs_reg}")
                                    elif op == '>':
                                        self.assembly.append(f"    SETG {lhs_reg}")
                                    elif op == '>=':
                                        self.assembly.append(f"    SETGE {lhs_reg}")
                                break
            
            elif line.endswith(':') and not line.startswith('FUNC'):
                self.assembly.append(f"{line}")
            
            elif line.startswith('IFFALSE'):
                parts = line.split()
                if len(parts) >= 4:
                    condition = parts[1]
                    label = parts[3]
                    cond_reg = self.get_register(condition)
                    self.assembly.append(f"    CMP {cond_reg}, 0")
                    self.assembly.append(f"    JE {label}")
            
            elif line.startswith('GOTO'):
                label = line.split()[1]
                self.assembly.append(f"    JMP {label}")
            
            elif line.startswith('RETURN'):
                parts = line.split()
                if len(parts) > 1:
                    ret_val = parts[1]
                    if ret_val.lstrip('-').isdigit():
                        self.assembly.append(f"    MOV AX, {ret_val}")
                    else:
                        ret_reg = self.get_register(ret_val)
                        self.assembly.append(f"    MOV AX, {ret_reg}")
            
            elif 'CALL' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    lhs = parts[0].strip()
                    rhs = parts[1].strip()
                    
                    call_parts = rhs.split()
                    if len(call_parts) >= 2:
                        func_name = call_parts[1].rstrip(',')
                        self.assembly.append(f"    CALL {func_name}")
                        
                        lhs_reg = self.get_register(lhs)
                        self.assembly.append(f"    MOV {lhs_reg}, AX")
            
            elif line.startswith('PUSH'):
                arg = line.split()[1]
                if arg.lstrip('-').isdigit():
                    self.assembly.append(f"    PUSH {arg}")
                else:
                    arg_reg = self.get_register(arg)
                    self.assembly.append(f"    PUSH {arg_reg}")
        
        return self.assembly
    
    def print_code(self):
        print("\n" + "="*80)
        print("TASK 7: ASSEMBLY CODE")
        print("="*80)
        for line in self.assembly:
            print(line)
        print()

# ============================================================================
# MAIN COMPILER
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    print("="*80)
    print("MINI C COMPILER")
    print("="*80)
    print(f"Input File: {input_file}")
    print("="*80)
    
    # TASK 1: Lexical Analysis
    print("\n" + "="*80)
    print("TASK 1: LEXICAL ANALYSIS (TOKENS)")
    print("="*80)
    
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    print(f"{'Token Type':<25} {'Value':<20} {'Line':<10} {'Column':<10}")
    print("-"*80)
    for token in tokens:
        if token.type != TokenType.EOF:
            print(f"{token.type.value:<25} {token.value:<20} {token.line:<10} {token.column:<10}")
    print()
    
    # TASK 2: Symbol Table
    symbol_table = SymbolTable()
    
    # TASK 3 & 4: Syntax Analysis and Parsing
    parser = Parser(tokens, symbol_table)
    ast = parser.parse()
    
    parser.print_syntax_analysis()
    
    # Print Symbol Table
    symbol_table.print_table()
    
    # Print AST
    if ast:
        ast_printer = ASTPrinter(ast)
        ast_printer.print_tree()
        
        # TASK 5: Intermediate Code Generation
        icg = IntermediateCodeGenerator(ast)
        intermediate_code = icg.generate()
        icg.print_code()
        
        # TASK 6: Code Optimization
        optimizer = CodeOptimizer(intermediate_code)
        optimized_code = optimizer.optimize()
        optimizer.print_code()
        
        # TASK 7: Assembly Code Generation
        asm_gen = AssemblyGenerator(optimized_code)
        assembly_code = asm_gen.generate()
        asm_gen.print_code()
    else:
        print("AST generation failed due to syntax errors.")
    
    print("="*80)
    print("COMPILATION COMPLETED")
    print("="*80)

if __name__ == "__main__":
    main() 