from __future__ import print_function
import sys
import numpy as np
import copy
import heapq as pq
from time import sleep

# x will be a truth value of an evaluated boolean expression
def indicator(x):
	if(x):
		return 1
	else:
		return 0

#this is used to calculate the element at array position i if the matrix was treated as an array
def arrToMatPos(i,mat,dim):
	return mat[i/dim][i%dim]

#this is used to calcualte the actual position of num in an matrix of dimension dim. ie, it's position when the puzzle is solved
def matToArr(num,dim):
	return (num-1)/dim,(num-1)%dim

#this is the environment class this contains the matrix and related functions
class Environment:
	#initialisation self explanatory
	def __init__(self,mat,dim):
		self.mat=mat
		self.dim = dim
		self.arrlen = (self.dim)*(self.dim)
		self.emptyItem = (self.dim)*(self.dim)
		self.emptyItem2 = self.emptyItem - 1


	def printMat(self):
		#print self.mat,"h:",self.heuristic()

		for i in range(0,self.dim):
			for j in range(0,self.dim):
				if self.mat[i][j] == self.dim*self.dim:
					print('b',end=" ")
				elif self.mat[i][j] == self.dim*self.dim -1:
					print('w',end=" ")
				elif self.mat[i][j] == self.dim:
					print('R',end=" ")
				else:
					print('b',end=" ")
			print('\n',end="")

		'''for i in range(0,self.dim):
			print self.mat[i]'''

		print( "h:",self.heuristic())

	#the environment tracks the position of both empty cells (this is used for it's calculation)
	def calcEmptyPos(self):
		e1o=0
		e2o=0
		for i in range (0,self.dim):
			for j in range(0,self.dim):
				if self.mat[i][j]== self.emptyItem:
					self.emptyX1 = i
					self.emptyY1 = j
					e1o=e1o+1
				if self.mat[i][j] == self.emptyItem2:
					self.emptyX2 = i
					self.emptyY2 = j
					e2o=e2o+1

		#in case due to shallow copy problem two elements of the same value is created 
		if e1o>1 or e2o>1:
			print ("wrong mat")
			sys.exit(0)

	#this is used to move the empty 1 ie n squared
	def moveEmpty1(self,dirn):
		return 0
		#retreiving the e1 position from environment
		ex1 = self.emptyX1
		ey1 = self.emptyY1

		#checking whether the motion of empty is within the bounds of the matrix
		#returns 0 to the called agent so that it can discard this movement
		if (ex1+dirn[0] >= self.dim or ey1+dirn[1] >= self.dim or  ex1+dirn[0]<0 or ey1+dirn[1]<0 ):
			return 0

		#swaping to empty ellements is also allowed. but it is fine as the heuristic takes care of redundancy
		if self.mat[ex1+dirn[0]][ey1+dirn[1]] == self.emptyItem2:
			self.emptyX2=ex1
			self.emptyY2=ey1

		#swaping elements
		self.mat[ex1][ey1] = self.mat[ex1+dirn[0]][ey1+dirn[1]]
		self.mat[ex1+dirn[0]][ey1+dirn[1]] = self.emptyItem

		self.emptyX1=ex1+dirn[0]
		self.emptyY1=ey1+dirn[1]
		#making sure that the empty positions are updated after swap
		self.calcEmptyPos()
		return 1

	#similiar to above but for moving n square minus 1
	def moveEmpty2(self,dirn):
		ex2 = self.emptyX2
		ey2 = self.emptyY2

		if (ex2+dirn[0] >= self.dim or ey2+dirn[1] >= self.dim or  ex2+dirn[0]<0 or ey2+dirn[1]<0 ):
			return 0

		if self.mat[ex2+dirn[0]][ey2+dirn[1]] == self.emptyItem:
			self.emptyX=ex2
			self.emptyY=ey2

		self.mat[ex2][ey2] = self.mat[ex2+dirn[0]][ey2+dirn[1]]
		self.mat[ex2+dirn[0]][ey2+dirn[1]] = self.emptyItem2

		self.emptyX2=ex2+dirn[0]
		self.emptyY2=ey2+dirn[1]
		self.calcEmptyPos()
		return 1

	#to calculate parity according to the function given in the pdf
	def clacParity(self):

		self.calcEmptyPos()

		parity = (2 - self.emptyX1) + (2 - self.emptyY1)
		for i in range (0,self.arrlen):
			for j in range(i+1,self.arrlen):
				pi = arrToMatPos(i,self.mat,self.dim)
				pj = arrToMatPos(j,self.mat,self.dim)
				parity = parity + indicator((pj<pi))

		parity = parity%2
		self.currentParity = parity
		print("current parity : " , parity)

	#this determines whether the puzzle have actually reached it's goal.
	#this can also be calculated using heuristic
	def isGoal(self):

		if self.mat[0][self.dim-1] == self.dim:
			return 1
		else:
			return 0

		for i in range(0,self.dim):
			for j in range(0,self.dim):
				if self.mat[i][j] != (i)*self.dim+j+1:
					return 0
		return 1

	#there are three types of heuristics designed but for the problem the manhattan distance is used (type 3)
	def heuristic(self,type=3):
		v1 = 0
		for i in range(self.dim):
			for j in range(self.dim):
				if self.mat[i][j] == self.dim:
					v1 = abs(i)+abs(j-(self.dim-1))
					I=i
					J=j
					return v1
					break;break

		'''for i in range(self.dim):
			for j in range(self.dim):
				if self.mat[i][j] == (self.dim)**2:
					v1 += min(abs(i-I+1),abs(i-I-1))
					v1 += min(abs(j-J+1),abs(j-J-1))
					return v1'''





		#misplaced penalty, heuristic
		if type==1:
			h=(self.dim)*(self.dim)
			for i in range(0,self.dim):
				for j in range(0,self.dim):
					if self.mat[i][j] == (i)*self.dim+j+1:
						h=h-1

		#linear distance to goal, heuristic
		if type==2:
			h=0
			for i in range(0,self.dim):
				for j in range(0,self.dim):
					if self.mat[i][j] == self.emptyItem or self.mat[i][j] == self.emptyItem2:
						val = self.mat[i][j]
						adder = min(abs((i*self.dim+j+1)-self.emptyItem),abs((i*self.dim+j+1)-self.emptyItem2))
					else:
						adder=abs(self.mat[i][j]-(i*self.dim+j+1))

					h=h+adder

		#manhattan distance to goal, heuristic
		if type==3:
			h=0
			#for each element
			for i in range(0,self.dim):
				for j in range(0,self.dim):
					#the element at i j
					val = self.mat[i][j]
					#it's actual position in solved matrix
					xi,xj=matToArr(val,self.dim)

					#in case the element is an empty item
					if val == self.emptyItem or val == self.emptyItem2:
						#the minimum manhattan distance to it's end position as the empty cells are not distinguishable
						xi1,xj1=matToArr(self.emptyItem,self.dim)
						xi2,xj2=matToArr(self.emptyItem2,self.dim)
						adder1 = abs(i-xi1)+abs(j-xj1)
						adder2 = abs(i-xi2)+abs(j-xj2)
						h=h+min(adder1,adder2)

					#otherwise just calculate the manhattan distance of the element to it's true position
					else:
						adder = abs(i-xi)+abs(j-xj)
						h=h+adder
		return h
