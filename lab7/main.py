import sys
import random
import math
import heapq as pq

#used heuristic is euclidean distance
def heuristic(nd1,nd2):
	return math.sqrt((nd1[0]-nd2[0])**2+(nd1[1]-nd2[1])**2)

#the class for storing the graph data and doing a star
class Enivronment:
	def __init__(self,nodes,links):
		self.nodes=nodes
		self.links=links

	def Astar(self,start,goal):

		# initialisation of variables
		openSet = []
		closed = []

		gDict={}
		fDict={}
		parent={}
		for node in self.nodes:
			parent[node]=(-1,-1)
			gDict[node]=10000
			fDict[node]=heuristic(node,goal)

		gDict[start]=0
		fDict[start]=gDict[start]+heuristic(start,goal)
		pq.heappush(openSet, ( fDict[start] , gDict[start] ,start)  )
		#open set of the form (h,g,(x,y) )


		#starting a star
		while openSet:

			f,g,checkNode = pq.heappop(openSet)
			closed.append(checkNode)

			if checkNode == goal:
				print "found, the path is ->"
				# this segment of code is used to print the path
				meow = checkNode

				while meow != (-1,-1):
					print meow,"g:",gDict[meow],"f:",fDict[meow]
					meow = parent[meow]

				return

			print "checking:",checkNode , "with g(n):" ,g," f(n):",f

			for neighbor in self.links[checkNode]:
				#neighbor of form ((x,y),d)
				#neighbor[0] is the node and neighbor[1] is the distance to neighbor from checkNode(of form (x,y))
				print "\tat neigh",neighbor[0]," with length:",neighbor[1]

				tentative_g_score = g + neighbor[1]
				
				if neighbor[0] in closed:
					print "\t",neighbor[0],"in closed list"
					continue

				if neighbor[0] not in [nd[2] for nd in openSet] or tentative_g_score<gDict[neighbor[0]]:
					parent[neighbor[0]]= checkNode
					gDict[neighbor[0]] = tentative_g_score
					fDict[neighbor[0]] = gDict[neighbor[0]] + heuristic(neighbor[0],goal)
					print "\tupdating",neighbor[0],"g:",tentative_g_score,"f:",fDict[neighbor[0]]
					if neighbor[0] not in [nd[2][0] for nd in openSet]:
						pq.heappush(openSet,( fDict[neighbor[0]] , tentative_g_score , neighbor[0]))
						


if __name__ == "__main__":

	nodes =[]
	links={}

	# reading the nodes data
	f = open('nodes')
	nodeIdent = f.readline() 
	print nodeIdent
	numNodes = [int(x) for x in next(f).split()]
	print numNodes[0]
	for i in range(0,numNodes[0]):
		nx,ny=[int(x) for x in next(f).split()]
		nodes.append((nx,ny))
		links[(nx,ny)]=[]
	
	print nodes

	#reading the edges data
	edges = []
	flinks = open('edges')
	edgeIdent = flinks.readline() 
	print edgeIdent
	numEdges = [int(x) for x in next(flinks).split()]
	print numEdges[0]
	for i in range(0,numEdges[0]):
		nx,ny,ngx,ngy,d=[float(x) for x in next(flinks).split()]
		edges.append(  ( (int(nx),int(ny)) , (int(ngx),int(ngy)) , d ) )
    
	# converting data format to a dictionary

	for edge in edges:
		links[edge[0]].append((edge[1],edge[2]))
		print edge[0],'-',edge[1],'-',edge[2]

	for node in nodes:
		print node
		for ng in links[node]:
			print '\t**',ng[0],'->',ng[1]

	# doing A star using the class Environment
	Env = Enivronment(nodes,links)
	Env.Astar((0,0),(6,2))


	sys.exit(0)