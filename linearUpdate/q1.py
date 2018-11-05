import sys
import matplotlib.pyplot as plt
import numpy as np




if __name__=="__main__":

	np.random.seed(0)

	T = 1000

	vals=[1,-1]

	plt.axis([0,T,-2,2])
	#plt.figure(1)

	x_axis = np.arange(T)
	theta=[]
	eata=[]
	for x in x_axis:
		eata.append(np.random.choice(vals))
		theta.append(np.mean(eata))

	y_axis=np.array(theta)
	#plt.subplot(321)
	#plt.title('avg')
	#plt.plot(x_axis,y_axis)


	theta2 = [0.0]
	eata = [0]
	vals = [1.0,-1.0]
	theta3 = [0.0]

	thetas1=[]
	thetas2=[0.0]
	thetas3=[0.0]

	theta_star = 1.0

	for t in x_axis:
		eata.append(np.random.choice(vals))
		c_eata = eata[t]
		c_theta2 = theta2[t]
		theta2.append(c_theta2+(1/(t+1))*(c_eata-c_theta2))
		theta3.append(c_theta2+(1.1)*(c_eata-c_theta2))

		thetas2.append(c_theta2+(1/(t+1))*(theta_star+c_eata-c_theta2))
		thetas3.append(c_theta2+(1.1)*(theta_star+c_eata-c_theta2))


	theta2.pop(0)
	theta3.pop(0)
	thetas2.pop(0)
	thetas3.pop(0)

	'''y_axis = np.array(theta2)
	plt.subplot(321)
	plt.title('1/(t+1)')
	plt.plot(x_axis,y_axis)

	y_axis = np.array(theta3)
	plt.subplot(325)
	plt.title('alpha=1.1')
	plt.plot(x_axis,y_axis)

	y_axis = np.array(thetas2)
	plt.subplot(324)
	plt.title('theta* + 1/t+1')
	plt.plot(x_axis,y_axis)

	y_axis = np.array(thetas3)
	plt.subplot(326)
	plt.title('theta* alpha=1.1')
	plt.plot(x_axis,y_axis)'''

	y_axis=np.array(theta3)
	plt.plot(x_axis,y_axis,color='y')
	y_axis=np.array(theta)
	plt.plot(x_axis,y_axis)
	y_axis=np.array(theta2)
	plt.plot(x_axis,y_axis)




	plt.show()
	sys.exit(0)