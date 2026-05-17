ir = []
# Generate simple 3-address code
ir.append("t1 = a + b")
ir.append("c = t1 * 2")

with open("../build/ir.txt", "w") as f:
    f.write("\n".join(ir))
