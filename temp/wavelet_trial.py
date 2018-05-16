import pywt
import os
import numpy as np
import matplotlib.pyplot as plt
import pprint
from mpl_toolkits.mplot3d import Axes3D
from collections import defaultdict
from matplotlib import cm
import json
import configparser
import matplotlib.axes as ax
import time

class Vividict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
#with open(os.path.abspath("virtenv/bin/mauna.dat")) as o:
#    data = np.loadtxt(os.path.abspath("virtenv/bin/sst_nino3.dat"))
#print (data)
#dt=0.083333333
t1= time.time()
x = np.arange(512)
y =np.sin(2*np.pi*x)



sampl_per=0.25
#coef, freq = pywt.cwt(y, np.arange(1,15), 'morl', sampl_per)

tremp = np.array(y).tolist()


for i in np.arange(0, 100):
    name="Tom"
    path_name = name+"_data.json"
    if os.path.exists(os.path.abspath(path_name)):
        temp_dict = json.load(open(os.path.abspath(path_name)))
        count_temp = []
        for x in temp_dict:
            count_temp.append(x)
        count = np.max(np.array(count_temp).astype(int))

    else:
        temp_dict = {}
        count = 0

    temp=[]
    temp.append(tremp)

    temp_dict[str(i)]=temp

    with open(os.path.abspath(path_name), 'w') as op:
        json.dump(temp_dict, op, indent=4)
    print(str(i))
#    pprint.pprint(temp)

with open(os.path.abspath(path_name)) as op:
    dat=json.load(op)


for k in dat:
    coef, freq= pywt.cwt(y, np.arange(1,15), "morl", sampl_per)
#    pprint.pprint(coef)
#    pprint.pprint(freq)


#if os.path.exists(os.path.abspath(path_name)):
#    temp_dict=json.load(open(os.path.abspath(path_name)))
#    count_temp=[]
#    for x in temp_dict:
#        count_temp.append(x)
#    count=np.max(np.array(count_temp).astype(int))
#
#else:
#    temp_dict={}
#    count=0
## canale
#for j in np.arange(0, len(temp)):
#    save["Channel"+str(j)]={}
#    for i in np.arange(0, len(freq)):
#        save["Channel"+str(j)]["Frequency"+str(i)]={}
#        save["Channel"+str(j)]["Frequency"+str(i)]["Frequency"]=freq[i]
#        save["Channel"+str(j)]["Frequency"+str(i)]["Data"]=temp[j][i]
#temp_dict[str(count+1)]={}
#temp_dict[str(count+1)]=save

#pprint.pprint(temp_dict)
#with open(os.path.abspath(path_name), 'w') as op:
#    json.dump(np.array(y).tolist(), op, indent=4)
#with open(os.path.abspath(path_name)) as op:
#    data_acq=json.load(op)
#pprint.pprint(data_acq)
print(time.time()-t1)
#for a in data_acq:
#    for b in data_acq[a]:
#        for c in data_acq[a][b]:
#            ttteam.append(data_acq[a][b][c]["Frequency"])

#pprint.pprint(ttteam)

#pprint.pprint(data_acq)
#print(data_acq['Sample'][str(0)]['Frequency'])



#plt.matshow(coef)
#plt.show()
#X=[]
#Y=[]
#Z=[]


 #   for j in freq:
 #       k=0
 #       a=np.array(coef)
 #       temp=a[:,i]
 #       Z.append(temp[k])
 #       k=k+1
#print(len(X))
#pprint.pprint(X)

#print("\n\n")
#pprint.pprint(freq)
#print(coef)
#print(len(X), " ", len(freq), " ", len(coef), " ", len(Z))

#fig = plt.figure()
#ax = plt.contour(coef)

#plt.show()