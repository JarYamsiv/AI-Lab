import sys
import numpy as np

# function to convert tuple to a number
def linear(x,dim):
	return (x[0]*dim)+x[1]

#function to get back the tuple from the previously generated number
def fold(x,dim):
	return (x/dim,x%dim)

#to check whether the move is valid (ie, is it going outside the grid)
def validMove(p,m,dim):
	n=(p[0]+m[0],p[1]+m[1])
	condition = n[0]>=0 and n[0]<dim
	condition = condition and n[1]>=0 and n[1]<dim
	return condition

#to add tuples
def tpadd(tp1,tp2):
	return tuple(map(lambda x, y: x + y, tp1, tp2))

#to check whether the given state is valid
def validState(n,dim):
	condition = n[0]>=0 and n[0]<dim
	condition = condition and n[1]>=0 and n[1]<dim
	return condition

#the grid object
class Grid(object):
	""" |-----------------------------------------------------------
		| mat[x][y] x increases downwards and y increases to the right
		| dictionaries are used to convert between char and corresponding actions
		| available actions are listed in the list actions
		| rewards and probs are randomly generated (check the functions)
		| reward is generated upon giving a number it will generate that many states with rewards and the value is selected random
		| probabilities are also generated using the same approach
		| probabilities are of the form p(sj|si,act) where sj is next state si is current and act is action
		|----------------------------------------------------------
	"""
	def __init__(self, dim):
		self.numStates = dim*dim
		self.dim = dim
		self.moves=[(0,1),(0,-1),(1,0),(-1,0)]
		self.moveEng={
		(0,0):'s',
		(0,1):'r',
		(0,-1):'l',
		(1,0):'d',
		(-1,0):'u'
		}
		self.actToMov={
		's':(0,0),
		'r':(0,1),
		'l':(0,-1),
		'd':(1,0),
		'u':(-1,0)
		}
		self.arrow={
		's':'o',
		'u':'^',
		'd':'v',
		'r':'>',
		'l':'<',
		}
		self.actions=['s','l','r','u','d']
		self.v=np.random.rand(self.dim,self.dim)

		self.rewards={}
		self.probs={}
		self.pi_dict={}
		self.pi_mat=[]

	def setRewards(self,rnum,type_='p',debugflag=False):
		r = np.random.choice(range(self.numStates),rnum)
		self.rewardStates = [fold(x,self.dim) for x in r]
		rw={}
		for rst in self.rewardStates:
			if type_ == 'p': 
				rw[rst]=np.random.randint(0,10)
			else:
				rw[rst]=np.random.randint(-10,10)

		if debugflag:
			print "reward states are"
			print rw

		for state in range(self.numStates):
			st = fold(state,self.dim)
			for ac in self.actions:
				action = self.actToMov[ac]
				nw = tpadd(st,action)
				if nw in self.rewardStates:
					self.rewards[(st,ac)]=rw[nw]
					if debugflag:
						print st ,"on" , ac ,"has reward:",self.rewards[(st,ac)]

	def setprobs(self,debugflag=False):
		# p(sj | si ,act)
		for sil in range(self.numStates):
			for actE in self.actions:
				for sjl in range(self.numStates):
					si=fold(sil,self.dim)
					sj=fold(sjl,self.dim)
					act=self.actToMov[actE]
					if not validMove(si,act,self.dim): #invalid moves (out of the grid) have 0 probability
						self.probs[(sjl,sil,actE)]=0.0
					else:
						if sj == tpadd(si,act): #in case of correct movement give more probability to this formation
							self.probs[(sjl,sil,actE)]=np.random.randint(100,110)
						else:
							self.probs[(sjl,sil,actE)]=np.random.randint(0,5)

		for sil in range(self.numStates):
			for actE in self.actions:
				sm=0.0 #normalising
				for sjl in range(self.numStates):
					sm =sm + self.probs[(sjl,sil,actE)]
				for sjl in range(self.numStates):
					if sm != 0.0:
						self.probs[(sjl,sil,actE)]=self.probs[(sjl,sil,actE)]/sm
					else:
						self.probs[(sjl,sil,actE)]=0.0
					si=fold(sil,self.dim)
					sj=fold(sjl,self.dim)
					act=self.actToMov[actE]
					if debugflag:
						print "pr(",sj,"|",si,self.moveEng[act],")=",self.probs[(sjl,sil,actE)]

	def calcV(self,alpha,gamma,debugflag=False):
		"""
			|-----------------------------------------------------------
			| VALUE ITERATION:
			| value matrix is populated randomly in the begining
			| difference(diff) represents whether the value have changed in the iteration
			| debugflag is used for debuging
			| gamma(discount coeff) and alpha(threashold coeff) are user defined
			| uses the formula v(s) = max(a){ R(s',a) + (g*sum( p(s'|s,a))*v(s'))  }
			| argmax is used to calculate policy
			| pi_mat contains the optimal policy
			|-----------------------------------------------------------
		"""
		diff = True
		itr=1
		while diff:
			if debugflag:
				print "iteration",itr
				print self.v
			itr=itr+1
			diff = False
			for statelinear in range(self.numStates):
				s = fold(statelinear,self.dim)
				Q=[]
				#print "state:",s
				for actionEng in self.actions:
					a = self.actToMov[actionEng]
					#print "\taction:",actionEng
					a_eng = self.moveEng[a]
					qsa = self.rewards.get((s,actionEng),0.0)
					#print "\trwd:",qsa
					if debugflag:
						#print s ,"on" , a_eng ,"has reward:",self.rewards.get((s,a_eng),0.0)
						pass
					prob_sum=0.0
					for sd in range(self.numStates):
						sdf=fold(sd,self.dim)
						if validMove(s,a,self.dim):
							prob_sum = prob_sum+ self.probs[(sd,statelinear,actionEng)]*self.v[sdf[0]][sdf[1]]
						#print "\t\tprobs:",self.probs[(sd,statelinear,actionEng)],"v:",self.v[sdf[0]][sdf[1]]
					qsa=qsa+gamma*prob_sum
					#print "\tqsa:",qsa
					Q.append(qsa)
				#print "Q(",s,"):",Q,"argmax",np.argmax(Q),"move",self.actions[np.argmax(Q)]
				new_v=np.max(Q)
				diff = diff or abs(self.v[s[0]][s[1]]-new_v)>alpha
				self.v[s[0]][s[1]]=new_v
				self.pi_dict[(s[0],s[1])]=self.actions[np.argmax(Q)]

			for i in range(self.dim):
				pi_mat_line=[]
				for j in range(self.dim):
					pi_mat_line.append(self.arrow[self.pi_dict[(i,j)]])
					#pi_mat_line.append(self.pi_dict[(i,j)])
				self.pi_mat.append(pi_mat_line)





		

if __name__ == "__main__":
	#np.random.seed(15)
	grd = Grid(4)
	print grd.v
	grd.setRewards(1,'p',True)
	grd.setprobs(False)
	grd.calcV(0.0000000001,0.75,False)
	print grd.v
	print "\npolicy:\n"
	for x in range(grd.dim):
		print grd.pi_mat[x]


	sys.exit(0)