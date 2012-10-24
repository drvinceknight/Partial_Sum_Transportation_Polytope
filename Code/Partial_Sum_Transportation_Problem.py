"""
Code to define a transportation problem and a partial sum transportation problem
"""
from __future__ import division
from openopt import NLP,LP
from numpy import *

class Problem():
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
            for r in Aeq[:self.m]:
               index=range(k,k+self.n)
               for j in index:
                   r[j]=1
               k+=self.n
            k=0
            for r in Aeq[self.m:]:
               index=[k+j*self.n for j in range(self.m)]
               for j in index:
                   r[j]=1
               k+=1
            self.Aeq=mat(Aeq)
        else:
            print "Invalid problem"

    def row_sum(self,matrix):
        r=[0 for i in range(self.m)]
        k=0
        for e in matrix:
            r[k/self.n]+=e
            k+=1
        return r

    def col_sum(self,matrix):
        r=[0 for i in range(self.n)]
        k=0
        for e in matrix:
            r[k%self.n]+=e
            k+=1
        return r

class Transportation_Problem(Problem):
    def __init__(self,r,s,cost_matrix):
        Problem.__init__(self,r,s,cost_matrix)
        self.cost_function=array(cost_matrix)
        self.lb=[0 for k in range(self.m*self.n)]
    def evaluate(self,matrix):
        return self.cost_function(matrix)
    def solve(self):
        p=LP(self.cost_function,Aeq=self.Aeq,beq=self.beq,lb=self.lb)
        r=p.solve('pclp')
        return [r.xf,r.ff]

class Partial_Sum_Transportation_Problem(Problem):
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
        r=p.solve('ralg')
        return [r.xf,r.ff]

class Solution_Comparison():
    def __init__(self,r,s,c):
        self.Transportation_Solution=Transportation_Problem(r,s,c).solve()
        self.Partial_Sum_Transportation_Solution=Partial_Sum_Transportation_Problem(r,s,c).solve()
    def Costs(self):
        return [self.Transportation_Solution[1],self.Partial_Sum_Transportation_Solution[1]]
    def Solutions(self):
        return [self.Transportation_Solution[0],self.Partial_Sum_Transportation_Solution[0]]
    def Partial_Sum_Optimal(self,precision=2):
        Partial_Sum_Solution=[round(e,precision) for e in self.Partial_Sum_Transportation_Solution[0]]
        return min(Partial_Sum_Solution)<0

print "----"
c=[100,1,1,100,100,1,1,1,100,1,1,10,1,10,1,1,1,10,1,10,10,1,10,1,100,1,1,100]
r=[3,2,1,6,1,1,1]
s=[6,2,1,6]

a=Solution_Comparison(r,s,c)
print a.Costs()
print a.Partial_Sum_Optimal()

