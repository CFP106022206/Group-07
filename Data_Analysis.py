# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:05:46 2019

@author: Julius 本機
"""

import numpy as np #計算用
import matplotlib.pyplot as plt #Drawing picture
import time

start = time.time()

R_datas = np.load('./R_datas.npy')
R_datas = np.delete(R_datas,0,axis = 1)

sep_datas = []

frames = np.shape(R_datas)[0]
n = np.shape(R_datas)[1]

#%%
#Using for loop
'''
for t in range(0,np.shape(R_datas)[0]):
    sep = []
    for i in R_datas_1:
        for j in R_datas_1:
            if i[0]!=j[0] or i[1]!=j[1] or i[2]!=j[2]:
                sep.append(1/np.linalg.norm(i-j))
                
    sep_datas.append(sum(sep))
    print(t)
'''
#%%
#Using Numpy
for t in range(0,frames):
    R_t_datas = R_datas[t,:,:]
    R_t_change = R_t_datas
    sep = 0
    for i in range(0,n):
        R_t_change = np.delete(R_t_change,0,axis = 0)
        R_t_change = np.append(R_t_change,np.zeros((1,3)),axis=0)
        diff = R_t_datas-R_t_change
        diff_3 = np.sum(diff**2,axis = 1)
        sep += -np.sum(1/diff_3)
    sep_datas.append(sep)
    print(t)
#%%
end = time.time()
t = np.linspace(0,frames-1,frames)
fig = plt.figure(figsize = (5,3),dpi=150)
plt.plot(t,sep_datas)
plt.xlabel("time(s)")
plt.ylabel("Seperation")
plt.savefig('seperation')
print("Calculation time: "+str(end-start))