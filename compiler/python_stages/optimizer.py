lines = open("../build/ir.txt").read().splitlines()
optimized = [line for line in lines if not "0 *" in line]  # remove useless ops

with open("../build/optimized_ir.txt", "w") as f:
    f.write("\n".join(optimized))

print("✅ Optimization Done")
