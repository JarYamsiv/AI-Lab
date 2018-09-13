import numpy as np
import sys
import pickle

def getEventTime(evnt):
    return evnt[0]

def calcSpeed(x):
    return (np.exp(0.5*x)/(1+np.exp(0.5*x)))+(15/(1+np.exp(0.5*x)))

#the environment
class Network:
    def __init__ (self,nVertex,networkMatrix,time,vehicle):
        self.nVertex=nVertex;
        self.networkMatrix=networkMatrix;
        self.time = time;
        self.vehicle = vehicle;
        self.vehicleCountOnRoad= np.zeros((10,10));
        self.events=[]
        self.events.append((time[0],0))

    def calcVehicleCount(self):
        self.vehicleCount= len(time)
        #print("there are ",self.vehicleCount," vehicles ")

    def getDist(self,x,y):
        return networkMatrix.item((x,y))

    def getVehicleDensity(self,x,y):
        return vehicleCountOnRoad.item((x,y))

    def executeNextEvent(self):
        sort(self.events,key=getEventTime)
        nextEventToExec=self.events.pop(0)

    def isDone(self):
        if len(self.events)==0:
            return 1
        else:
            return 0


#the agent(s)
class Vehicle:
    def __init__(self,startNode,startTime,id,travelData,roadNetwork):
        self.startNode=startNode
        self.currentNode = self.startNode
        self.startTime=startTime
        #print("start node : ",self.startNode," start time: ",self.startTime)
        self.id= id
        self.travelData=travelData
        #print(self.travelData)
        self.followingEvent=self.startTime
        self.roadNetwork=roadNetwork
        self.position=0

    def calcNextEvent(self,x):
        distance=self.roadNetwork.getDist(self.position,self.position+1)
        x=self.roadNetwork.getVehicleDensity(self.position,self.position+1)
        nextEvent=self.followingEvent+(distance/calcSpeed(x))


if __name__=="__main__":
    print("starting the programme");

    #loading the adjacency matrix of the road network
    netMat = pickle.load(open("roads/road.dat","r"))

    #loading the array which stores the time at which each vehicle starts from it's 
    time = pickle.load(open("roads/time","r"))

    #each vehicle will go through 5 nodes including the start
    vehicleTravelData = pickle.load(open("roads/vehicle","r"))

    roadNet=Network(10,netMat,time,vehicleTravelData)
    roadNet.calcVehicleCount();

    #loading the vehicle data
    vehicles = []
    for i in range(100):
        vehicles.append(   Vehicle(  vehicleTravelData.item((i,0))  ,time.item(i)  ,i  ,vehicleTravelData[i]  ,roadNet  )   )



    #exiting the programme
    sys.exit(0)


