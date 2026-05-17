import json, sys

with open(sys.argv[1]) as f:
    ast = json.load(f)

symbol_table = {}

for node in ast.get("statements", []):
    if node["type"] == "assign":
        var = node["id"]
        symbol_table[var] = "int"

print("✅ Semantic Analysis Complete")
print("Symbol Table:", symbol_table)
