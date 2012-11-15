from __future__ import division
import csv
import matplotlib.pyplot as plt
from sys import argv

if len(argv)==1:
    infile=open("Output_file.csv","rb")
else:
    infile=open(argv[1],"rb")

inread=csv.reader(infile)
data=[e for e in inread]
infile.close

instances=0
wins=0
number=len(data)
scatter_m=[]
scatter_n=[]
max_data={}
running_win_percentage=[]
for row in data:
    instances+=1
    m=eval(row[1])
    n=eval(row[2])
    if m in max_data:
        max_data[m]=max(max_data[m],n)
    else:
        max_data[m]=n
    if eval(row[0]):
        wins+=1
        scatter_m.append(m)
        scatter_n.append(n)
    running_win_percentage.append(wins/instances)

line_m=[]
line_maxn=[]

for key in max_data:
    line_m.append(key)
    line_maxn.append(max_data[key])

plt.figure()
plt.imshow([[1,2],[2,3]])
plt.plot(line_m,line_maxn,label="Region Explored",color="black")
plt.scatter(scatter_m,scatter_n, label="Wins (%s/%s)"%(wins,number))
plt.xlabel("m")
plt.ylabel("n")
plt.title("Location of wins")
plt.legend(loc="upper right")
plt.savefig("Scatter_plot_of_wins.pdf")

plt.figure()
plt.plot(range(number),running_win_percentage)
plt.xlabel("Instances")
plt.ylabel("Winning %")
plt.savefig("Winning%.pdf")

print "---------------------"
print "Total instances:",number
print "Total wins:",wins
print "Success rate:",wins/number
print "---------------------"
