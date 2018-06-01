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
import random
import virtenv.include.neural_network as neu_net


def wavelet_analysis(data, sample_rate):
    coef = []
    freq = []
    arrow = []
    dati = []
    canali = []

    for sing_acqu in np.arange(0, len(data)):
        acq = data[str(sing_acqu)]
        arrow.append(acq["arrow"])
        for sing_chn in acq["dati"]:
            canali.append(sing_chn)
        dati.append(canali)

    for sampl in dati:
        part_coef=[]
        part_freq=[]

        for chan in sampl:
            scale = np.arange(1, 15)
            temp_coef, temp_freq = pywt.cwt(chan, scale, "morl", sample_rate)
            threshold = signal_to_noise_ratio(temp_coef)

            for j in temp_coef:
                for k in j:
                    if k < threshold:
                        print(k+ "--> 0")
                        k = 0

            part_coef.append(temp_coef)
            part_freq.append(temp_freq)

        coef.append(part_coef)
        freq.append(part_freq)

    return coef, freq, arrow


def signal_to_noise_ratio(data):
    max_val = 0
    sum = 0
    count = 0
    for i in data:
        for j in i:
            if max_val < j:
                max_val = j
            sum += j
            count += 1
#    print(str(max_val)+"/("+str(sum)+"/"+str(count)+")")
    return max_val/(sum/count)



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

name = "Tom"
path_name = name + "_data.json"

for i in np.arange(0, 10):
    if os.path.exists(os.path.abspath(path_name)):
        temp_dict = json.load(open(os.path.abspath(path_name)))
    #    temp = {}
   #     o = 0
 #       for x in np.arange(0, len(temp_dict)): ##acquisizione
  #           count_temp = []
  #          for k in temp_dict[str(x)]:## arrow + dati
  #              count_temp.append(k)
  #          temp[str(o)]=count_temp
  #          o+=1
        count = len(temp_dict)

    else:
        temp_dict = {}
        count = 0

    a = random.choice(["right", "left"])
    temp_ch=[]
    temp_glob = {}
    temp_glob["arrow"] = a
    for k in np.arange(0,10):
        temp_ch.append(tremp)
    temp_glob["dati"] = temp_ch

    temp_dict[str(count)]=temp_glob

    with open(os.path.abspath(path_name), 'w') as op:
        json.dump(temp_dict, op, indent=4)
#    pprint.pprint(temp)

with open(os.path.abspath(path_name)) as op:
    dat=json.load(op)



#pprint.pprint(dat)
print("finito json dump")
#pprint.pprint(dat["0"])
#print(len(dat))
#freccia = []
#dati = []
#canali = []

#for k in np.arange(0, len(dat)):
#    print(k)
#    ins = dat[str(k)]
#    freccia.append(ins["freccia"])
#    print(ins["freccia"])
#    for jj in ins["dati"]:
#        canali.append(jj)
#    dati.append(canali)

#pprint.pprint(len(freccia))
#pprint.pprint(len(dati))
print("before wavelet")
coef, freq, flag = wavelet_analysis(dat, sampl_per)
print("after wavelet")
nn = neu_net.NeuralNetwork(flag, "tom", coef, freq)

nn.setup_nn()
accuracy = nn.train(10)
print("Accuracy " + accuracy)

#    for kss in k:
#        pprint.pprint(kss)

#    coef, freq= pywt.cwt(y, np.arange(1,15), "morl", sampl_per)
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