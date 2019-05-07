# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:07:06 2019

@author: Julius 本機
"""

import numpy as np #計算用
import matplotlib.pyplot as plt #Drawing picture
#import imageio as io #Making videos
import test #C calculation program
from mpl_toolkits.mplot3d import Axes3D
import time #Time the code

start = time.time() #The start time

#%%

G = 6.67*10**-11 #Gravitational constant
 
M = 4.5*10**9 #Particle Mass

n = 100 #Number of particles

simulation_frame = 2000

time_resoultion = 0.02

e = 0            #coefficient of restitution


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

R[:,0:3] = position + np.ones((n,3))*27450

#給定速度(等速前進)
R[:,3] *= 2100*32
R[:,4] *= -2100*32
R[:,5] *= 0
R[:,6] *= M #粒子質量
R[:,7] *= 5 #粒子半徑
R_datas = np.zeros((simulation_frame,n,3))
R_datas[0,:,:3] = R[:,:3] #儲存所有frame的位置資訊

#Center Mass
R[0,0:6] = 0
R[0,6] = 6*10**24
R[0,7] = 500

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
#繪圖與輸出教給藝術總監 @陳重名

start_of_drawing = time.time()

picture_scale = 50000

for t in range(0,simulation_frame):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(R_datas[t,:,0],R_datas[t,:,1],R_datas[t,:,1])
    ax.set_xlim(-picture_scale,picture_scale)
    ax.set_ylim(-picture_scale,picture_scale)
    ax.set_zlim(-picture_scale,picture_scale)
    plt.savefig(r'C:\Users\林彥興\.spyder-py3\Computation of physics\Final Project\frame_Earth_far\Roche_limit_%04d.png' % t)
    plt.close()
    print(t)

end = time.time()

print('Calculation time: '+ str(calculation_time-start))
print('Drawing time: '+ str(end-start_of_drawing))