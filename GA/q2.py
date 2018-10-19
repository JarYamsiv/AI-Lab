import sys

import numpy as np

from random import uniform
from random import randint
from random import choice

from copy import deepcopy

bits="0123456789abcdef"
POOL_SIZE = 200

def constraint(x):
	if x<=10.0 and x>= -10.0:
		return 1
	else:
		return 0

def encode(x):
	a = float.hex(x)
	b = [x for x in a]
	if b[0] == '-':
		b.pop(0)
		return b,'-'
	else:
		return b,'+'

def decode(x,sign):
	f=[]
	if sign == '-':
		f.append('-')
		for i in x:
			f.append(i)
	else:
		for i in x:
			f.append(i)
	#print f
	h = ''.join(str(e) for e in f)
	#print float.fromhex(h)
	return float.fromhex(h)

def crossover(p1,s1,p2,s2):
	'''
		c1 anbd c2 are childs
		the first 4 elements of both of them are same
		and the rest are taken as crossovers with probability 0.5
	'''
	c1,c2=[],[]
	c1.append('0')
	c1.append('x')
	c1.append('1')
	c1.append('.')
	c2.append('0')
	c2.append('x')
	c2.append('1')
	c2.append('.')
	for i in range(4,20):
		if randint(0,1):
			c1.append(p1[i])
			c2.append(p2[i])
		else:
			c1.append(p2[i])
			c2.append(p1[i])

	if randint(0,1):
		return c1,c2,s1,s2
	else:
		return c1,c2,s2,s1
	

def mutate(x):
	a = deepcopy(x)
	for i in range(4,17):
		a[i] = choice(bits)
	return a

def fitnessFun(x):
	v1 = x**2
	v2 = (x-2)**2
	return np.exp(-v1)+np.exp(-v2)



if __name__=="__main__":
	'''for i in range(2):
		b1,sign1 = encode(uniform(-10.0,10.0))
		b2,sign2 = encode(uniform(-10.0,10.0))
		c1,c2 = crossover(b1,sign1,b2,sign2)
		print b1,sign1, decode(b1,sign1) , constraint(decode(b1,sign1))
		print b2,sign2, decode(b2,sign2) , constraint(decode(b2,sign2))
		print c1,sign1, decode(c1,sign1) , constraint(decode(c1,sign1))
		print c2,sign2, decode(c2,sign2) , constraint(decode(c2,sign2))
		m = mutate(c1)
		print m,sign1,decode(m,sign1) , fitnessFun(decode(m,sign1))'''
	'''
	|=====================================================================================
	| GENETTIC ALGORITHM 2
	| optimise the following problem using genetic learning algorithm
	| minimise f1(x) = x^2
	| minimise f2(x) = (x-2)^2
	| such that -10<=x<=10
	| before crossover and mutaion the floating point number is encoded (to hex)
	| while calculation of fitness it is decoded
	|=====================================================================================
	'''
	p1,s1 = encode(uniform(-10.0,10.0))
	p2,s2 = encode(uniform(-10.0,10.0))
	while True:
		c1,c2,cs1,cs2=crossover(p1,s1,p2,s2)
		pool=[]
		fitpool=[]
		for i in range(POOL_SIZE):
			if randint(0,1):
				m = mutate(c1) #mutated
				md = decode(m,cs1) #mutated adn decoded
			else:
				m = mutate(c2) #mutated
				md = decode(m,cs2) #mutated adn decoded

			pool.append(m)
			fitpool.append(fitnessFun(md))

		max1       = np.argmax(fitpool)
		max1_val_f = fitpool[max1]
		max1_val   = pool[max1]

		pool.pop(max1)
		fitpool.pop(max1)

		max2       = np.argmax(fitpool)
		max2_val_f = fitpool[max2]
		max2_val   = pool[max2]

		p1,s1,p2,s2 = max1_val,cs1,max2_val,cs2
		print "1) ",decode(max1_val,cs1),"fit:",max1_val_f
		print "2) ",decode(max2_val,cs2),"fit:",max2_val_f

	

	print ">>>>>" , decode(max1_val,cs1) , decode(max2_val,cs2)


	sys.exit(0)