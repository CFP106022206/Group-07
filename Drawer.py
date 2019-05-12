# -*- coding: utf-8 -*-
"""
Created on Sun May 12 22:16:49 2019

@author: Julius 本機
"""

import numpy as np #Calculation
import matplotlib.pyplot as plt #Drawing picture
from mpl_toolkits.mplot3d import Axes3D
import time #Time the code
import imageio #Making videos
import os #File Path

R_datas = np.load("R_datas.npy")

#%%

start_of_drawing = time.time()

scale = 1*10**4

time_accelation = 100

simulation_frame = np.shape(R_datas)[0]

for t in range(0,int(simulation_frame/time_accelation)):
    fig = plt.figure(figsize=(5,5),dpi=80)
    ax = Axes3D(fig)
    ax.scatter(R_datas[t*time_accelation,:,0],R_datas[t*time_accelation,:,1],R_datas[t*time_accelation,:,2])
    ax.set_xlim(-scale,scale)
    ax.set_ylim(-scale,scale)
    ax.set_zlim(-scale,scale)
    plt.savefig(r'C:\Users\林彥興\.spyder-py3\Computation of physics\Final Project\frame\Roche_limit_%04d.png' % t)
    plt.close()
    print(t)

end = time.time()

print('Drawing time: '+ str(end-start_of_drawing)) 

fileList = []
for file in os.listdir('C:/Users/林彥興/.spyder-py3/Computation of physics/Final Project/frame/'):
    if file.startswith('Roche_limit_'):
        complete_path = 'C:/Users/林彥興/.spyder-py3/Computation of physics/Final Project/frame/' + file
        fileList.append(complete_path)

writer = imageio.get_writer('Circular_5.mp4', fps=20)

t = 0

for im in fileList:
    writer.append_data(imageio.imread(im))
    t += 1
    print(t)

writer.close()