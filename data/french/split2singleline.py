import sys
i = 1
for line in sys.stdin:
    if line.strip() == "":
        continue
    f = open("./source.single.{}".format(i),"w")
    f.write(line)
    f.close()
    i += 1