#to check whether the given to environment share equal matrices
def eq(mat1,mat2,dim):
	for i in range(0,dim):
		for j in range(0,dim):
			if mat1.mat[i][j] != mat2.mat[i][j]:
				return 0
	return 1
#same as above
def EQ(mat1,mat2):
	return np.array_equal(mat1.mat,mat2.mat)
#not used in this question please see a star implementation below
def BFS(env):
	envQ=[]
	visited = []
	envQ.append(env)

	boolCont= 0
	currentNodeEnv = env

	while not currentNodeEnv.isGoal():

		currentNodeEnv=envQ.pop(0)
		print("=======poping=======")
		currentNodeEnv.printMat()
		print("====================")
		if currentNodeEnv.isGoal():
			print ("found answer")
			break;

		boolCont=0
		for node in visited:
			if EQ(node,currentNodeEnv):
				boolCont = 1
				break

		if boolCont:
			continue

		if currentNodeEnv.moveEmpty1((0,1)):
			print("e1 move left")
			currentNodeEnv.printMat()
			envQ.append(copy.deepcopy(currentNodeEnv))
			currentNodeEnv.moveEmpty1((0,-1))

		if currentNodeEnv.moveEmpty1((0,-1)):
			print("e1 move right")
			currentNodeEnv.printMat()
			envQ.append(copy.deepcopy(currentNodeEnv))
			currentNodeEnv.moveEmpty1((0,1))

		if currentNodeEnv.moveEmpty1((1,0)):
			print("e1 move down")
			currentNodeEnv.printMat()
			envQ.append(copy.deepcopy(currentNodeEnv))
			currentNodeEnv.moveEmpty1((-1,0))

		if currentNodeEnv.moveEmpty1((-1,0)):
			print("e1 move up")
			currentNodeEnv.printMat()
			envQ.append(copy.deepcopy(currentNodeEnv))
			currentNodeEnv.moveEmpty1((1,0))

		#empty 2 movement
		if currentNodeEnv.moveEmpty2((0,1)):
			print("e2 move left")
			currentNodeEnv.printMat()
			envQ.append(copy.deepcopy(currentNodeEnv))
			currentNodeEnv.moveEmpty2((0,-1))

		if currentNodeEnv.moveEmpty2((0,-1)):
			print("e2 move right")
			currentNodeEnv.printMat()
			envQ.append(copy.deepcopy(currentNodeEnv))
			currentNodeEnv.moveEmpty2((0,1))

		if currentNodeEnv.moveEmpty2((1,0)):
			print("e2 move down")
			currentNodeEnv.printMat()
			envQ.append(copy.deepcopy(currentNodeEnv))
			currentNodeEnv.moveEmpty2((-1,0))

		if currentNodeEnv.moveEmpty2((-1,0)):
			print("e2 move up")
			currentNodeEnv.printMat()
			envQ.append(copy.deepcopy(currentNodeEnv))
			currentNodeEnv.moveEmpty2((1,0))

		visited.append(copy.deepcopy(currentNodeEnv))


