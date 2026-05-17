import re
from typing import Dict, List, Tuple, Any

class CodeOptimizer:
    def __init__(self):
        self.constants = {}  # Store constant values
        self.used_variables = set()  # Track used variables
        
    def parse_statement(self, line: str) -> Tuple[str, Any]:
        """Parse a single statement and return its type and components"""
        line = line.strip()
        
        # Assignment: var = expr
        assign_match = re.match(r'(\w+)\s*=\s*(.+)', line)
        if assign_match:
            var, expr = assign_match.groups()
            return ('assign', var, expr.strip())
        
        # Print statement
        if line.startswith('print'):
            print_match = re.match(r'print\s*\((.+)\)', line)
            if print_match:
                expr = print_match.group(1).strip()
                return ('print', expr)
        
        # Return statement
        if line.startswith('return'):
            return_match = re.match(r'return\s+(.+)', line)
            if return_match:
                expr = return_match.group(1).strip()
                return ('return', expr)
        
        # If statement (simplified)
        if line.startswith('if'):
            return ('if', line)
        
        return ('unknown', line)
    
    def evaluate_expression(self, expr: str) -> Any:
        """Try to evaluate an expression with constant folding"""
        expr = expr.strip()
        
        # Replace known constants in the expression
        for var, val in self.constants.items():
            # Use word boundaries to avoid partial replacements
            expr = re.sub(r'\b' + re.escape(var) + r'\b', str(val), expr)
        
        # Try to evaluate as a constant expression
        try:
            # Only evaluate if expression contains only numbers and operators
            if re.match(r'^[\d\+\-\*/\(\)\s\.]+$', expr):
                result = eval(expr)
                return result
            return expr
        except:
            return expr
    
    def track_variable_usage(self, expr: str):
        """Track which variables are used in an expression"""
        # Find all variable names (alphanumeric identifiers)
        variables = re.findall(r'\b[a-zA-Z_]\w*\b', expr)
        self.used_variables.update(variables)
    
    def constant_propagation(self, statements: List[str]) -> List[str]:
        """Apply constant propagation optimization"""
        optimized = []
        
        for stmt in statements:
            parsed = self.parse_statement(stmt)
            
            if parsed[0] == 'assign':
                _, var, expr = parsed
                
                # Evaluate the expression with known constants
                evaluated_expr = self.evaluate_expression(expr)
                
                # Check if result is a constant
                if isinstance(evaluated_expr, (int, float)):
                    self.constants[var] = evaluated_expr
                    optimized.append(f"{var} = {evaluated_expr}")
                else:
                    # Not a constant, remove from constants dict if present
                    if var in self.constants:
                        del self.constants[var]
                    
                    # Replace constants in expression
                    new_expr = str(evaluated_expr)
                    optimized.append(f"{var} = {new_expr}")
                    
            elif parsed[0] == 'print':
                _, expr = parsed
                self.track_variable_usage(expr)
                evaluated_expr = self.evaluate_expression(expr)
                optimized.append(f"print({evaluated_expr})")
                
            elif parsed[0] == 'return':
                _, expr = parsed
                self.track_variable_usage(expr)
                evaluated_expr = self.evaluate_expression(expr)
                optimized.append(f"return {evaluated_expr}")
                
            else:
                # Track variables in unknown statements
                self.track_variable_usage(stmt)
                optimized.append(stmt)
        
        return optimized
    
    def dead_code_elimination(self, statements: List[str]) -> List[str]:
        """Remove assignments to variables that are never used"""
        # First pass: identify all used variables
        temp_used = set()
        for stmt in statements:
            parsed = self.parse_statement(stmt)
            if parsed[0] == 'assign':
                _, var, expr = parsed
                # Track variables used in RHS of assignment
                variables = re.findall(r'\b[a-zA-Z_]\w*\b', expr)
                temp_used.update(variables)
            elif parsed[0] in ['print', 'return']:
                expr = parsed[1]
                variables = re.findall(r'\b[a-zA-Z_]\w*\b', expr)
                temp_used.update(variables)
        
        # Second pass: remove dead assignments
        optimized = []
        for stmt in statements:
            parsed = self.parse_statement(stmt)
            
            if parsed[0] == 'assign':
                _, var, expr = parsed
                # Keep assignment if variable is used
                if var in temp_used or var in self.used_variables:
                    optimized.append(stmt)
                else:
                    # Dead code - commented out for visibility
                    optimized.append(f"# DEAD CODE: {stmt}")
            else:
                optimized.append(stmt)
        
        return optimized
    
    def optimize(self, code: str) -> str:
        """Apply all optimizations to the code"""
        # Split code into statements (one per line)
        statements = [line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        
        print("=== Original Code ===")
        for stmt in statements:
            print(stmt)
        
        # Apply constant propagation and folding
        print("\n=== After Constant Propagation & Folding ===")
        propagated = self.constant_propagation(statements)
        for stmt in propagated:
            print(stmt)
        
        # Apply dead code elimination
        print("\n=== After Dead Code Elimination ===")
        optimized = self.dead_code_elimination(propagated)
        result = []
        for stmt in optimized:
            print(stmt)
            if not stmt.startswith('# DEAD CODE:'):
                result.append(stmt)
        
        return '\n'.join(result)


def main():
    import sys
    
    print("Mini Compiler - Code Optimizer")
    print("=" * 50)
    
    # Check if source file is provided
    if len(sys.argv) < 2:
        print("Usage: python optimizer.py <source_file>")
        print("\nExample: python optimizer.py source.txt")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    try:
        # Read source code from file
        with open(source_file, 'r') as f:
            source_code = f.read()
        
        print(f"Reading source file: {source_file}\n")
        
        # Optimize the code
        optimizer = CodeOptimizer()
        optimized_code = optimizer.optimize(source_code)
        
        print("\n" + "=" * 50)
        print("=== Final Optimized Code ===")
        print("=" * 50)
        print(optimized_code)
        
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()