ir = open("../build/optimized_ir.txt").read().splitlines()

with open("../build/assembly.asm", "w") as f:
    for line in ir:
        parts = line.split("=")
        if len(parts) == 2:
            lhs, rhs = parts
            f.write(f"MOV {lhs.strip()}, {rhs.strip()}\n")

print("✅ Assembly Generated: build/assembly.asm")
