#! /usr/bin/env python
#"""
#Code to define a transportation problem and a partial sum transportation problem
#"""
from __future__ import division
from itertools import permutations
from openopt import NLP,LP
from numpy import *
from random import random,randint
import csv

def row_permutation_of_cost_function(r,s,c):
    """
    This function is used at a later stage to permute rows of cost function
    """
    m=len(r)
    s=len(s)
    output=[[] for i in range(m)]
    for e in output:
        for i in range(s):
            e.append(c.pop(0))
    output=permutations(output)
    r=[]
    for e in output:
        e=[i for k in e for i in k]
        r.append(e)
    return r

class Problem():
    """
    This is the main class for our problems, it contains the equality constraints.
    """
    def __init__(self,r,s,cost_matrix):
        if sum(r)==sum(s):
            self.m=len(r)
            self.n=len(s)
            self.cost_matrix=cost_matrix
            self.r=r
            self.s=s
            self.beq=tuple(r+s)
            Aeq=[[0 for i in range(self.m*self.n)] for j in range(self.m+self.n)]
            k=0
            #Code for row sums:
            for r in Aeq[:self.m]:
               index=range(k,k+self.n)
               for j in index:
                   r[j]=1
               k+=self.n
            k=0
            #Code for col sums:
            for r in Aeq[self.m:]:
               index=[k+j*self.n for j in range(self.m)]
               for j in index:
                   r[j]=1
               k+=1
            self.Aeq=mat(Aeq)
        else:
            print "Invalid problem"


class Transportation_Problem(Problem):
    """
    This class inherits from previous problem class giving methods for solving as an LP and also including positivity constraints.
    """
    def __init__(self,r,s,cost_matrix):
        Problem.__init__(self,r,s,cost_matrix)
        self.cost_function=array(cost_matrix)
        self.lb=[0 for k in range(self.m*self.n)]
    def evaluate(self,matrix):
        return self.cost_function(matrix)
    def solve(self):
        p=LP(self.cost_function,Aeq=self.Aeq,beq=self.beq,lb=self.lb)
        p.iprint = -1
        r=p.solve('pclp')
        return [r.xf,r.ff]

