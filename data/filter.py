import sys
import os

lines = []
with open(sys.argv[1], 'r') as f:
    for line in f:
        try:
            sp = line.split()
            if sp[1] == 'IP' and sp[2] == sys.argv[2]:
                lines.append(sp)
        except:
            continue

out = "\n".join([" ".join(el) for el in lines])

with open(sys.argv[3], 'w') as f:
    f.write(out)
