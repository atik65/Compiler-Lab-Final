import sys
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

try:
    import ply.lex as lex
    import ply.yacc as yacc
except ImportError:
    print("Error: PLY package not found. Please install it using:")
    print("pip install ply")
    sys.exit(1)

# ============================================================================
# TASK 1: LEXICAL ANALYSIS (TOKENIZATION) - Using PLY Lex
# ============================================================================

# Reserved keywords
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
}

# Token list
tokens = [
    'IDENTIFIER',
    'INTEGER_LITERAL',
    'FLOAT_LITERAL',
    'STRING_LITERAL',
    'CHAR_LITERAL',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MODULO',
    'ASSIGN',
    'EQ',
    'NE',
    'LT',
    'LE',
    'GT',
    'GE',
    'AND',
    'OR',
    'NOT',
    'INCREMENT',
    'DECREMENT',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'COMMA',
] + list(reserved.values())

# Token rules
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_CHAR_LITERAL(t):
    r"'([^'\\]|\\.)'"
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_COMMENT(t):
    r'//.*|/\*(.|\n)*?\*/'
    pass  # Ignore comments

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

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

# Global symbol table
symbol_table = SymbolTable()

# ============================================================================
# TASK 3 & 4: SYNTAX ANALYSIS AND PARSER (AST) - Using PLY Yacc
# ============================================================================

# AST Node Classes
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

# Parser rules
syntax_errors = []
syntax_ok_lines = set()

def p_program(p):
    '''program : declaration_list'''
    p[0] = Program(p[1])

def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaration(p):
    '''declaration : var_declaration
                   | function_declaration
                   | statement'''
    p[0] = p[1]

def p_var_declaration(p):
    '''var_declaration : type IDENTIFIER SEMICOLON
                       | type IDENTIFIER ASSIGN expression SEMICOLON'''
    if len(p) == 4:
        symbol_table.add_symbol(p[2], p[1], p.lineno(2))
        syntax_ok_lines.add(p.lineno(1))
        p[0] = VarDecl(p[1], p[2], None, p.lineno(1))
    else:
        symbol_table.add_symbol(p[2], p[1], p.lineno(2))
        syntax_ok_lines.add(p.lineno(1))
        p[0] = VarDecl(p[1], p[2], p[4], p.lineno(1))

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | VOID'''
    p[0] = p[1]

def p_function_declaration(p):
    '''function_declaration : type IDENTIFIER LPAREN parameter_list RPAREN block
                            | type IDENTIFIER LPAREN RPAREN block'''
    if len(p) == 7:
        symbol_table.add_symbol(p[2], f"function:{p[1]}", p.lineno(2))
        syntax_ok_lines.add(p.lineno(1))
        old_scope = symbol_table.current_scope
        symbol_table.current_scope = p[2]
        for param_type, param_name in p[4]:
            symbol_table.add_symbol(param_name, param_type, p.lineno(2))
        symbol_table.current_scope = old_scope
        p[0] = FunctionDecl(p[1], p[2], p[4], p[5], p.lineno(1))
    else:
        symbol_table.add_symbol(p[2], f"function:{p[1]}", p.lineno(2))
        syntax_ok_lines.add(p.lineno(1))
        p[0] = FunctionDecl(p[1], p[2], [], p[4], p.lineno(1))

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_parameter(p):
    '''parameter : type IDENTIFIER'''
    p[0] = (p[1], p[2])

def p_block(p):
    '''block : LBRACE statement_list RBRACE
             | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = Block(p[2])
    else:
        p[0] = Block([])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : expression_statement
                 | var_declaration
                 | if_statement
                 | while_statement
                 | for_statement
                 | return_statement
                 | block'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON
                            | SEMICOLON'''
    if len(p) == 3:
        syntax_ok_lines.add(p.lineno(2))
        p[0] = ExprStmt(p[1])
    else:
        syntax_ok_lines.add(p.lineno(1))
        p[0] = None

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        syntax_ok_lines.add(p.lineno(1))
        p[0] = IfStmt(p[3], p[5], None, p.lineno(1))
    else:
        syntax_ok_lines.add(p.lineno(1))
        p[0] = IfStmt(p[3], p[5], p[7], p.lineno(1))

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement'''
    syntax_ok_lines.add(p.lineno(1))
    p[0] = WhileStmt(p[3], p[5], p.lineno(1))

