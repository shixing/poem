import sys


lines = []
for line in sys.stdin:
    lines.append(line)

for i in xrange(1,15):
    for line in lines:
        print line.replace("@@",str(i)),
    print 
    print


