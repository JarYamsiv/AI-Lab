import sys
import numpy as np

#w is the wickets left and r is the desired run to find the probability
def probability(w,r):
	pw_min = [0.01,0.02,0.03,0.1,0.3]
	pw_max = [0.1,0.2,0.3,0.5,0.7]
	pr_min = 0.5
	pr_max = 0.8

	if r>5:
		r = r-1

	r=r-1

	pw = pw_min[r] + (pw_max[r]-pw_min[r])*(w-1)/9
	pr = pr_min + (pr_max-pr_min)*(w-1)/9
	return pw,pr

if __name__=="__main__":

	states = [11,10,9,8,7,6,5,4,3,2,1] #represents the amount of wickets left
	n      = 9
	v      = np.random.rand(n)
	scores = [1,2,3,4,6]
	print v
	alpha = 0.00001
	diff  = True
	while diff:
		diff=False
		for s in states:
			for b in range(300):
				for a in scores:
					pass



	sys.exit(0)