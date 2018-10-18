import sys
import numpy as np

POS_MAX = 0.6
POS_MIN = -1.2
VEL_MAX = 0.07
VEL_MIN = -0.07
POSITIONS = 181
VELOCITIES = 141

def pstate(val):
	"""
		the output will be 0 to 180 and
		the input is a position from -1.2 to 0.6
	"""
	return int((val+1.2)*100)

def posi(state):
	"""
		the input is a state ranging from 0 to 180
		and returns the corresponding position
	"""
	return (state/100.0)-1.2

def vstate(val):
	return int((val+0.07)*1000)

def velo(state):
	return ((state/1000.0)-0.07)

def prob(sp,sv,sdp,sdv,act):
	pass

def newStateCalc(cp,cv,act):
	"""
		cp  = current position in state form (ie 0-180)
		cv = current velocity in state form (ie 0-140)
		act = action taken
	"""
	pos = posi(cp)
	vel = velo(cv)
	new_vel = round(vel + act*0.001 + np.cos(3*pos)*(-0.0025),2)
	new_pos = round(pos + new_vel,1)
	pnew = pstate(new_pos)
	vnew = vstate(new_vel)
	return pnew,vnew

def stateValidity(pos,vel):
	condition = 0 <= pos and pos<POSITIONS
	condition = condition and 0 <= vel and vel <VELOCITIES
	return condition




		

class Car:
	"""
	|-----------------------------------------------------------
	|	Description:
	|	starting state anywhere between -0.4 to -0.6
	|	position : -1.2 to 0.6
	|	velocity : (-0.07) to (0.07)
	|	finishes when p>=0.55 or when t>200
	|	decretise position with 0.01 ie,180 states
	|	descretise velocity with 0.001 ie,140 states
	|	ie total 180x140 states
	|	probability is 1.0 if it takes the accurate state transition, 0.0 otherwise
	|	pos = pos + vel
	|	vel = vel + act*0.001 + cos(3*p)*(-0.0025)
	|-----------------------------------------------------------
	"""
	def __init__(self):

		self.position=-0.5
		self.numpos = POSITIONS
		self.numvel = VELOCITIES
		self.numstates = self.numpos*self.numvel
		self.velocity=0.0
		self.V = np.zeros((self.numpos,self.numvel)) # V[position_state][velocity_state] = 0.0	
		self.actions=[-1,0,1]
		self.policy=np.zeros((self.numpos*self.numvel))
		self.gamma = 0.75	
		self.alpha = 0.0001

	def valueIteration(self):
		converged = False
		itr = 0
		while not converged:
			converged = True
			for p in range(self.numpos):
				for v in range(self.numvel):
					"""equivlent to for s in states"""
					print "from state" , p ,v , "actual:" , posi(p) , velo(v)
					v_array = []
					for a in self.actions:
						'''pos = posi(p)
						vel = velo(v)
						new_vel = vel + a*0.001 + np.cos(3*pos)*(-0.0025)
						new_pos = pos + new_vel
						pnew = pstate(new_pos)
						vnew = vstate(new_vel)'''
						pnew,vnew = newStateCalc(p,v,a)
						if  not stateValidity(pnew,vnew):
							continue
						print "\tnext on act:",a,pnew , vnew , "actual:" , posi(pnew) , velo(vnew)
						V = 0.0
						""" v(t+1)(s) = max(a:A){ R(s,a)+g*sum[s:S]( p(s'|s,a)*v(t)(s') ) 
							from the definitions of probability in this example
							for all states s'  from s which are not s+a p(s'|s,a) = 0.0 and for s'=s+a p(s'|s,a) = 1.0
							v(t+1)(s) = max(a:A){ -1 + g*sum[a:A]{1.0*v(t)(s+a) } } 
						"""
						V = V + (-1)  #reward is -1 always
						'''summation = 0.0 # represents the sum[s:S] which in this case 
						for act in self.actions:
							pdnew,vdnew = newStateCalc(p,v,act)
							summation = summation + self.V[pdnew][vdnew]'''
						V = V + self.gamma*self.V[pnew][vnew]
						v_array.append(V)
					#updating the value of V
					if not v_array:
						continue
					new_V = max(v_array)
					pi = np.argmax(v_array)
					change = abs(self.V[p][v] - new_V)<self.alpha
					converged = converged and change
					self.V[p][v] = new_V
					converged = True









if __name__=="__main__":
	car = Car()
	'''for i in range(POSITIONS):
		for j in range(VELOCITIES):
			pos = posi(i)
			vel = velo(j)
			print pos, vel , pstate(pos) , vstate(vel)'''
	#car.valueIteration()
	sys.exit(0)