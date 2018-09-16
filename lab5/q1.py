import numpy as np
import heapq
import math 

def EucldienDist(p1,p2):
	return math.sqrt(pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2))

def manhattanDist(p1,p2):
	return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

class Environment:
	def __init__(self,dim):
		self.dim = dim
		self.mat = np.random.randint(1,size=(dim,dim))
		for i in range (0,dim):
			for j in range (0,dim):
				self.mat[i][j]=0

		maxBumps = np.random.randint(dim)
		for i in range(0,maxBumps):
			bumpPos_i = np.random.randint(dim)
			bumpPos_j = np.random.randint(dim)
			bumpAmt   = np.random.randint(1,dim/2)
			for m in range (0,bumpAmt):
				for n in range(0,bumpAmt):
					x=abs(bumpPos_i-bumpAmt+(m/2))%dim
					y=abs(bumpPos_j-bumpAmt+(n/2))%dim
					self.mat[x][y]=1

	def printMat(self):
		print(self.mat)

	def ispossible(self,currentpos,movement):
		x=currentpos[0]+movement[0]
		y=currentpos[1]+movement[1]
		if x>self.dim or x<0 or y>self.dim or y<0:
			return 0
		if x<self.dim and y<self.dim:
			if self.mat[x][y] == 1:
				return 0
		return 1

	def next(self,currentpos,movement):
		x=currentpos[0]+movement[0]
		y=currentpos[1]+movement[1]
		return (x,y)

class agent:
	def __init__(self,env):
		self.env = env

	def setStartPos(self,pos):
		self.stPos=pos

	def setGoalpos(self,pos):
		self.goalPos = pos

	def Djikstra(self):
		currentpos=self.stPos
		f=self.stPos
		q = [(0,f,())]
		seen = set()
		mins = {f:0}
		movePossibility = [(1,0),(-1,0),(0,1),(0,-1)]
		while q:
			(cost,v1,path) = heapq.heappop(q)
			#print "checking: ",v1 
			if v1 not in seen:
				seen.add(v1)
				path += (v1, )
				
				if v1 == self.goalPos:
					return (cost,path)

				for move in movePossibility:
					isChanged =False
					if env.ispossible(v1,move):
						v2 = env.next(v1,move)
						#print "moving v1 to: ",v2 
						if v2 not in seen:
							isChanged =True
							prev = mins.get(v2,None)
							nxt = cost+1
							if prev is None or nxt < prev:
								mins[v2] = nxt
								#print "pushing to q: ",v2
								heapq.heappush(q,(nxt,v2,path))
								
		return (-1,None)

	def Astar(self,fM=4,type='e'):
		currentpos=self.stPos
		f=self.stPos
		q = [(0,f,())]
		seen = set()
		mins = {f:0}
		if fM==4:
			movePossibility = [(1,0),(-1,0),(0,1),(0,-1)]
		else:
			movePossibility = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
		while q:
			(cost,v1,path) = heapq.heappop(q)
			#print "checking: ",v1 
			if v1 not in seen:
				seen.add(v1)
				#path = (v1,path)
				path += (v1, )
				
				if v1 == self.goalPos:
					return (cost,path)

				for move in movePossibility:
					if env.ispossible(v1,move):
						v2 = env.next(v1,move)
						#print "moving v1 to: ",v2 
						if v2 not in seen:
							prev = mins.get(v2,None)
							if type=='e' or type == 'E':
								next = cost+EucldienDist(v2,self.goalPos)
							if type == 'm' or type =='M':
								next = cost+manhattanDist(v2,self.goalPos)
							if prev is None or next < prev:
								mins[v2] = next
								#print "pushing to q: ",v2
								heapq.heappush(q,(next,v2,path))
		
		return (-1,None)




if __name__ == "__main__":
	env = Environment(30)
	env.printMat()
	agnt = agent(env)
	agnt.setStartPos((0,0))
	agnt.setGoalpos((25,25))
	x=agnt.Astar(8,'e')

	print "length: " ,x[0]
	print "path: ", x[1] , "steps: ",len(x[1])
