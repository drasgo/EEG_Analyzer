import pywt
import os
import numpy as np
import matplotlib.pyplot as plt
import pprint
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm

import matplotlib.axes as ax

#with open(os.path.abspath("virtenv/bin/mauna.dat")) as o:
#    data = np.loadtxt(os.path.abspath("virtenv/bin/sst_nino3.dat"))
#print (data)
#dt=0.083333333

x = np.arange(512)
y =np.sin(2*np.pi*x)
sampl_per=0.25
coef, freq = pywt.cwt(y, np.arange(1,15.9), 'morl', sampl_per)


#plt.matshow(coef)
#plt.show()
X=[]
Y=[]
Z=[]


 #   for j in freq:
 #       k=0
 #       a=np.array(coef)
 #       temp=a[:,i]
 #       Z.append(temp[k])
 #       k=k+1
print(len(X))
pprint.pprint(X)

print("\n\n")
pprint.pprint(freq)
print(coef)
print(len(X), " ", len(freq), " ", len(coef), " ", len(Z))

fig = plt.figure()
ax = plt.inferno(coef, freq)

plt.show()