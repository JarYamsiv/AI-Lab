import sys
import numpy as np

# x will be a truth value of an evaluated boolean expression
def indicator(x):
	if(x):
		return 1
	else:
		return 0

def arrToMatPos(i,mat,dim):
	return mat.item((i/dim,i%dim))

class Environment:
	def __init__(self,mat):
		self.mat=mat
		self.dim = (mat.shape)[0]
		self.arrlen = (self.dim)*(self.dim)
		self.emptyItem = (self.dim)*(self.dim)


	def printMat(self):
		print(self.mat)

	def calcEmptyPos(self):
		for i in range (0,self.dim):
			for j in range(0,self.dim):
				if self.mat.item((i,j))== self.emptyItem:
					self.emptyX = i
					self.emptyY = j
					return

	def moveEmpty(self,dirn):
		ex = self.emptyX
		ey = self.emptyY

		if not (ex+dirn[0] < self.dim and ey+dirn[1] < self.dim):
			return 0

		self.mat[ex][ey] = self.mat[ex+dirn[0]][ey+dirn[1]]
		self.mat[ex+dirn[0]][ey+dirn[1]] = self.emptyItem

		self.emptyX=ex+dirn[0]
		self.emptyY=ey+dirn[1]
		return 1

	def clacParity(self):

		self.calcEmptyPos()

		parity = (2 - self.emptyX) + (2 - self.emptyY)
		for i in range (0,self.arrlen):
			for j in range(i+1,self.arrlen):
				pi = arrToMatPos(i,self.mat,self.dim)
				pj = arrToMatPos(j,self.mat,self.dim)
				parity = parity + indicator((pj<pi))

		parity = parity%2
		self.currentParity = parity
		print("current parity : " , parity)

	def isGoal(self):
		for i in (0,self.dim):
			for j in (0,self.dim):
				if self.mat.item((i,j)) != (i*self.dim+j):
					return 0
		return 1

	def equality(self,matrix):
		for i in (0,self.dim):
			for j in (0,self.dim):
				if self.mat.item((i,j)) != i*self.dim+j:
					return 0
		return 1

	def copy(self):
		copy = self
		return copy

def EQ(mat1,mat2):
	return np.array_equal(mat1.mat,mat2.mat)


if __name__ == "__main__":
	print("commencing program")

	print("loading matrix....")
	matrix = np.loadtxt("testMat.txt")
	env = Environment(matrix)
	#env.printMat()
	env.clacParity()

	#print(env.isGoal())

	print("========================some test==============================")
	tst = Environment(matrix)
	tstL = []
	tstL.append(tst)
	tst.clacParity()
	tst.moveEmpty((1,1))
	tstL.append(tst.copy())
	k = tstL.pop()
	k.printMat()
	k = tstL.pop()
	k.printMat()
	print("===============================================================")

	envQ=[]
	visited = []
	envQ.append(env)

	boolCont= 0
	currentNodeEnv = env

	while not currentNodeEnv.isGoal():

		currentNodeEnv=envQ.pop()
		print("=======poping=======")
		currentNodeEnv.printMat()
		print("====================")

		boolCont=0
		for node in visited:
			if EQ(node,currentNodeEnv):
				boolCont = 1
				break

		if boolCont:
			continue

		if currentNodeEnv.moveEmpty((0,1)):
			print("move left")
			currentNodeEnv.printMat()
			envQ.append(currentNodeEnv)
			currentNodeEnv.moveEmpty((0,-1))

		if currentNodeEnv.moveEmpty((0,-1)):
			print("move right")
			currentNodeEnv.printMat()
			envQ.append(currentNodeEnv)
			currentNodeEnv.moveEmpty((0,1))

		if currentNodeEnv.moveEmpty((1,0)):
			print("move down")
			currentNodeEnv.printMat()
			envQ.append(currentNodeEnv)
			currentNodeEnv.moveEmpty((-1,0))

		if currentNodeEnv.moveEmpty((-1,0)):
			print("move up")
			currentNodeEnv.printMat()
			envQ.append(currentNodeEnv)
			currentNodeEnv.moveEmpty((1,0))

		visited.append(currentNodeEnv)
		

	sys.exit(0)