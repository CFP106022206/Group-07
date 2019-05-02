# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:07:06 2019

@author: Julius 本機
"""

import numpy as np #計算用
import matplotlib.pyplot as plt #畫圖用
import imageio as io #輸出影片用
import test

global G #Gravitational constant
G = 1 
global M #Center Body Mass
M = 5000
global n #Number of particles
n = 100 
global simulation_frame
simulation_frame = 100
global time_resoultion
time_resoultion = 1
global e #coefficient of restitution
e = 0
global T
T = 0

global R
R = np.ones((n,8))
R.astype('float64')

global R_datas
R_datas = np.zeros((n,3,simulation_frame))
R_datas[:,0:3,0] = R[:,0:3] #儲存所有frame的位置資訊，是個"3*n*simulation_frame"的陣列


#給定 Initial Condition
#給定位置(均勻球形分布)
r = 100 #小天體的半徑
k = n
while k > 0:
    position = np.transpose((np.random.random((3,1))-np.ones((3,1))*0.5)*2*r)
    norm = np.linalg.norm(position)
    if norm < r:
        R[n-k,0:3] = position
        k -= 1
#給定速度(等速前進)
for i in range(0,n):
    R[i,3:6] = np.array([1,0,0])


def frame(): #用於計算
    global R
    empty_array = np.zeros((8,n))
    empty_array = empty_array.copy(order='C')
    R = R.copy(order='C')
    test.main_func(R,empty_array,G,time_resoultion,e)
    R = empty_array


def store(t): #用於儲存不同時間的位置資訊
    new_R_data = R[:,0:3]
    global R_datas
    R_datas[:,0:3,t] = new_R_data

for t in range(0,simulation_frame): #執行主程式
    frame()
    store(t)

#繪圖與輸出教給藝術總監 @陳重名
