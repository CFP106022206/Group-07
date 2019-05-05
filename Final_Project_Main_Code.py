# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:07:06 2019

@author: Julius 本機
"""

import numpy as np #計算用
#import matplotlib.pyplot as plt #畫圖用
#import imageio as io #輸出影片用
import test
#from mpl_toolkits.mplot3d import Axes3D

#%%

G = 6.67*10**-11 #Gravitational constant
 
M = 8000         #Center Body Mass

n = 100          #Number of particles

simulation_frame = 100

time_resoultion = 1

e = 0            #coefficient of restitution

R = np.ones((n,8))
R.astype('float64')
R = R.copy(order='C')
 
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

#給定速度(等速前進)
R[:,4:6] *= 0
R[:,6]   *= 8000

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

#%%
#繪圖與輸出教給藝術總監 @陳重名
