import sys
import numpy as np

class Grid(object):
	"""docstring for Grid"""
	def __init__(self,dim):
		self.dim = dim
		self.mat = np.random.rand(dim,dim)
		self.v   = np.random.rand(dim,dim)
		self.probs={}
		self.actions={}
		self.matrange=range(0,dim)
		for i in range (0,dim):
			for j in range (0,dim):
				self.mat[i][j]=round(self.mat[i][j],2)

		moves = [(0,0),(1,0),(0,1),(-1,0),(0,-1)]

		for i in range(0,dim):
			for j in range(0,dim):
				self.actions[(i,j)]=[]
				self.probs[(i,j)]  =[]

		for move in moves:
			for i in range(0,dim):
				for j in range(0,dim):
					condition = i+move[0]>=0 and i+move[0]<self.dim
					condition = condition and j+move[1]>=0 and j+move[1]<self.dim
					if condition:						
						self.actions[(i,j)].append(move)
						self.probs[(i,j)].append(np.random.rand())

		for i in range(0,dim):
			for j in range(0,dim):
				avg=0
				for p in self.probs[(i,j)]:
					avg=avg+p
				avg=avg/len(self.probs[(i,j)])
				for k in range(0,len(self.probs[(i,j)])):
					self.probs[(i,j)][k]=self.probs[(i,j)][k]/avg

		self.states = [ (x/dim,x%dim) for x in range(0,dim*dim) ]

	
	def setUpRewards(self,stnum,acnum):
		rwar =  np.random.choice(range(self.dim*self.dim),stnum)
		self.rewardStates = [(x/self.dim,x%self.dim) for x in rwar]
		self.rewards={}
		for states in self.rewardStates:
			for action in self.actions[states]:
				if np.random.randint(0,acnum) == 1:
					self.rewards[(states,action)] = np.random.randint(10,20)


	def calcV(self,x,y,alpha):
		for i in self.matrange:
			for j in self.matrange:
				Q=[]
				for k in len(self.actions[(i,j)]):
					Q.append(0.0)



if __name__ == "__main__":
	np.random.seed(10)
	grd = Grid(4)
	print grd.mat
	grd.setUpRewards(3,2)
	sys.exit(0)