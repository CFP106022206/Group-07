# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:07:06 2019

@author: Julius 本機
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio as io

G = 1 #Gravitational constant
M = 5000 #Center Body Mass
n = 100 #Number of particles
simulation_time = 1000
e = 0 #coefficient of restitution
T = 0

R = np.ones((8,n))
R.astype('float64')

def frame(R): #用於計算
    #Calling C code
    return R, dt #回傳dt以便計算總時間
    
def image(R,i): #用於畫圖
    #藝術總監 @陳重名 請自由發揮
    T += dt #代表經過的時間
    frame(R)
    fig, ax = plt.subplots(figsize=(5,5))
    ax.scatter(R) #Matplotlib有3D的Scatter繪圖功能
    ax.set(title='frame:{}'.format(T))
    
    fig.canvas.draw()  # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    return image

kwargs_write = {'fps':24.0, 'quantizer':'nq'} #預設參數
io.mimsave('./2D_Transverse_wave_E_open_boundary.mp4', [image(R,i) for i in range(simulation_time)], fps=24) #匯出 mp4 檔案