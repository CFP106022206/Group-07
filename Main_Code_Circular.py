# -*- coding: utf-8 -*-
"""
This code is used to simulate the destruction process in a circular orbit.
"""

import numpy as np #計算用
import matplotlib.pyplot as plt #Drawing picture
#import imageio as io #Making videos
import test #C calculation program
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as a
import time #Time the code

start = time.time() #The start time

#%%

G = 6.67*10**-11 #Gravitational constant
 
M = 10**5        #Particle Mass

n = 100          #Number of particles

simulation_frame = 5000

time_resoultion = 1

e = 0.5           #coefficient of restitution

M_center = 10**16 #Center Body Mass

distance = 2250

#R is the main array that stores the 3D position and velocity of the particles
R = np.ones((n,8))
R.astype('float64')
R = R.copy(order='C') #Make sure it works in C, dark magic

#This is an array that is used for the C module
empty_array = np.empty_like(R)
empty_array = empty_array.copy(order='C')

#%%

#給定 Initial Condition
#給定位置(均勻球形分布)
r = 100 #小天體的半徑

coor_trans = np.zeros((n,3))
coor_trans[:,0] = r
coor_trans[:,1] = np.pi
coor_trans[:,2] = 2*np.pi

spherical = np.random.rand(n,3)*coor_trans

position = np.zeros((n,3))
position[:,0] = spherical[:,0]*np.sin(spherical[:,1])*np.cos(spherical[:,2])
position[:,1] = spherical[:,0]*np.sin(spherical[:,1])*np.sin(spherical[:,2])
position[:,2] = spherical[:,0]*np.cos(spherical[:,1])

R[:,0:3] = position
R[:,0:3] += [distance,0,0]

#給定速度(等速前進)
R[:,3] *= 0
R[:,4] *= (G*M_center/distance)**0.5
R[:,5] *= 0
R[:,6] *= M #粒子質量
R[:,7] *= 10 #粒子半徑

#Center Mass
R[0,0:6] = 0
R[0,6] = M_center
R[0,7] = 500

R_datas = np.zeros((simulation_frame,n,3))
R_datas[0,:,:3] = R[:,:3] #儲存所有frame的位置資訊
#%%

def frame(): #用於計算
    global G
    global time_resoultion
    global R
    global e
    global empty_array 
    
    test.main_func(R,empty_array,G,time_resoultion,e)
    R = empty_array


def store(t): #用於儲存不同時間的位置資訊
    global R_datas
    global R
    R_datas[t,:,:3] = R[:,:3]

#%%
    
for t in range(1,simulation_frame): #執行主程式
    frame()
    store(t)
    print(t)

calculation_time = time.time()

#%%
end = time.time()
print(calculation_time-start)
np.save('./Circular_distance_to_time/R=2750.npy',R_datas)