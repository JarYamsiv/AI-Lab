import random
import sys


#THE BUNNY CLASS
class bunny:
	def __init__(self):
		self.Pos=0
		self.state=1
		self.vx=0
	def motion(self,env):
		if env.bunnyPlace()==1:
			#the bunny is at the shore
			self.state=0
			print("shore found")
			sys.exit(0)
		else:
			self.vx=random.randint(0,1);
			if self.vx==0:
				print("move right")
				self.Pos=self.Pos+1
				env.moveBunny(1)
			else:
				print("move left")
				self.Pos=self.Pos-1
				env.moveBunny(-1)

	def bunnyState(self):
		return self.bunnyState





#THE ENVIRONMENT CLASS
class Environment:
	def __init__(self,shorePosition,bunnyPosi):
		self.shorePositions=shorePosition
		self.bunnyPos=bunnyPosi

	def bunnyPlace(self):
		for i in self.shorePositions:
			if(self.bunnyPos==i):
				return 1
		return 0

	def moveBunny(self,offset):
		self.bunnyPos=self.bunnyPos+offset
		print("current bunny pos in environment:",self.bunnyPos)



if __name__=="__main__":
	b = bunny()
	e = Environment([-100,100],5)
	print("classes initialized")
	while(e.bunnyPlace()!=1):
		b.motion(e)
		if(e.bunnyPlace()==1):
			print("shore found")
			sys.exit(0);
			break;

	print("shore found")
	sys.exit(0);

