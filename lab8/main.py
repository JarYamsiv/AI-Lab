import sys
import numpy as np
import copy

def isPossible(st,ac,dim):
	sd = tuple(map(lambda x, y: x + y, st, ac))
	condition = True
	condition = condition and sd[0]>=0 and sd[0]<dim
	condition = condition and sd[1]>=0 and sd[1]<dim
	return condition

class Grid(object):
	"""docstring for Grid"""
	def __init__(self,dim):
		self.dim = dim
		self.mat = np.random.rand(dim,dim)
		self.v   = np.random.rand(dim,dim)
		self.pi  = {}
		self.probs={}
		self.probs2={}
		self.actions={}
		self.matrange=range(0,dim)
		self.eact={
			(0,0):"stay",
			(1,0):"down",
			(-1,0):"up",
			(0,1):"right",
			(0,-1):"left",
			}
		for i in range (0,dim):
			for j in range (0,dim):
				self.mat[i][j]=round(self.mat[i][j],2)
				self.v[i][j] = round(self.v[i][j],5)

		moves = [(1,0),(0,1),(-1,0),(0,-1)]

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
				print "actions of ",(i,j),":",[self.eact[x] for x in self.actions[(i,j)]]
				avg=0
				for p in self.probs[(i,j)]:
					avg=avg+p
				for k in range(0,len(self.probs[(i,j)])):
					self.probs[(i,j)][k]=self.probs[(i,j)][k]/avg
					print "prob(",i,j,self.eact[self.actions[(i,j)][k]],") = ",self.probs[(i,j)][k]

		self.states = [ (x/dim,x%dim) for x in range(0,dim*dim) ]

	
	def setUpRewards(self,stnum,acnum):
		rwar =  np.random.choice(range(self.dim*self.dim),stnum)
		print "chosen numbers =" , rwar
		self.rewardStates = [(x/self.dim,x%self.dim) for x in rwar]
		print "chosen states =" , self.rewardStates
		self.rewards={((2,2),(0,-1)):53}
		for states in self.rewardStates:
			for action in self.actions[states]:
				if np.random.randint(0,acnum) == 1:
					self.rewards[(states,action)] = np.random.randint(10,20)
					print "reward " , states , "ac ", self.eact[action] , " = " , self.rewards[(states,action)]

	def setUpRewardsFull(self,stnum,acnum):
		rwar =  np.random.choice(range(self.dim*self.dim),stnum)
		print "chosen numbers =" , rwar
		self.rewardStates = [(x/self.dim,x%self.dim) for x in rwar]
		print "chosen states =" , self.rewardStates
		self.rewards={((2,2),(0,-1)):53}
		for states in self.states:
			for action in self.actions[states]:
				if True:
					self.rewards[(states,action)] = np.random.randint(-10,20)
					print "reward " , states , "ac ", self.eact[action] , " = " , self.rewards[(states,action)]

	def calcV(self,itr,alpha,gamma=0.3):
		diff = False
		for i in self.matrange:
			for j in self.matrange:
				Q=[]
				print "state:",(i,j),"itr:",itr
				for k in range(len(self.actions[(i,j)])):
					st = (i,j)
					ac = self.actions[(i,j)][k]
					pb = self.probs[(i,j)][k]

					new_v = self.rewards.get((st,ac),0.0)

					pr_sum = 0.0
					for l in range(len(self.actions[(i,j)])):

						state_dash = tuple(map(lambda x, y: x + y, (i,j), self.actions[(i,j)][l]))
						print "\t\tsd=",state_dash,"v(sd)=",self.v[state_dash[0]][state_dash[1]]

						pr_sum = pr_sum + self.probs[(i,j)][l]*self.v[state_dash[0]][state_dash[1]]


					new_v = new_v + gamma*pr_sum
					print "\t action:",ac,"rwd:",self.rewards.get((st,ac),0.0),"new_v:",new_v,"old:",self.v[i][j]
					Q.append(new_v)
				diff = diff or (abs (self.v[i][j]-max(Q)))>alpha
				self.v[i][j] = max(Q)
				print Q," arg=",np.argmax(Q)
				self.pi[(i,j)] = self.actions[(i,j)][np.argmax(Q)]
		return diff



if __name__ == "__main__":
	np.random.seed(10)
	grd = Grid(4)
	print grd.v
	grd.setUpRewards(5,2)

	print " "
	diff = True
	itr = 1
	while diff:
		diff = grd.calcV(itr,0.0001)
		print grd.v
		print "after iteration:",itr
		print " "
		itr = itr+1

	act_mat=[]
	act_mat_line=[]
	for i in range(4):
		act_mat_line=[]
		for j in range(4):
			#print "state:",(i,j),"action",grd.eact[grd.pi[(i,j)]]
			act_mat_line.append(grd.eact[grd.pi[(i,j)]])
		act_mat.append(copy.deepcopy(act_mat_line))
		print act_mat_line

	print grd.rewards

	sys.exit(0)