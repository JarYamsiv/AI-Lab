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



'''
	for a certain bowler (id = x) what is the probability that
	the batsman will be out
'''
def get_probability(x):
	return 6.0/B[x-1][1]

def get_run(x):
	return B[x-1][0]


'''
	this is used to solve the dp and populate the
	array with best values. and using this we'll find
	the best_bowler for a (run,over) combination
'''
def solveDP():
	''' base cases '''
	'''global dp_bowler
	global dp
	global best_bowler'''


	for over in range(max_overs):
		dp[(over, 0)]    = 0
		dp_bowler[(over,0)] = bowlers
	for batsman_rem in range(max_batsman):
		dp[(0, batsman_rem)] = 0
		dp_bowler[(0,batsman_rem)] = bowlers


	for i in range(max_overs):
		for j in range(max_batsman):
			dp[(i,j)] = 0
			dp_bowler[(i,j)] = deepcopy(bowlers)
			best_bowler[(i,j)] = 1

	for z in range(1):
			
		for batsman_rem in range(max_batsman):
			for over in range(max_overs):
				Q = []
				print "at(batsman_rem:",batsman_rem+1,",over:",over+1,")"
				print "\tbowler_arr:",dp_bowler[(over,batsman_rem)]
				for bowler in dp_bowler[(over,batsman_rem)]:
					out_prob = get_probability(bowler)
					runs_yield = get_run(bowler)
					#print "\t\tbowler",bowler,"r:",runs_yield,"p:",out_prob
					if batsman_rem>0:
						val = (out_prob*runs_yield)+ (1-out_prob)*(runs_yield+dp[(over,batsman_rem-1)])
						Q.append(val)
					else:
						val = (out_prob*runs_yield)+(1-out_prob)*(runs_yield+dp[(over,batsman_rem)])
						Q.append(val)

			
				if Q:
					dp[(over,batsman_rem)] = np.min(Q)
					#print "\t",Q

					bbowler = dp_bowler[(over,batsman_rem)][np.argmin(Q)]
					print "\tbest_bowler",bbowler
					if over<max_overs-1:
						for j in range(1,max_overs-over):
							#print "\t\tpoping",bbowler
							#print "\t\tfrom(",over+j,",",batsman_rem,")",dp_bowler[(over+j,batsman_rem)]
							if dp_bowler[(over+j,batsman_rem)] and np.argmin(Q)<len(dp_bowler[(over+j,batsman_rem)]):
								dp_bowler[(over+j,batsman_rem)].pop(np.argmin(Q))
							#print "\t\tleaving",dp_bowler[(over+j,batsman_rem)]

					best_bowler[(over,batsman_rem)] = bbowler
		#break





if __name__=="__main__":

	'''global dp
	global best_bowler'''

	solveDP()

	best_value = np.zeros((max_overs,max_batsman))
	best_action = np.zeros((max_overs,max_batsman))

	for i in range(max_overs):
		for j in range(max_batsman):
			best_value[i][j] = dp[(i,j)]
			best_action[i][j] = best_bowler[(i,j)]

	headv = "In following matrix V, Vij is the best expected value at state ( i = overs_rem, j = batsman_rem )"
	np.savetxt("OptimalValue.txt", best_value, delimiter = "    ", header = headv, fmt = "%f")

	heada = "In following matrix A, Aij is the optimal action at state ( i = overs_rem, j = batsman_rem )"
	np.savetxt("OptimalActions.txt", best_action, delimiter = "    ", header = heada, fmt = "%d")

	
	sys.exit(0)