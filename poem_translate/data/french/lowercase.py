import sys

for line in sys.stdin:
    line = line.decode("utf8").strip()
    line = line.lower()
    print line.encode("utf8")