def p_for_statement(p):
    '''for_statement : FOR LPAREN expression_opt SEMICOLON expression_opt SEMICOLON expression_opt RPAREN statement'''
    syntax_ok_lines.add(p.lineno(1))
    p[0] = ForStmt(p[3], p[5], p[7], p[9], p.lineno(1))

def p_expression_opt(p):
    '''expression_opt : expression
                      | empty'''
    p[0] = p[1]

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    if len(p) == 4:
        syntax_ok_lines.add(p.lineno(1))
        p[0] = ReturnStmt(p[2], p.lineno(1))
    else:
        syntax_ok_lines.add(p.lineno(1))
        p[0] = ReturnStmt(None, p.lineno(1))

def p_expression(p):
    '''expression : assignment_expression'''
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment_expression : IDENTIFIER ASSIGN assignment_expression
                             | logical_or_expression'''
    if len(p) == 4:
        p[0] = Assignment(p[1], p[3], p.lineno(1))
    else:
        p[0] = p[1]

def p_logical_or_expression(p):
    '''logical_or_expression : logical_or_expression OR logical_and_expression
                             | logical_and_expression'''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_logical_and_expression(p):
    '''logical_and_expression : logical_and_expression AND equality_expression
                              | equality_expression'''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_equality_expression(p):
    '''equality_expression : equality_expression EQ relational_expression
                           | equality_expression NE relational_expression
                           | relational_expression'''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_relational_expression(p):
    '''relational_expression : relational_expression LT additive_expression
                             | relational_expression GT additive_expression
                             | relational_expression LE additive_expression
                             | relational_expression GE additive_expression
                             | additive_expression'''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_additive_expression(p):
    '''additive_expression : additive_expression PLUS multiplicative_expression
                           | additive_expression MINUS multiplicative_expression
                           | multiplicative_expression'''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_multiplicative_expression(p):
    '''multiplicative_expression : multiplicative_expression MULTIPLY unary_expression
                                 | multiplicative_expression DIVIDE unary_expression
                                 | multiplicative_expression MODULO unary_expression
                                 | unary_expression'''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_unary_expression(p):
    '''unary_expression : MINUS unary_expression
                        | NOT unary_expression
                        | INCREMENT unary_expression
                        | DECREMENT unary_expression
                        | postfix_expression'''
    if len(p) == 3:
        p[0] = UnaryOp(p[1], p[2])
    else:
        p[0] = p[1]

def p_postfix_expression(p):
    '''postfix_expression : primary_expression INCREMENT
                          | primary_expression DECREMENT
                          | primary_expression'''
    if len(p) == 3:
        p[0] = UnaryOp(p[2], p[1])
    else:
        p[0] = p[1]

def p_primary_expression(p):
    '''primary_expression : IDENTIFIER
                          | INTEGER_LITERAL
                          | FLOAT_LITERAL
                          | STRING_LITERAL
                          | CHAR_LITERAL
                          | LPAREN expression RPAREN
                          | function_call'''
    if len(p) == 2:
        if isinstance(p[1], str):
            p[0] = Identifier(p[1])
        elif isinstance(p[1], int):
            p[0] = Literal(str(p[1]), "int")
        elif isinstance(p[1], float):
            p[0] = Literal(str(p[1]), "float")
        else:
            p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN argument_list RPAREN
                     | IDENTIFIER LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = FunctionCall(p[1], p[3])
    else:
        p[0] = FunctionCall(p[1], [])

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        syntax_errors.append(f"Line {p.lineno}: Syntax error at '{p.value}'")
        # Try to recover by skipping the token
        parser.errok()
    else:
        syntax_errors.append("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

def print_syntax_analysis():
    print("\n" + "="*80)
    print("TASK 3: SYNTAX ANALYSIS")
    print("="*80)
    
    if syntax_errors:
        for error in syntax_errors:
            print(error)
    
    for line in sorted(syntax_ok_lines):
        if not any(str(line) in err for err in syntax_errors):
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
            if node.expression:
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





# class ASTPrinter:
#     def __init__(self, ast: Program):
#         self.ast = ast
#         self.dot_code = []
#         self.node_id = 0

#     def print_tree(self):
#         print("\n" + "="*80)
#         print("TASK 4: ABSTRACT SYNTAX TREE (AST)")
#         print("="*80)
#         print("Generating AST as 'ast.png'...")
#         self.generate_dot()
#         self.render_graph()

#     def generate_dot(self):
#         self.dot_code = [
#             "digraph AST {",
#             "    node [shape=box, style=filled, fillcolor=lightblue];",
#             "    edge [color=black];"
#         ]
#         self._add_node(self.ast, None)
#         self.dot_code.append("}")

#     def _add_node(self, node, parent_id):
#         if node is None:
#             return None
#         node_id = f"node_{self.node_id}"
#         self.node_id += 1

#         label = self._node_label(node)
#         self.dot_code.append(f'    {node_id} [label="{label}"];')

#         if parent_id:
#             self.dot_code.append(f'    {parent_id} -> {node_id};')

#         children = self._get_children(node)
#         for child in children:
#             child_id = self._add_node(child, node_id)
#             if child_id:
#                 pass  # Already connected in _add_node

#         return node_id

#     def _node_label(self, node):
#         if isinstance(node, Program):
#             return "Program"
#         elif isinstance(node, VarDecl):
#             return f"{node.var_type} {node.name}"
#         elif isinstance(node, Assignment):
#             return "="
#         elif isinstance(node, BinaryOp):
#             return node.operator
#         elif isinstance(node, Identifier):
#             return node.name
#         elif isinstance(node, Literal):
#             return str(node.value)
#         elif isinstance(node, FunctionCall):
#             return node.name
#         else:
#             return type(node).__name__

#     def _get_children(self, node):
#         if isinstance(node, Program):
#             return node.declarations
#         elif isinstance(node, VarDecl):
#             return [node.init_value] if node.init_value else []
#         elif isinstance(node, Assignment):
#             return [node.target, node.value]
#         elif isinstance(node, BinaryOp):
#             return [node.left, node.right]
#         elif isinstance(node, FunctionCall):
#             return node.args
#         elif isinstance(node, Block):
#             return node.statements
#         elif isinstance(node, IfStmt):
#             return [node.condition, node.then_block] + ([node.else_block] if node.else_block else [])
#         elif isinstance(node, WhileStmt):
#             return [node.condition, node.body]
#         else:
#             return []

#     def render_graph(self):
#         dot_content = "\n".join(self.dot_code)
#         from graphviz import Source
#         src = Source(dot_content)
#         src.render('ast', format='png', cleanup=True)
#         print("✅ AST saved as 'ast.png'")


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
            elif isinstance(decl, (IfStmt, WhileStmt, ForStmt, ReturnStmt, ExprStmt)):
                self.visit_statement(decl)
    
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
            if stmt:
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
            if node.expression:
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
        self.optimized_code = []  # Reset in case of reuse
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
        print("\nNote: This compiler requires the PLY package.")
        print("Install it using: pip install ply")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    print("="*80)
    print("MINI C COMPILER (Using PLY - Python Lex-Yacc)")
    print("="*80)
    print(f"Input File: {input_file}")
    print("="*80)
    
    # TASK 1: Lexical Analysis
    print("\n" + "="*80)
    print("TASK 1: LEXICAL ANALYSIS (TOKENS)")
    print("="*80)
    
    lexer.input(source_code)
    tokens_list = []
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
    
    print(f"{'Token Type':<25} {'Value':<20} {'Line':<10} {'Position':<10}")
    print("-"*80)
    for tok in tokens_list:
        print(f"{tok.type:<25} {str(tok.value):<20} {tok.lineno:<10} {tok.lexpos:<10}")
    print()
    
    # Reset lexer for parsing
    lexer.lineno = 1
    
    # TASK 3 & 4: Syntax Analysis and Parsing
    global syntax_errors, syntax_ok_lines
    syntax_errors = []
    syntax_ok_lines = set()
    
    ast = parser.parse(source_code, lexer=lexer)
    
    print_syntax_analysis()
    
    # TASK 2: Print Symbol Table
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