class Partial_Sum_Transportation_Problem(Problem):
    """
    This class inherits from Problem class giving methods for solving as an NLP and also including partial sum positivity constraints.
    """
    def __init__(self,r,s,cost_matrix):
        Problem.__init__(self,r,s,cost_matrix)
        self.cost_function=lambda a: sum([abs(a[k])*cost_matrix[k] for k in range(self.m*self.n)])
        self.lb=[-max(r[k//self.n],s[k%self.n]) for k in range(self.m*self.n)]
        self.ub=[max(r[k//self.n],s[k%self.n]) for k in range(self.m*self.n)]
        tau=sum(self.s)
        self.initial_solution=[r[k//self.n]*s[k%self.n]/tau for k in range(self.m*self.n)]
        A=[[0 for i in range(self.m*self.n)] for j in range(2*self.m*(self.n-1)+2*self.n*(self.m-1))]
        b=[0  for j in range(2*self.m*(self.n-1)+2*self.n*(self.m-1))]

#First row sum
        for h in range(1,self.n):
            k=0
            for r in A[(h-1)*self.m:h*self.m]:
               index=[j+k*self.n for j in range(h)]
               for j in index:
                   r[j]=-1
               k+=1

#Reverse row sum
        for h in range(1,self.n):
            k=0
            for r in A[(self.n+(h-1)-1)*self.m:(self.n+h-1)*self.m]:
               index=[self.n-1-j+k*self.n for j in range(h)]
               for j in index:
                   r[j]=-1
               k+=1

#First column sum
        for h in range(1,self.m):
            k=0
            for r in A[2*self.m*(self.n-1)+(h-1)*self.n:2*self.m*(self.n-1)+h*self.n]:
               index=[k+j*self.n for j in range(h)]
               for j in index:
                   r[j]=-1
               k+=1

#Reverse column sum
        for h in range(1,self.m):
            k=0
            for r in A[2*self.m*(self.n-1)+(self.m-1)*self.n+(h-1)*self.n:2*self.m*(self.n-1)+(self.m-1)*self.n+h*self.n]:
               index=[self.n*self.m-1-k-j*self.n for j in range(h)]
               for j in index:
                   r[j]=-1
               k+=1

        self.A=A
        self.b=b
    def evaluate(self,matrix):
        return self.cost_function(matrix)
    def solve(self):
        p=NLP(self.cost_function,self.initial_solution,Aeq=self.Aeq,beq=self.beq,A=self.A,b=self.b,lb=self.lb,ub=self.ub)
        p.iprint = -1
        r=p.solve('ralg')
        return [r.xf,r.ff]

class Solution_Comparison():
    """
    This defines a class that compares two approaches to solving a given problem.
    """
    def __init__(self,r,s,c,row_permute=True):
        self.Transportation_Solution=Transportation_Problem(r,s,c).solve()
        [best_solution,best_cost]=Partial_Sum_Transportation_Problem(r,s,c).solve()
        if row_permute:
            for e in row_permutation_of_cost_function(r,s,c):
                [candidate_solution,candidate_cost]=Partial_Sum_Transportation_Problem(r,s,e).solve()
                if candidate_cost<best_cost:
                    [best_solution,best_cost]=[candidate_solution,candidate_cost]
        self.Partial_Sum_Transportation_Solution=[best_solution,best_cost]
    def Costs(self):
        return [self.Transportation_Solution[1],self.Partial_Sum_Transportation_Solution[1]]
    def Solutions(self):
        return [self.Transportation_Solution[0],self.Partial_Sum_Transportation_Solution[0]]
    def Partial_Sum_Optimal(self,precision=2):
        Partial_Sum_Solution=[round(e,precision) for e in self.Partial_Sum_Transportation_Solution[0]]
        return min(Partial_Sum_Solution)<0

class Comparison_Experiment():
    """
    This defines a class of experiments, the compare_instance method generates a random instance.
    """
    def __init__(self,Max_m,Max_n,Max_tau_value,Max_c_value,row_permute=False):
        self.Max_m=Max_m
        self.Max_n=Max_n
        self.Max_tau_value=Max_tau_value
        self.Max_c_value=Max_c_value
        self.row_permute=row_permute
    def Compare_instance(self):
        m=randint(3,self.Max_m)
        n=randint(3,self.Max_n)
        self.m=m
        self.n=n
        tau=randint(1,self.Max_tau_value)
        r=[random() for e in range(m)]
        r=[round(tau*e/sum(r),2) for e in r]
        s=[random() for e in range(n)]
        s=[round(sum(r)*e/sum(s),2) for e in s]
        c=[self.Max_c_value*random() for e in range(m*n)]
        if sum(r)==sum(s):
            result=Solution_Comparison(r,s,c,self.row_permute)
            return [result.Partial_Sum_Optimal(),m,n,r,s,c,tau,result.Costs()[0],result.Costs()[1],[e for e in result.Solutions()[0]],[e for e in result.Solutions()[1]]]
        return False

def Run_Experiment(Max_m,Max_n,Max_tau_value,Max_c_value,row_permute=False,csv_file="Output_file.csv"):
    """
    This function runs experiments (until interrupted) output to a csv file.
    """
    k=0
    number_of_wins=0
    while True:
        a=Comparison_Experiment(Max_m,Max_n,Max_tau_value,Max_c_value,row_permute)
        try:
            b=a.Compare_instance()
            if b:
                k+=1
                print ""
                print "------------------------------------------"
                print "Instance number %s completed."%k
                print "\tm:",a.m
                print "\tn:",a.n
                if b[0]:
                    number_of_wins+=1
                print "\tNumber of wins:",number_of_wins
                print "------------------------------------------"
                print ""
                outfile=open(csv_file,"a")
                writefile=csv.writer(outfile)
                writefile.writerow(b)
                outfile.close()
        except:
            pass

#Run_Experiment(50,50,100,100,True)
Run_Experiment(50,50,100,100,False)
