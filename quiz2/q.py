import numpy as np
from copy import deepcopy
import sys

'''
	PROBLEM DESCRIPTION
	===================
|-----------------------------------------
| the batting team has 3 wickets and 10 overs
| the bowling team has 5 bowlers each having two overs
| (economy,strike) is given
| on average takes a wicket every 'strike' balls
| and gives away 'economy' runs every over
| same bowler can bow two consecutive overs and all batsman are the same
| minimise runs scored 
|-----------------------------------------
	SOLUTION IDEA
	=============
|-----------------------------------------------------------------------
| the solution will be a matrix which says for a particular bastman remaining at a
| particular over which bowler should bowl. m[batsman_rem][over] = bowler_id 
|-----------------------------------------------------------------------
'''

max_bowlers = 5
max_run = 10*6*6
max_batsman = 3 #or max wickets
max_overs = 10

B = [ (3.0,33.0) ,(3.5,30.0), (4.0,24.0) ,(4.5,18.0) ,(5.0,15.0)]
bowlers = [1,2,3,4,5,1,2,3,4,5]

'''
	dp is the dynamic programming array
	represented as a dictionary
	dp[(player,ball_rem)] <- previous qn
	dp[(over,batsman_rem)]
'''
dp = {}
dp_bowler = {}

'''
	best_bowler is the bowler to be chosen at runs,overs
'''
best_bowler = {}

def gethash(arr):
	str=""
	for l in arr:
		if l==0:
			str += '0'
		if l==1:
			str += '1'
		if l==2:
			str += '2'
	return str

'''
	for a certain bowler (id = x) what is the probability that
	the batsman will be out
'''
def get_probability(x):
	return 1.0/B[x-1][1]

def get_run(x):
	return B[x-1][0]


'''
	this is used to solve the dp and populate the
	array with best values. and using this we'll find
	the best_bowler for a (run,over) combination
'''
def solveDP(wk_left,b_oversleft):
	''' base cases '''

	overs_left=sum(b_oversleft)

	if overs_left==0:
		return 0

	if wk_left==0:
		return 0

	s = gethash(b_oversleft)

	if dp.get((wk_left,s),None) != None:
		return dp[(wk_left,s)]



	Q = []
	for i in range(5):
		if b_oversleft[i] > 0:
			b_new     = deepcopy(b_oversleft)
			b_new[i]  -= 1
			exp_runs  = get_run(i) + (get_probability(i)*solveDP(wk_left-1,b_new)+(1- get_probability(i) )*solveDP(wk_left,b_new))
			Q.append(exp_runs)
		else:
			Q.append(100000000)

	dp[(wk_left,s)] = np.min(Q)
	best_bowler[(wk_left,s)] = np.argmin(Q)
	return dp[(wk_left,s)]





if __name__=="__main__":

	'''global dp
	global best_bowler'''
	overs_left = [2,2,2,2,2]

	solveDP(3,overs_left)

	for k in dp:
		print(k,dp[k],best_bowler.get(k,None))

	'''best_value = np.zeros((max_overs,max_batsman))
	best_action = np.zeros((max_overs,max_batsman))

	for i in range(max_overs):
		for j in range(max_batsman):
			best_value[i][j] = dp[(i,j)]
			best_action[i][j] = best_bowler[(i,j)]

	headv = "In following matrix V, Vij is the best expected value at state ( i = overs_rem, j = batsman_rem )"
	np.savetxt("OptimalValue.txt", best_value, delimiter = "    ", header = headv, fmt = "%f")

	heada = "In following matrix A, Aij is the optimal action at state ( i = overs_rem, j = batsman_rem )"
	np.savetxt("OptimalActions.txt", best_action, delimiter = "    ", header = heada, fmt = "%d")
	'''
	
sys.exit(0)