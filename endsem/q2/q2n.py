from __future__ import print_function
import sys
import numpy as np
from random import randint
from random import choice
from copy import deepcopy
import matplotlib.pyplot as plt

'''
----------------------------------------------------------------------
	IDEA OF IMPLEMENTATION:

	representation of the floating point number is done using the following idea
	> first generate a binary of length 64
	> this represents integers from 0 -> 2^64-1
	> this is the genetype of our programme
	> now the conversion of genotype to phenotype is done using the following idea
		> let genotype = b
		> find i =  int(b) .  this will span from 0 to 2^64-1
		> do mi =  i-(2^63) now we'll obtain a number between -2^63 and 2^63-1
		> do f = mi*2.04/(2^63) now we'll obtain a float between -2.04 and 2.04
		> we can reverse the following instructions to get back the genotype from the phenotype
	> crossover and mutaion are done using simple string manipulations (see code) 

----------------------------------------------------------------------
'''

MAX_LEN = 64

'''integer to binary'''
def ib(x):
	return "{0:b}".format(x)

'''binary to integer'''
def bi(x):
	int(str(x),2)

'''to make the strings length equal to MAX_LEN'''
def beq(x):
	return x.zfill(MAX_LEN)

def binary_to_gray(n):
    """Convert Binary to Gray codeword and return it."""
    n = int(n, 2) # convert to int
    n ^= (n >> 1)
 
    # bin(n) returns n's binary representation with a '0b' prefixed
    # the slice operation is to remove the prefix
    return "{0:b}".format(n).zfill(MAX_LEN)

def gray_to_binary(n):
    """Convert Gray codeword to binary and return it."""
    n = int(n, 2) # convert to int
 
    mask = n
    while mask != 0:
        mask >>= 1
        n ^= mask
 
    # bin(n) returns n's binary representation with a '0b' prefixed
    # the slice operation is to remove the prefix
    return "{0:b}".format(n).zfill(MAX_LEN)

'''
	return float value b/w (-2.04 to 2.04) from 
	a binary of length 64 (explained above)
'''
def retfloat(x):
	a = int(x,2)
	a-=(2**(MAX_LEN-1))
	return (a*2.04)/(2**(MAX_LEN-1))

def retInt(x):
	return int((x*(2**(MAX_LEN-1)))/2.04)+(2**(MAX_LEN-1))

