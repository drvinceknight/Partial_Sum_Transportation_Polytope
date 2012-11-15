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
running_win_percentage=[]
max_m=0
max_n=0
number_of_wins_dictionary={}
for row in data:
    instances+=1
    m=eval(row[1])
    n=eval(row[2])
    string="[%s,%s]"%(m,n)
    max_m=max(max_m,m)
    max_n=max(max_n,n)
    if eval(row[0]):
        wins+=1
        if string in number_of_wins_dictionary:
            number_of_wins_dictionary[string]+=1
        else:
            number_of_wins_dictionary[string]=1
    running_win_percentage.append(wins/instances)


number_of_wins_array=[[0 for n in range(max_n)] for m in range(max_m)]
for e in number_of_wins_dictionary:
    l=eval(e)
    number_of_wins_array[l[0]-1][l[1]-1]=number_of_wins_dictionary[e]

plt.figure()
<<<<<<< HEAD
plt.plot(line_m,line_maxn,label="Region Explored",color="black")
plt.scatter(scatter_m,scatter_n, label="Wins (%s/%s)"%(wins,number))
=======
plt.imshow(number_of_wins_array,origin='lower',interpolation='nearest')
plt.colorbar()
plt.set_cmap('hot')
>>>>>>> im_plot
plt.xlabel("m")
plt.ylabel("n")
plt.title("Location of wins")
#plt.legend(loc="upper right")
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
