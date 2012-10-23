"""
Code to define a transportation problem and a partial sum transportation problem
"""

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
            self.Aeq=Aeq
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
        self.Aeq=mat(self.Aeq)
    def evaluate(self,matrix):
        return self.cost_function(matrix)
    def solve(self):
        p=LP(self.cost_function,Aeq=self.Aeq,beq=self.beq,lb=self.lb)
        r=p.solve('pclp')
        return r.xf,r.ff
#print ""
#print "--- Testing ---"
#print ""


#f = array([15,8,80])
#A = mat('1 2 3; 8 15 80; 8 80 15; -100 -10 -1') # numpy.ndarray is also allowed
#b = [15, 80, 150, -800] # numpy.ndarray, matrix etc are also allowed
#Aeq = mat('80 8 15; 1 10 100') # numpy.ndarray is also allowed
#beq = (750, 80)

#lb = [4, -80, -inf]
#ub = [inf, -8, inf]
#p = LP(f, A=A, Aeq=Aeq, b=b, beq=beq, lb=lb, ub=ub)
#or p = LP(f=f, A=A, Aeq=Aeq, b=b, beq=beq, lb=lb, ub=ub)

#r = p.minimize('glpk') # CVXOPT must be installed
#r = p.minimize('lpSolve') # lpsolve must be installed
#r = p.minimize('pclp')
#search for max: r = p.maximize('glpk') # CVXOPT & glpk must be installed
#r = p.minimize('nlp:ralg', ftol=1e-7, xtol=1e-7, goal='min', plot=1)

#print('objFunValue: %f' % r.ff) # should print 204.48841578
#print('x_opt: %s' % r.xf) # should print [ 9.89355041 -8.



#print""
#print "---- Test 2 ---"
#print""
#Aeq=mat([[1,1,0,0],[0,0,1,1],[1,0,1,0],[0,1,0,1]])
#beq=array([1,1,1,1])
#f=array([1,1,3,1])
#lb=[0,0,0,0]
#ub=[1,1,1,1]
#p=LP(f,beq=beq,Aeq=Aeq,lb=lb,ub=ub)
#r=p.minimize('pclp')
#print('objFunValue: %f' % r.ff) # should print 204.48841578
#print('x_opt: %s' % r.xf) # should print [ 9.89355041 -8.






print "----"
test=Transportation_Problem([1,1],[1,1],[1,1,3,1])
print test.solve()
test=Transportation_Problem([1,1,1],[1,2],[1,2,3,4,5,6])
print test.solve()
test=Transportation_Problem([1,1,3,1],[1,2,2,1],[1,2,3,4,5,6,1,2,3,4,5,6,4,3,2,1])
print test.solve()

#class Partial_Sum_Transportation_Problem(self,cost_matrix):


