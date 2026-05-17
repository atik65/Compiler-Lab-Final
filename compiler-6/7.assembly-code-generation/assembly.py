import re
import sys

# ============== LEXER ==============
class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, Line:{self.line})"

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.tokens = []
        
        self.keywords = {'int', 'if', 'else', 'while', 'print'}
        self.token_patterns = [
            ('NUMBER', r'\d+'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ASSIGN', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MUL', r'\*'),
            ('DIV', r'/'),
            ('LT', r'<'),
            ('GT', r'>'),
            ('LE', r'<='),
            ('GE', r'>='),
            ('EQ', r'=='),
            ('NE', r'!='),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('SEMICOLON', r';'),
            ('NEWLINE', r'\n'),
            ('WHITESPACE', r'[ \t]+'),
        ]
    
    def tokenize(self):
        while self.pos < len(self.source):
            matched = False
            
            for token_type, pattern in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                
                if match:
                    value = match.group(0)
                    
                    if token_type == 'NEWLINE':
                        self.line += 1
                    elif token_type == 'WHITESPACE':
                        pass
                    elif token_type == 'ID' and value in self.keywords:
                        self.tokens.append(Token(value.upper(), value, self.line))
                    elif token_type != 'WHITESPACE':
                        self.tokens.append(Token(token_type, value, self.line))
                    
                    self.pos = match.end()
                    matched = True
                    break
            
            if not matched:
                raise SyntaxError(f"Unexpected character '{self.source[self.pos]}' at line {self.line}")
        
        self.tokens.append(Token('EOF', None, self.line))
        return self.tokens

# ============== AST NODES ==============
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(ASTNode):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

class Assignment(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class PrintStatement(ASTNode):
    def __init__(self, expr):
        self.expr = expr

# ============== PARSER ==============
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
    
    def expect(self, token_type):
        if self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        raise SyntaxError(f"Expected {token_type} but got {self.current_token.type} at line {self.current_token.line}")
    
    def parse(self):
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def statement(self):
        if self.current_token.type == 'INT':
            return self.var_declaration()
        elif self.current_token.type == 'ID':
            return self.assignment()
        elif self.current_token.type == 'IF':
            return self.if_statement()
        elif self.current_token.type == 'WHILE':
            return self.while_statement()
        elif self.current_token.type == 'PRINT':
            return self.print_statement()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.type} at line {self.current_token.line}")
    
    def var_declaration(self):
        self.expect('INT')
        name = self.expect('ID').value
        
        if self.current_token.type == 'ASSIGN':
            self.advance()
            value = self.expression()
            self.expect('SEMICOLON')
            return VarDecl(name, value)
        
        self.expect('SEMICOLON')
        return VarDecl(name)
    
    def assignment(self):
        name = self.expect('ID').value
        self.expect('ASSIGN')
        expr = self.expression()
        self.expect('SEMICOLON')
        return Assignment(name, expr)
    
    def if_statement(self):
        self.expect('IF')
        self.expect('LPAREN')
        condition = self.expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        
        then_block = []
        while self.current_token.type != 'RBRACE':
            then_block.append(self.statement())
        self.expect('RBRACE')
        
        else_block = None
        if self.current_token.type == 'ELSE':
            self.advance()
            self.expect('LBRACE')
            else_block = []
            while self.current_token.type != 'RBRACE':
                else_block.append(self.statement())
            self.expect('RBRACE')
        
        return IfStatement(condition, then_block, else_block)
    
    def while_statement(self):
        self.expect('WHILE')
        self.expect('LPAREN')
        condition = self.expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        
        body = []
        while self.current_token.type != 'RBRACE':
            body.append(self.statement())
        self.expect('RBRACE')
        
        return WhileStatement(condition, body)
    
    def print_statement(self):
        self.expect('PRINT')
        self.expect('LPAREN')
        expr = self.expression()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        return PrintStatement(expr)
    
    def expression(self):
        return self.comparison()
    
    def comparison(self):
        left = self.term()
        
        while self.current_token.type in ('LT', 'GT', 'LE', 'GE', 'EQ', 'NE'):
            op = self.current_token.value
            self.advance()
            right = self.term()
            left = BinOp(left, op, right)
        
        return left
    
    def term(self):
        left = self.factor()
        
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.value
            self.advance()
            right = self.factor()
            left = BinOp(left, op, right)
        
        return left
    
    def factor(self):
        left = self.primary()
        
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token.value
            self.advance()
            right = self.primary()
            left = BinOp(left, op, right)
        
        return left
    
    def primary(self):
        if self.current_token.type == 'NUMBER':
            value = int(self.current_token.value)
            self.advance()
            return Number(value)
        elif self.current_token.type == 'ID':
            name = self.current_token.value
            self.advance()
            return Variable(name)
        elif self.current_token.type == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.type} at line {self.current_token.line}")

