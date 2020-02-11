import numpy as np
import matplotlib.pyplot as plt

plt.figure()
timeData = np.loadtxt("timeData.csv", delimiter = ',')
xPosData = np.loadtxt("xData.csv", delimiter = ',')
yPosData = np.loadtxt("yData.csv", delimiter = ',')
zPosData = np.loadtxt("zData.csv", delimiter = ',')

plt.plot(xPosData)
plt.show()
plt.plot(yPosData)
plt.show()
plt.plot(zPosData)
plt.show()

#plt.plot(countData,yData, xlabel = "time", ylabel = "y displacement", title = "y displacement over time")
#plt.plot(countData,zData, xlabel = "time", ylabel = "z displacement", title = "z displacement over time")
#plt.show()