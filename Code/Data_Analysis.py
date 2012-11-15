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
number_of_wins_dictionary={}
number_of_attempts_dictionary={}
max_m=0
max_n=0
max_n_dictionary={}
for row in data:
    instances+=1
    m=eval(row[1])
    n=eval(row[2])
    string="[%s,%s]"%(m,n)
    if m in max_n_dictionary:
        max_n_dictionary[m]=max(max_n_dictionary[m],n)
    else:
        max_n_dictionary[m]=n
    if string in number_of_attempts_dictionary:
        number_of_attempts_dictionary[string]+=1
    else:
        number_of_attempts_dictionary[string]=1
    if eval(row[0]):
        wins+=1
        if string in number_of_wins_dictionary:
            number_of_wins_dictionary[string]+=1
        else:
            number_of_wins_dictionary[string]=1
    max_m=max(max_m,m)
    max_n=max(max_n,n)
    running_win_percentage.append(wins/instances)


number_of_wins_array=[[0 for n in range(max_n)] for m in range(max_m)]
for e in number_of_wins_dictionary:
    l=eval(e)
    number_of_wins_array[l[0]-1][l[1]-1]=number_of_wins_dictionary[e]/number_of_attempts_dictionary[e]

x_attempt=[]
y_attempt=[]
for e in max_n_dictionary:
    x_attempt.append(e)
    y_attempt.append(max_n_dictionary[e])

plt.figure()
plt.plot(x_attempt,y_attempt,color="red",label="Region Explored")
plt.imshow(number_of_wins_array,origin='lower',interpolation='nearest')
plt.colorbar()
#plt.set_cmap('hot')
plt.xlabel("m")
plt.ylabel("n")
plt.title("Percentage of wins")
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
