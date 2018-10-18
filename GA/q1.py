import sys
import numpy as np
from random import randint
from random import choice
from copy import deepcopy

finalString = "vismay loves genetic algorithm"
length = len(finalString)

d = []
for i in range(97,123):
	d.append(chr(i))
d.append(' ')

POOLSIZE = 200

def generateRandom():
	s = []
	for i in range(length):
		n = randint(0,26)
		s.append(d[n])
	return s

def fitnessScore(string):
	fitness = 0
	for i in range(length):
		if string[i] == finalString[i]:
			fitness = fitness + 1
	return fitness

def crossover(s1,s2):
	a=[]
	b=[]
	for i in range(length):
		if randint(0,1):
			a.append(s1[i])
			b.append(s2[i])
		else:
			a.append(s2[i])
			b.append(s1[i])
	return a,b

def mutate(string):
	s = deepcopy(string)
	total = randint(2,3)
	for j in range(total):
		i = randint(0,length-1)
		n = choice(d)
		s[i] = n
	return s

def prnt(data):
	print("".join(str(x) for x in data))

def prnt_s(data):
	scr = fitnessScore(data)
	print("".join(str(x) for x in data),scr)

'''
|=======================================================================================
| IMPLEMENTATION OF GENETIC LEARNING ALGORITHM
| the required string is: "vismay loves genetic algorithm"
| starting string can be anything of length same as final string
|=======================================================================================
'''
if __name__ == "__main__":
	print "final string:" , finalString
	print "length:" , length

	initialString = []

	print "dictionary = ",d
	s1 = generateRandom()
	s2 = generateRandom()
	st1,st2 = s1,s2
	prnt(s1)
	prnt(s2)
	prnt(crossover(s1,s2))
	print fitnessScore(s1)

	print "====STARTING===="
	itr = 0
	while True:
		s_new,s_new1 = crossover(s1,s2)
		pool = []
		fitpool = []
		for i in range(POOLSIZE):
			if randint(0,1):
				m_s = mutate(s_new)
				m_f = fitnessScore(m_s)
			else:
				m_s = mutate(s_new1)
				m_f = fitnessScore(m_s)
			pool.append(m_s)
			fitpool.append(m_f)

		#taking the first maximum
		m1_f_arg = np.argmax(fitpool)
		m1_f = fitpool[m1_f_arg]
		m1_s = pool[m1_f_arg]
		print "1.  pos:",m1_f_arg,"fit_val:" , m1_f
		prnt(m1_s)
		pool.pop(m1_f_arg)
		fitpool.pop(m1_f_arg)

		#taking the second maximum
		m2_f_arg = np.argmax(fitpool)
		m2_f = fitpool[m2_f_arg]
		m2_s = pool[m2_f_arg]
		print "2.  pos:",m2_f_arg,"fit_val:" , m2_f
		prnt(m2_s)
		pool.pop(m2_f_arg)
		fitpool.pop(m2_f_arg)  

		s1 = m1_s
		s2 = m2_s


		if m1_f == length or m2_f == length:
			break
		itr = itr +1

	print "================FINAL================="
	if m1_f == length:
		prnt(m1_s)
	else:
		prnt(m2_s)
	print "==========STARTED FROM================="
	prnt(st1)
	prnt(st2)
	print "iterations:",itr
	sys.exit(0)