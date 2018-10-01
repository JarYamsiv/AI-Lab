import sys

actions = [1,2,3,4,6]
prob = [
[],
[],
[],
[],
[],
[],
[],
[],
[],
[]
]

def run(pi,bl):
	if dp[p][b] != -1 :
		return dp[p][b]
	else:
		mx = -1
		for ac in actions:
			suc = prob[p][ac]
			fail = pf[p][ac]
			mx = max((ac + run(p,b-1))*suc , run(p + 1,b - 1)*fail)
		dp[p][b] = mx
		return dp[p][b]



if __name__ == "__main__":

	runs = [1,2,3,4,6]

	prob1  = [0.01,0.2,0.03,0.1,0.3]

	#if we have n balls what is the maixmum run that we can get
	currentRun = 0;


	sys.exit(0)