class Robot:
	def __init__(self):
		self.pos=[0,0]

	def PerceptAndMove(self,env):
		if(env.isAtDirt(pos)==1):
			return 1

class Environment:
	def __init__(self,dirtPos,robotPos):
		self.dirtPos=dirtPos
		self.robotPos=robotPos

	def isRobotAtDirt(self):
		if(dirtPos==robotPos):
			return 1
		else:
			return 0

	def moveRobot(offset):
		robotPos[0]=robotPos[0]+offset[0]
		robotPos[1]=robotPos[1]+offset[1]


if __name__=="__main__":
	r=Robot()
	e=Environment([10,15],[1,-1])