def Astar(env):
	#envQ correspons to the priority queue storing the matrices
	path=[]
	steps=0
	envQ=[]
	visited = []
	pq.heappush(envQ, ( env.heuristic() , steps,path , env ) )

	boolCont= 0
	currentNodeEnv = env

	while not currentNodeEnv.isGoal():

		#poping the one with least f
		f,st,path,currentNodeEnv=pq.heappop(envQ)
		print ("=======poping=======")
		currentNodeEnv.printMat()
		print ("====================",f)
		#sleep(0.5)
		if currentNodeEnv.isGoal() or currentNodeEnv.heuristic()==0:
			print ("found answer; steps:",st)
			#print "path is:",path
			break;

		#if the poped matrix is in visited then we skips the loop
		boolCont=0
		for node in visited:
			if eq(node,currentNodeEnv,node.dim):
				boolCont = 1
				print ("visited!!")
				break

		if boolCont:
			continue

		st=st+1
		#all possible movements of e1
		if currentNodeEnv.moveEmpty1((0,1)):
			#if the motion is possible then add it to queue
			print("e1 move left")
			currentNodeEnv.printMat()
			#adding a copy to the queue to avoid shallow copy problem
			z= copy.deepcopy(currentNodeEnv)
			path.append("e1l")
			pq.heappush(envQ,(z.heuristic(),st,path,z))
			#revert back it's motion so that it can be used later
			currentNodeEnv.moveEmpty1((0,-1))

		#see above
		if currentNodeEnv.moveEmpty1((0,-1)):
			print("e1 move right")
			currentNodeEnv.printMat()
			z= copy.deepcopy(currentNodeEnv)
			path.append("e1r")
			pq.heappush(envQ,(z.heuristic(),st,path,z))
			currentNodeEnv.moveEmpty1((0,1))

		if currentNodeEnv.moveEmpty1((1,0)):
			print("e1 move down")
			currentNodeEnv.printMat()
			z= copy.deepcopy(currentNodeEnv)
			path.append("e1d")
			pq.heappush(envQ,(z.heuristic(),st,path,z))
			currentNodeEnv.moveEmpty1((-1,0))

		if currentNodeEnv.moveEmpty1((-1,0)):
			print("e1 move up")
			currentNodeEnv.printMat()
			z= copy.deepcopy(currentNodeEnv)
			path.append("e1u")
			pq.heappush(envQ,(z.heuristic(),st,path,z))
			currentNodeEnv.moveEmpty1((1,0))

		#empty 2 movement see aboce comments

		if currentNodeEnv.moveEmpty2((0,1)):
			print("e2 move left")
			currentNodeEnv.printMat()
			z= copy.deepcopy(currentNodeEnv)
			path.append("e2l")
			pq.heappush(envQ,(z.heuristic(),st,path,z))
			currentNodeEnv.moveEmpty2((0,-1))

		if currentNodeEnv.moveEmpty2((0,-1)):
			print("e2 move right")
			currentNodeEnv.printMat()
			z= copy.deepcopy(currentNodeEnv)
			path.append("e2r")
			pq.heappush(envQ,(z.heuristic(),st,path,z))
			currentNodeEnv.moveEmpty2((0,1))

		if currentNodeEnv.moveEmpty2((1,0)):
			print("e2 move down")
			currentNodeEnv.printMat()
			z= copy.deepcopy(currentNodeEnv)
			path.append("e2d")
			pq.heappush(envQ,(z.heuristic(),st,path,z))
			currentNodeEnv.moveEmpty2((-1,0))

		if currentNodeEnv.moveEmpty2((-1,0)):
			print("e2 move up")
			currentNodeEnv.printMat()
			z= copy.deepcopy(currentNodeEnv)
			path.append("e2u")
			pq.heappush(envQ,(z.heuristic(),st,path,z))
			currentNodeEnv.moveEmpty2((1,0))

		#adding to the visited array
		visited.append(copy.deepcopy(currentNodeEnv))	

if __name__ == "__main__":

	#run using pthon q1.py <ip.txt
	#or using 'make' (type 'make' in terminal)

	print ("commencing program" )

	print ("loading matrix...." )

	dimension=int(raw_input("enter the dimension:"))

	matrix = []
	for i in range(0,dimension):
		line = [int(x) for x in raw_input().split()]
		matrix.append(line)

	#matrix = np.loadtxt("new.txt")
	print (matrix)
	env = Environment(matrix,dimension)

	env.clacParity()

	Astar(env)

	env.printMat()
		

	sys.exit(0)