class optimizer:
	def __init__(
		self,bitlen=MAX_LEN,
		type='sum',
		specification='none',
		spec_prop='none',
		crsv_prob=0.5,
		mut_prob=0.5,
		pool_size=200,
		epoch=1000,
		batchsize = 50,
		threshold=-8
		):
		self.BIT_LEN = bitlen
		self.type  = type
		self.cr_p  = crsv_prob
		self.mut_p = mut_prob
		self.pool_size = pool_size
		self.epoch = epoch
		self.THRESHOLD = threshold
		self.specification = specification
		self.batchsize=batchsize

	def changeval(
		self,bitlen=MAX_LEN,
		type='sum',
		specification='none',
		spec_prop='none',
		crsv_prob=0.5,
		mut_prob=0.5,
		pool_size=200,
		epoch=1000,
		threshold=-8
		):
		self.BIT_LEN = bitlen
		self.type  = type
		self.cr_p  = crsv_prob
		self.mut_p = mut_prob
		self.pool_size = pool_size
		self.epoch = epoch
		self.THRESHOLD = threshold
		self.specification = specification
		self.batchsize=batchsize

	def crossover(self,s1,s2):
		pt = randint(0,self.BIT_LEN)
		a=""
		b=""
		for i in range(0,pt):
			a+=s1[i]
			b+=s2[i]

		for i in range(pt,self.BIT_LEN):
			a+=s2[i]
			b+=s1[i]

		return a,b

	def mutate(self,string,amt=5,ftfn=0):
		s = list((string))
		k= len(s)
		total = randint(1,amt)
		for j in range(0,total):
			i = randint(0,k-1)
			if randint(0,1):
				s[i] = '0'
			else:
				s[i] = '1'
		return ("".join(s))

	def fitness(self,x):
		s = 0.0
		for i in range(5):
			s += x[i]**2

		for i in range(5):
			s += int(x[i])

		for i in range(5):
			s += (x[i]**4) + np.random.normal()

		return s

	def f1(self,x):
		s = 0.0
		for i in range(5):
			s += x[i]**2
		return s

	def f2(self,x):
		s = 0.0
		for i in range(5):
			s += int(x[i])
		return s

	def f3(self,x):
		s = 0.0
		for i in range(5):
			s += (x[i]**4) + np.random.normal()
		return s


	def optimise(self):
		if self.type == 'sum':
			if self.specification == 'none':
				return self.optimise_sum_sp_none()
		elif self.type == 'pareto':
			if self.specification == 'none':
				return self.optimise_pareto_sp_none()

	def optimise_sum_sp_none(self):
		a = beq(ib(randint(0,2**64-1)))
		b = beq(ib(randint(0,2**64-1)))

		a1 = [a]*5
		a2 = [b]*5

		itr = 0

		maxarr = []
		cmin = 0.0

		eli = False

		while itr<self.epoch:
			itr+=1

			a1n = []
			a2n = []

			
			#cross over
			# a1n and a2n are the crossover products
			for i in range(5):
				t1,t2 = self.crossover(a1[i],a2[i])
				a1n.append(t1)
				a2n.append(t2)

			if not eli:
				pool = []
				fitpool 	= []
			else:
				for i in range(randint(0,50)):
					appending_one = [self.mutate(x,1) for x in a1]
					appending_score = self.fitness([retfloat(x) for x in appending_one])
					pool.append(appending_one)
					fitpool.append(appending_score)

			while len(pool) < self.pool_size:
				if np.random.uniform()>self.cr_p:
					appending_one = [self.mutate(x,3) for x in a1n]
					appending_score = self.fitness([retfloat(x) for x in appending_one])
				else:
					appending_one = [self.mutate(x,3) for x in a2n]
					appending_score = self.fitness([retfloat(x) for x in appending_one])

				pool.append(appending_one)
				fitpool.append(appending_score)

			m1f = np.min(fitpool)
			m1farg = np.argmin(fitpool)
			m1 = pool[m1farg]

			pool.pop(m1farg)
			fitpool.pop(m1farg)

			m2f = np.min(fitpool)
			m2farg = np.argmin(fitpool)
			m2 = pool[m2farg]

			v1 = (  [   round(retfloat(x),4)   for x in m1])
			v2 = (  [   round(retfloat(x),4)   for x in m2])

			if itr%self.batchsize==0:
				print(itr,v1,v2,end="")
				print(m1f,m2f)
				maxarr.append(min(m1f,m2f))

			if m1f<cmin:
				eli = True
				cmin=m1f
			else:
				eli = False

			#if m1f<self.THRESHOLD or m2f<self.THRESHOLD:
				#break

			a1,a2 = m1,m2

		return maxarr

	def optimise_pareto_sp_none(self):
		a = beq(ib(randint(0,2**64-1)))
		b = beq(ib(randint(0,2**64-1)))

		a1 = [a]*5
		a2 = [b]*5

		itr = 0

		maxarr = []

		while itr<self.epoch:
			itr+=1

			a1n = []
			a2n = []

			
			#cross over
			# a1n and a2n are the crossover products
			for i in range(5):
				t1,t2 = self.crossover(a1[i],a2[i])
				a1n.append(t1)
				a2n.append(t2)

			pool = []
			fitpool 	= []
			for j in range(self.pool_size):
				if np.random.uniform()>self.cr_p:
					appending_one = [self.mutate(x) for x in a1n]
					appending_score1 = self.f1([retfloat(x) for x in appending_one])
					appending_score2 = self.f2([retfloat(x) for x in appending_one])
					appending_score3 = self.f3([retfloat(x) for x in appending_one])
				else:
					appending_one = [self.mutate(x) for x in a2n]
					appending_score1 = self.f1([retfloat(x) for x in appending_one])
					appending_score2 = self.f2([retfloat(x) for x in appending_one])
					appending_score3 = self.f3([retfloat(x) for x in appending_one])

				pool.append(appending_one)
				fitpool.append(  (appending_score1,appending_score2,appending_score3)  )

			fp1 = [x[0] for x in fitpool]
			fp2 = [x[1] for x in fitpool]
			fp3 = [x[2] for x in fitpool]

			m1f = np.min(fitpool)
			m1farg = np.argmin(fitpool)
			m1 = pool[m1farg]

			pool.pop(m1farg)
			fitpool.pop(m1farg)

			m2f = np.min(fitpool)
			m2farg = np.argmin(fitpool)
			m2 = pool[m2farg]

			v1 = (  [   round(retfloat(x),4)   for x in m1])
			v2 = (  [   round(retfloat(x),4)   for x in m2])
			print(itr,v1,v2,end="")
			print(m1f,m2f)

			maxarr.append(min(m1f,m2f))

			if m1f<self.THRESHOLD or m2f<self.THRESHOLD:
				break

			a1,a2 = m1,m2

		return min(m1f,m2f)



if __name__ == "__main__":


	op1 = optimizer(epoch=1000,batchsize=50)
	y = op1.optimise()

	plt.plot(np.arange(len(y))*50,y)
	plt.show()

	sys.exit(0)