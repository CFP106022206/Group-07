# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:07:06 2019

@author: Julius 本機
"""

import numpy as np #計算用
import matplotlib.pyplot as plt #畫圖用
import imageio as io #輸出影片用

G = 1 #Gravitational constant
M = 5000 #Center Body Mass
n = 100 #Number of particles
simulation_frame = 1000
e = 0 #coefficient of restitution
T = 0

R = np.ones((8,n))
R.astype('float64')
R_datas = R[0:2,:] #儲存所有frame的位置資訊，是個"3*n*simulation_frame"的陣列

#給定 Initial Condition
#給定位置(均勻球形分布)
r = 100 #小天體的半徑
k = n
while k > 0:
    position = (np.random.random((1,3))-np.ones((1,3))*0.5)*2*r
    norm = np.linalg.norm(position)
    if norm < r:
        R[0:3,n-k] = position
        k -= 1
#給定速度(等速前進)
for i in range(0,n):
    R[3:6,i] = np.array([1,0,0])



def frame(R): #用於計算
    #Calling C code @王一晨
    return R, dt #回傳dt以便計算總時間

def store(R): #用於儲存不同時間的位置資訊
    new_R_data = frame(R)[0:2,:]
    np.append(R_datas,new_R_data,axis = 2)
'''
for i in range(0,simulation_frame): #執行主程式
    frame(R)
    store(R)
'''
#繪圖與輸出教給藝術總監 @陳重名
