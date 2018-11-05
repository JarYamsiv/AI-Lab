import sys
import numpy as np
import matplotlib.pyplot as plt

class engine:
	def __init__(self,dim,b=None,A=None):
		self.b = b
		self.A = A
		self.dim = dim

		if b != None and len(b) != dim:
			print ('error')
			sys.exit(1)


	def get_e(self):
		vals = [1.0,-1.0]
		x=[]
		for d in range(self.dim):
			x.append(np.random.choice(vals))
		return np.array(x)

	def calcT_m1(self,T,a):
		'''
			0(t) = 0(t-1) + a(b-0(t-1))
		'''

		if self.b ==None:
			print ('b not found')
			sys.exit(0)

		
		th = [np.zeros(self.dim)]  #theta
		e = [np.zeros(self.dim)]  #eta
		for t in range(T):
			c_e = self.get_e()
			e.append(c_e)
			c_th = th[t]
			th_n = c_th + a*(self.b-c_th) 
			th.append(th_n)
		th.pop(0)
		self.th = th
		self.e = th
		return [(np.linalg.norm(x-self.b))**2 for x in th]

	def calcT_m2(self,T,a):
		'''
			0(t) = 0(t-1) + a(b-A*0(t-1))
		'''

		if self.b ==None or self.A ==None:
			print ('b/A not found')
			sys.exit(0)

		
		th = [np.zeros(self.dim)]  #theta
		e = [np.zeros(self.dim)]  #eta
		for t in range(T):
			c_e = self.get_e()
			e.append(c_e)
			c_th = th[t]
			th_n = c_th + a*(self.b-np.dot(self.A,c_th)) 
			th.append(th_n)
		th.pop(0)
		self.th = th
		self.e = th
		return [(np.linalg.norm(x-self.b))**2 for x in th]


		
 
if __name__=="__main__":

	e1 = engine(2,[-1.0,-1.0])
	y_axis = e1.calcT_m1(1000,0.001)
	plt.plot(np.arange(1000),y_axis)

	e2 = engine(2,[1.0,1.0],[[2.0,0.0],[0.0,1.0]])
	y_axis = e2.calcT_m2(1000,0.001)
	plt.plot(np.arange(1000),y_axis)


	plt.show()
	sys.exit(0)