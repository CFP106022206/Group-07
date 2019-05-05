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

G = 6.67*10**-11 #Gravitational constant
 
M = 8000         #Center Body Mass

n = 100          #Number of particles

simulation_frame = 10
time_resoultion = 1

e = 0            #coefficient of restitution

T = 0

R = np.ones((n,8))
R.astype('float64')
R = R.copy(order='C')
 
empty_array = np.empty_like(R)
empty_array = empty_array.copy(order='C')

#給定 Initial Condition
#給定位置(均勻球形分布)
r = 100 #小天體的半徑
k = n
while k > 0:
    position = (np.random.random((1,3))-np.ones((1,3)))*2*r
    norm = np.linalg.norm(position)
    if norm < r:
        R[n-k,0:3] = position
        k -= 1
#給定速度(等速前進)
R[:,4:6] *= 0
R[:,6]   *= 8000

R_datas = np.zeros((simulation_frame,n,3))
R_datas[0,:,:3] = R[:,:3] #儲存所有frame的位置資訊


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

for t in range(1,simulation_frame): #執行主程式
    frame()
    store(t)
'''
def image(i):
    fig, ax = plt.subplots(figsize=(5,5))
    ax.scatter(R_datas[:,0,i],R_datas[:,1,i])
    ax.set(xlabel='Offset', ylabel='Offset',title='frame:{}'.format(t))
    ax.set_ylim(-1000, 1000)
    ax.set_xlim(-1000, 1000)
    
    fig.canvas.draw()  # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    return image

kwargs_write = {'fps':24.0, 'quantizer':'nq'}
io.mimsave('./movie.mp4', [image(i) for i in range(simulation_frame)], fps=20)
'''


#繪圖與輸出教給藝術總監 @陳重名
