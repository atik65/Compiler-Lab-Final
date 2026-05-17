# Mini Compiler Project

A complete compiler implementation integrating **Lex** (lexical analysis), **Bison** (syntax analysis), and **Python** (semantic analysis, optimization, and code generation).

## 📋 Project Overview

This project implements all 7 phases of compilation:

1. **Lexical Analysis (Lex)** - Tokenization of source code
2. **Symbol Table (Python)** - Variable tracking and scope management
3. **Syntax Analysis (Bison)** - Grammar validation
4. **AST Construction (Bison)** - Abstract Syntax Tree generation
5. **Intermediate Code Generation (Python)** - Three-address code
6. **Code Optimization (Python)** - Constant folding, dead code elimination
7. **Assembly Generation (Python)** - x86-64 assembly output

## 🏗️ Architecture

```
Source Code (.txt)
       ↓
   [LEX - C]
       ↓
    Tokens
       ↓
  [BISON - C]
       ↓
  AST (JSON)
       ↓
  [PYTHON]
  ├─ Symbol Table
  ├─ Semantic Analysis
  ├─ Intermediate Code
  ├─ Optimization
  └─ Assembly Generation
       ↓
  Assembly Code (.s)
```

## 📦 Prerequisites

### Required Software:

- **Flex/Lex** - Lexical analyzer generator
- **Bison/Yacc** - Parser generator
- **GCC** - C compiler
- **Python 3.6+** - Backend compiler phases
- **Make** - Build automation

### Installation (Ubuntu/Debian):

```bash
sudo apt-get update
sudo apt-get install flex bison gcc make python3
```

### Installation (macOS):

```bash
brew install flex bison gcc make python3
```

### Installation (Fedora/RHEL):

```bash
sudo dnf install flex bison gcc make python3
```

## 📁 Project Structure

```
mini-compiler/
├── lexer.l              # Lex specification (Task 1)
├── parser.y             # Bison grammar (Task 3-4)
├── compiler.py          # Python backend (Task 2, 5-7)
├── Makefile             # Build automation
├── example.txt          # Example source program
└── README.md            # This file
```

## 🚀 Quick Start

### 1. Build the Compiler

```bash
make all
```

### 2. Test with Example

```bash
make test
```

### 3. Compile Your Own Program

```bash
make compile INPUT=your_program.txt
```

### 4. Build and Run Executable

```bash
make run INPUT=your_program.txt
```

## 📝 Language Syntax

### Data Types

- `int` - Integer type
- `float` - Floating point type

### Variable Declaration

```c
int x;              // Declaration
int y = 10;         // Declaration with initialization
float pi = 3.14;    // Float variable
```

### Arithmetic Operations

```c
int result = x + y;
int product = a * b;
int difference = x - y;
int quotient = x / y;
```

### Control Flow

#### If Statement

```c
if (x > 10) {
    print(x);
}
```

#### If-Else Statement

```c
if (x > y) {
    print(x);
} else {
    print(y);
}
```

#### While Loop

```c
int i = 0;
while (i < 10) {
    i = i + 1;
}
```

### Built-in Functions

```c
print(variable);    // Print variable value
return value;       // Return from program
```

### Comments

```c
// Single line comment
```

## 🔧 Detailed Usage

### Manual Step-by-Step Compilation

#### Step 1: Build Parser

```bash
bison -d -v parser.y
flex lexer.l
gcc -Wall -g parser.tab.c lex.yy.c -o parser -lfl
```

#### Step 2: Generate AST

```bash
./parser example.txt
```

This creates `ast.json` containing the Abstract Syntax Tree.

#### Step 3: Run Python Backend

```bash
python3 compiler.py ast.json
```

This performs:

- Symbol table creation
- Semantic analysis
- Intermediate code generation
- Code optimization
- Assembly code generation

Output: `output.s` (assembly file)

#### Step 4: Assemble to Executable

```bash
gcc output.s -o program -no-pie
./program
```

## 📊 Output Examples

### Symbol Table

```
=== Symbol Table ===
Name            Type       Scope    Offset   Init
------------------------------------------------------------
x               int        0        0        True
y               int        0        4        True
z               int        0        8        True
result          int        0        12       True
```

