# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:07:06 2019

This is the main code for our final project of "Computation of physics".
The code is made to simulate the gravity and collision between N particles.
Which can be used to study Tidal Effect, Roche Limit and other phenomenon.

Crew member:
    林彥興 106020008 Main Code Constructor / 
    王一晨 106022212 Main Code Constructor / Calculation of collision and gravity
    陳重名 106022206 Director of Art
    呂長益 106022109 Art Supporter
    黃禕煒 x1072165  Art Supporter / Calculation of Collision and Gravity
    陳重衡 106020087 Initial Condition Giver 

"""

import numpy as np #計算用
import matplotlib.pyplot as plt #Drawing picture
import test #C calculation program
from mpl_toolkits.mplot3d import Axes3D
import time #Time the code

start = time.time() #The start time

#%%

'''Creating parameter and array'''

G = 6.67*10**-11 #Gravitational constant
 
M = 5*10**5 #Particle Mass

n = 100 #Number of particles

simulation_frame = 5000

time_resoultion = 0.001

e = 0            #coefficient of restitution


#R is the main array that stores the 3D position and velocity of the particles
R = np.ones((n,8))
R.astype('float64')
R = R.copy(order='C') #Make sure it works in C, dark magic

#This is an array that is used for the C module
empty_array = np.empty_like(R)
empty_array = empty_array.copy(order='C')

#%%

'''Initial Condition'''

#給定位置(均勻球形分布)
r = 50 #小天體的半徑

coor_trans = np.zeros((n,3))
coor_trans[:,0] = r
coor_trans[:,1] = np.pi
coor_trans[:,2] = 2*np.pi

spherical = np.random.rand(n,3)*coor_trans

position = np.zeros((n,3))
position[:,0] = spherical[:,0]*np.sin(spherical[:,1])*np.cos(spherical[:,2])
position[:,1] = spherical[:,0]*np.sin(spherical[:,1])*np.sin(spherical[:,2])
position[:,2] = spherical[:,0]*np.cos(spherical[:,1])

r_vector = np.ones((n,3))
r_vector[:,2] = 0

R[:,0:3] = position + r_vector*10**4/2**0.5

#給定速度(等速前進)
R[:,3] *= 141400
R[:,4] *= -141400
R[:,5] *= 0

R[:,6] *= M #粒子質量
R[:,7] *= 5 #粒子半徑


#Center Mass
R[0,0:6] = 0
R[0,6] = 6*10**24
R[0,7] = 500

#Creat the array that stores the data in different time
R_datas = np.zeros((simulation_frame,n,3))
R_datas[0,:,:3] = R[:,:3] 

#%%

'''Define the function use for calculation and storing data'''

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

'''Main Code'''

for t in range(1,simulation_frame): #執行主程式
    frame()
    store(t)
    print(t)

calculation_time = time.time()
print("Calculation_time: "+str(calculation_time-start))
np.save("R_datas.npy",R_datas)