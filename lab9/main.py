from __future__ import print_function
import numpy as np

dp        = {}
best_shot = {}      


#actions contain all types of shots that can be played
shots  = [1,2,3,4,6]

#probability of a wicket falling corresponding to the selected shot
pw_min = [0.01, 0.02, 0.03, 0.1, 0.3]
pw_max = [0.1 , 0.2, 0.3, 0.5, 0.7]

#probability of scoring the number of runs given by the shot  
pr_min = 0.5
pr_max = 0.8


def get_probability(x, a):
	pw = pw_min[a] + (pw_max[a] - pw_min[a]) * (( x - 1) / 9.0 ) 
	pr = pr_max + (pr_min - pr_max) * (( x - 1) / 9.0 ) 
	return (pw, pr)


def solveDP():
	""" 
	Returns the optimal action at the DP-state defined by the player's index and the no of remaining balls.
	"""


	#Base cases
	for player in range(1, 11):
		dp[(player, 0)]    = 0
	for balls_rem in range(0, 301):
		dp[(0, balls_rem)] = 0

	for balls_rem in range(1, 301):
		for player in range(1, 11):
			Q = []
			for si in range(len(shots)) :
				prob_out, prob_score = get_probability(player, si)
				out_runs = 0
				if( player <= 9): 
					out_runs = dp[(player + 1, balls_rem - 1)]
				Q.append( prob_out * out_runs + (1 - prob_out) * (dp[(player, balls_rem - 1)] + shots[si] * prob_score)  ) 
			dp[(player, balls_rem)] = np.max( Q )
			best_shot[(player, balls_rem)] = shots[np.argmax( Q )]

"""
Showing the results
"""

# DP state       : current player and number of remaining balls .
# Value          : Maximum expected runs at this state .
# DP Transitions : iterate over all the actions and take the maximum of the expected runs . 




#Solve the problems in bottom - up fashion to see all combinations.
solveDP()

best_value  = np.zeros((300, 10))
best_action = np.zeros((300, 10))
for i in range(300):
	for j in range(10):
		best_value[i][j]  = dp[(j + 1, i + 1)]
		best_action[i][j] = best_shot[(j + 1, i + 1)]


headv = "In following matrix V, Vij is the best expected value at state ( i = balls remaining, j = player index )\n"
np.savetxt("OptimalValue.txt", best_value, delimiter = "    ", header = headv, fmt = "%f")

heada = "In following matrix A, Aij is the optimal action at state ( i = balls remaining, j = player index )\n"
np.savetxt("OptimalActions.txt", best_action, delimiter = "    ", header = heada, fmt = "%d")