### Intermediate Code (Three-Address Code)

```
0: # Program Start
1: DECLARE x int
2: x = 10
3: DECLARE y int
4: y = 20
5: DECLARE z int
6: t0 = x + y
7: z = t0
8: t1 = z * 2
9: DECLARE result int
10: result = t1
```

### Optimized Code

After constant folding and dead code elimination:

```
1: DECLARE x int
2: x = 10
3: DECLARE y int
4: y = 20
5: DECLARE z int
6: z = 30          # Constant folded: 10 + 20
7: DECLARE result int
8: result = 60     # Constant folded: 30 * 2
```

### Assembly Output (x86-64)

```asm
.section .data
fmt: .string "%d\n"

.section .text
.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $16, %rsp
    # Declare x as int
    movq $10, [rbp-0]
    # Declare y as int
    movq $20, [rbp-4]
    ...
```

## 🧪 Testing

### Run All Tests

```bash
make test
```

### Test Custom Program

Create a file `test.txt`:

```c
int a = 5;
int b = 10;
int sum = a + b;
print(sum);
return sum;
```

Compile and run:

```bash
make run INPUT=test.txt
```

## 🐛 Troubleshooting

### Error: "command not found: flex"

Install Flex: `sudo apt-get install flex`

### Error: "undefined reference to 'yywrap'"

Add `-lfl` flag when linking: `gcc ... -lfl`

### Error: Python syntax errors

Ensure Python 3.6+ is installed: `python3 --version`

### Error: Assembly won't assemble

The generated assembly is x86-64 compatible. Ensure you're on a 64-bit system.

### Error: "Permission denied" when running ./program

Make executable: `chmod +x program`

## 📚 Educational Value

This project demonstrates:

1. **Lexical Analysis** - Pattern matching and tokenization
2. **Syntax Analysis** - Grammar rules and parsing
3. **Semantic Analysis** - Type checking and scope resolution
4. **Code Generation** - Translation to lower-level representations
5. **Optimization** - Improving code efficiency
6. **Multi-language Integration** - Combining C and Python

## 🎯 Learning Outcomes

- Understanding compiler phases
- Working with Lex and Bison
- Implementing symbol tables
- Generating intermediate representations
- Code optimization techniques
- Assembly code generation
- Inter-language communication

## 🔄 Extending the Compiler

### Add New Features

#### 1. Add For Loops

Modify `lexer.l` to recognize `for` keyword:

```c
"for"               { return FOR; }
```

Update `parser.y` grammar:

```yacc
for_statement:
    FOR LPAREN assignment expression SEMICOLON assignment RPAREN
    LBRACE statement_list RBRACE
    ;
```

#### 2. Add Functions

Add function declaration syntax and call mechanism.

#### 3. Add Arrays

Extend grammar for array declarations and indexing.

#### 4. Add More Optimizations

Implement in `compiler.py`:

- Common subexpression elimination
- Loop unrolling
- Register allocation

## 📖 References

- **Lex & Yacc Tutorial**: [GNU Flex Manual](https://www.gnu.org/software/flex/manual/)
- **Bison Documentation**: [GNU Bison Manual](https://www.gnu.org/software/bison/manual/)
- **Compiler Design**: "Compilers: Principles, Techniques, and Tools" (Dragon Book)
- **x86-64 Assembly**: [AMD64 Architecture Reference](https://www.amd.com/system/files/TechDocs/24592.pdf)

## 🤝 Contributing

To extend this project:

1. Fork the repository
2. Add your features
3. Test thoroughly
4. Submit improvements

## 📄 License

This is an educational project. Feel free to use and modify for learning purposes.

## 👨‍💻 Author

Created as a comprehensive compiler design project demonstrating the integration of:

- C (via Lex/Bison)
- Python
- Assembly (x86-64)

## 🎓 Acknowledgments

This project covers standard compiler theory topics taught in:

- CS Compiler Design courses
- Programming Language Implementation courses
- Systems Programming courses

---

**Happy Compiling! 🚀**
