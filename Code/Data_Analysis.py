from __future__ import division
import csv
from sys import argv

if len(argv)==1:
    infile=open("Output_file.csv","rb")
else:
    infile=open(argv[1],"rb")

inread=csv.reader(infile)
data=[e for e in inread]
infile.close


wins=0
number=len(data)
for row in data:
    if eval(row[0]):
        wins+=1

print "Total files:",number
print "Total wins:",wins
print "Success rate:",wins/number