# ============== CODE GENERATOR ==============
class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0
        self.variables = {}
        self.stack_offset = 0
    
    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"
    
    def emit(self, instruction):
        self.code.append(instruction)
    
    def generate(self, ast):
        self.emit("; Generated Assembly Code")
        self.emit("section .data")
        self.emit("    fmt_int db '%d', 10, 0  ; Format string for printing")
        self.emit("")
        self.emit("section .bss")
        self.emit("")
        self.emit("section .text")
        self.emit("    global main")
        self.emit("    extern printf")
        self.emit("")
        self.emit("main:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rsp, 64          ; Allocate space for local variables")
        self.emit("")
        
        for stmt in ast.statements:
            self.generate_statement(stmt)
        
        self.emit("")
        self.emit("    xor rax, rax         ; Return 0")
        self.emit("    mov rsp, rbp")
        self.emit("    pop rbp")
        self.emit("    ret")
        
        return '\n'.join(self.code)
    
    def generate_statement(self, stmt):
        if isinstance(stmt, VarDecl):
            self.stack_offset += 8
            self.variables[stmt.name] = -self.stack_offset
            if stmt.value:
                self.generate_expression(stmt.value)
                self.emit(f"    mov [rbp{self.variables[stmt.name]}], rax  ; Store {stmt.name}")
            else:
                self.emit(f"    mov qword [rbp{self.variables[stmt.name]}], 0  ; Initialize {stmt.name} to 0")
        
        elif isinstance(stmt, Assignment):
            self.generate_expression(stmt.expr)
            if stmt.name not in self.variables:
                raise NameError(f"Variable '{stmt.name}' not declared")
            self.emit(f"    mov [rbp{self.variables[stmt.name]}], rax  ; Assign to {stmt.name}")
        
        elif isinstance(stmt, IfStatement):
            else_label = self.new_label()
            end_label = self.new_label()
            
            self.generate_expression(stmt.condition)
            self.emit("    cmp rax, 0")
            self.emit(f"    je {else_label}           ; Jump if false")
            
            for s in stmt.then_block:
                self.generate_statement(s)
            self.emit(f"    jmp {end_label}")
            
            self.emit(f"{else_label}:")
            if stmt.else_block:
                for s in stmt.else_block:
                    self.generate_statement(s)
            
            self.emit(f"{end_label}:")
        
        elif isinstance(stmt, WhileStatement):
            start_label = self.new_label()
            end_label = self.new_label()
            
            self.emit(f"{start_label}:")
            self.generate_expression(stmt.condition)
            self.emit("    cmp rax, 0")
            self.emit(f"    je {end_label}           ; Exit loop if false")
            
            for s in stmt.body:
                self.generate_statement(s)
            
            self.emit(f"    jmp {start_label}         ; Loop back")
            self.emit(f"{end_label}:")
        
        elif isinstance(stmt, PrintStatement):
            self.generate_expression(stmt.expr)
            self.emit("    mov rsi, rax          ; Value to print")
            self.emit("    lea rdi, [rel fmt_int]")
            self.emit("    xor rax, rax")
            self.emit("    call printf")
    
    def generate_expression(self, expr):
        if isinstance(expr, Number):
            self.emit(f"    mov rax, {expr.value}")
        
        elif isinstance(expr, Variable):
            if expr.name not in self.variables:
                raise NameError(f"Variable '{expr.name}' not declared")
            self.emit(f"    mov rax, [rbp{self.variables[expr.name]}]  ; Load {expr.name}")
        
        elif isinstance(expr, BinOp):
            self.generate_expression(expr.right)
            self.emit("    push rax")
            self.generate_expression(expr.left)
            self.emit("    pop rbx")
            
            if expr.op == '+':
                self.emit("    add rax, rbx")
            elif expr.op == '-':
                self.emit("    sub rax, rbx")
            elif expr.op == '*':
                self.emit("    imul rax, rbx")
            elif expr.op == '/':
                self.emit("    xor rdx, rdx")
                self.emit("    idiv rbx")
            elif expr.op == '<':
                self.emit("    cmp rax, rbx")
                self.emit("    setl al")
                self.emit("    movzx rax, al")
            elif expr.op == '>':
                self.emit("    cmp rax, rbx")
                self.emit("    setg al")
                self.emit("    movzx rax, al")
            elif expr.op == '<=':
                self.emit("    cmp rax, rbx")
                self.emit("    setle al")
                self.emit("    movzx rax, al")
            elif expr.op == '>=':
                self.emit("    cmp rax, rbx")
                self.emit("    setge al")
                self.emit("    movzx rax, al")
            elif expr.op == '==':
                self.emit("    cmp rax, rbx")
                self.emit("    sete al")
                self.emit("    movzx rax, al")
            elif expr.op == '!=':
                self.emit("    cmp rax, rbx")
                self.emit("    setne al")
                self.emit("    movzx rax, al")

# ============== MAIN COMPILER ==============
def compile_file(source_file):
    try:
        with open(source_file, 'r') as f:
            source_code = f.read()
        
        print(f"Compiling {source_file}...")
        print("=" * 60)
        
        # Lexical Analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        print(f"✓ Lexical Analysis: {len(tokens)} tokens")
        
        # Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"✓ Syntax Analysis: AST generated")
        
        # Code Generation
        codegen = CodeGenerator()
        assembly = codegen.generate(ast)
        print(f"✓ Code Generation: Assembly code generated")
        
        print("=" * 60)
        print("\n✓ Compilation successful!")
        print("\n" + "=" * 60)
        print("GENERATED ASSEMBLY CODE:")
        print("=" * 60)
        print(assembly)
        print("=" * 60)
        
        # print("\nTo assemble and run (Linux x64):")
        # print("  1. Save the output to a file (e.g., output.asm)")
        # print("  2. nasm -f elf64 output.asm -o output.o")
        # print("  3. gcc output.o -o output -no-pie")
        # print("  4. ./output")
        
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except NameError as e:
        print(f"Semantic Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file>")
        print("\nExample source code format:")
        print("  int x = 10;")
        print("  int y = 20;")
        print("  int sum = x + y;")
        print("  print(sum);")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    compile_file(source_file)