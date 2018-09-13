import sys
import numpy as np

#####################################
# agent class:
# agent can percept the environment to decided whether it has reached 
# the goal or not.  based on this information it makes a random move
# possible six direcions which are selected by first choosing the direction
# and then choosing whether it should move by 1 or -1
#####################################
class agent:
	def __init__(self,pos):
		#initialising the agent position from outside the class
		self.pos=pos

	def randMove(self):
		#this method is not used as this has 8 directions of freedom to move
		pos=self.pos
		moveDirn=np.array([1,-1])
		vx=np.random.choice(moveDirn,1)[0]
		vy=np.random.choice(moveDirn,1)[0]
		vz=np.random.choice(moveDirn,1)[0]
		L=self.L
		willMove = pos[0]+vx<=L and pos[0]+vx>=0
		willMove = willMove and pos[1]+vy<=L and pos[1]+vy>=0
		willMove = willMove and pos[2]+vz<=L and pos[2]+vz>=0

		if(willMove):
			pos = (  pos[0]+vx,  pos[1]+vy,  pos[2]+vz)
			self.pos=pos
			print("moved to ",self.pos)

	def randMoveSingle(self):
		#here there are only 6 available directions to move
		#moveDirn defines the dimensions
		moveDirn=np.array([0,1,2])
		#moveAmount defines the amount it should move in the selected direction 
		moveAmount=np.array([1,-1])

		#choose both direction and amount randomly
		v=np.random.choice(moveDirn,1)[0]
		dv=np.random.choice(moveAmount,1)[0]

		#calculating the new position
		nextPos=list(self.pos)
		nextPos[v]=nextPos[v]+dv
		if nextPos[v]<=self.L and nextPos[v]>=0:
			#moves the agent only if it doesn't cross the boundry after it's motion
			self.pos=(nextPos[0],nextPos[1],nextPos[2])
			print("moved  to : ",self.pos)


	def addEnv(self,env):
		#to add a reference of the environment to the agent so that it can be used to percet whether agent 
		#has reached the goal ro not
		self.environment=env
		self.L=env.L


class environment:
	def __init__(self,L,goalpos):
		self.goalPos=goalpos
		self.L=L

	def addAgent(self,agent):
		self.agent=agent

	def isReached(self):
		if self.agent.pos == self.goalPos:
			return 1
		else:
			return 0

if __name__ == "__main__":
	print("starting programme")

	L=10

	a = agent((L/2,L/2,L/2))

	env = environment(L,(L,L,L))

	a.addEnv(env)

	env.addAgent(a)

	steps=0
	while not env.isReached():
		a.randMoveSingle()
		steps=steps+1

	print("number of steps :",steps)

	sys.exit(0)