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
					print "reward " , states , "ac ", action , " = " , self.rewards[(states,action)]


	def calcV(self,itr,alpha,gamma=0.02):
		diff = False
		for i in self.matrange:
			for j in self.matrange:
				Q=[]
				#print "state:",(i,j),"itr:",itr
				for k in range(len(self.actions[(i,j)])):
					st = (i,j)
					ac = self.actions[(i,j)][k]
					pb = self.probs[(i,j)][k]

					new_v = self.rewards.get((st,ac),0.0)

					pr_sum = 0.0
					for l in range(len(self.actions[(i,j)])):

						state_dash = tuple(map(lambda x, y: x + y, (i,j), self.actions[(i,j)][l]))

						pr_sum = pr_sum + self.probs[(i,j)][l]*self.v[state_dash[0]][state_dash[1]]


					new_v = new_v + gamma*pr_sum
					#print "\t action:",ac,"rwd:",self.rewards.get((st,ac),0.0),"new_v:",new_v,"old:",self.v[i][j]
					Q.append(new_v)
				diff = diff or (self.v[i][j]-max(Q))>alpha
				self.v[i][j] = max(Q)
		return diff



if __name__ == "__main__":
	np.random.seed(10)
	grd = Grid(4)
	print grd.v
	grd.setUpRewards(3,2)

	print " "
	diff = True
	itr = 1
	while diff:
		diff=False
		diff = grd.calcV(itr,0.00000001)
		print grd.v
		print "after iteration:",itr
		print " "
		itr = itr+1

	sys.exit(0)