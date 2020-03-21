import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x = []
y = []
z = []

z = np.loadtxt('zData.csv')
#print(a.size)

#histX = plt.hist(x, bins=100)
i=0
'''
while i<2000:
    np.delete(arr=y,obj=i)
    i = i + 1
'''

histZ = plt.hist(z, bins=10)
#histZ = plt.hist(z, bins=100)
plt.show()