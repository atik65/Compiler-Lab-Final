import re
import sys

symbol_table = []

def build_symbol_table(code):
    pattern = r'\b(int|float|char)\s+([a-zA-Z_]\w*)'
    for dtype, var in re.findall(pattern, code):
        symbol_table.append({"type": dtype, "name": var})

def display_symbol_table():
    if not symbol_table:
        print("No symbols found.")
        return

    print("\n" + "="*35)
    print("{:<5} {:<15} {:<10}".format("No.", "Identifier", "Type"))
    print("="*35)
    for i, sym in enumerate(symbol_table, start=1):
        print("{:<5} {:<15} {:<10}".format(i, sym["name"], sym["type"]))
    print("="*35 + "\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 phase2_symbol_table.py <input_file>")
        return

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    build_symbol_table(code)
    display_symbol_table()

if __name__ == "__main__":
    main()



# python3 phase2_symbol_table.py input/test_input.c > symbols.txt
