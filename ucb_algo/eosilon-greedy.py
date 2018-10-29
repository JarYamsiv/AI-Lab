'''
|---------------------------------------------------------------
|	solving multi armed bandit using epsilon-greedy algorithm
|---------------------------------------------------------------

'''
from __future__ import print_function
import sys
import numpy as np
import os
from time import sleep
from copy import deepcopy

N_expiriments = 100
N_episodes = 500000

def up():
    # My terminal breaks if we don't flush after the escape-code
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()

def down():
    # I could use '\x1b[1B' here, but newline is faster and easier
    sys.stdout.write('\n')
    sys.stdout.flush()

class Bandit:
	def __init__(self,probs):
		self.N= len(probs)
		self.probs = probs
		pass
	def get_reward(self, action):
		rand = np.random.random()  # [0.0,1.0)
		reward = 1 if (rand < self.probs[action]) else 0
		return reward


class Agent:
	def __init__(self,bandit,epsilon):
		self.Q = np.zeros(bandit.N,dtype=np.float)
		self.k = np.zeros(bandit.N,dtype=np.int)
		self.N = bandit.N
		self.epsilon = epsilon
		self.Cpos = 0
		self.itr=0
		
	def printStats(self):

		self.itr+=1
		mx = max(self.Q)
		if mx==0:
			mx=1
		ar = deepcopy(self.Q)
		arr = [x/mx for x in ar]
		printlen = 50

		print("states",self.itr)
		for i in range(self.N):
			for j in range(printlen+15):
				print(' ',end='')
			print("\r",end='')

			self.Cpos += 1
			print("bandit",i,'[',end='')
			for j in range(int(printlen*arr[i])):
				print('=',end='')
			print(']')
		for i in range(self.N+1):
			up()

	def updateQ(self,action,reward):
		self.k[action] += 1
		self.Q[action] += (1./self.k[action]) * (reward - self.Q[action])

	def get_action(self,bandit,force_Explore=False):
		rand = np.random.random()
		if rand<self.epsilon or force_Explore:
			action_explore = np.random.randint(bandit.N)
			return action_explore
		else:
			action_greedy = np.random.choice(np.flatnonzero(self.Q == self.Q.max()))
			return action_greedy



if __name__ == "__main__":
	print("Commencing program")
	bandit = Bandit([0.10,0.50,0.60,0.80,0.10,0.25,0.60,0.45,0.75,0.65])
	agent = Agent(bandit,0.01)
	for j in range(N_episodes):
		action = agent.get_action(bandit)
		reward = bandit.get_reward(action)
		agent.updateQ(action,reward)
		agent.printStats()
		#sleep(0.0001)
	sys.exit(0)