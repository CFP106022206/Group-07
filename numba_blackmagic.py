# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 22:19:03 2019

@author: 王一晨
"""
import numpy as np
from numba import njit, prange

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as a
import matplotlib.pyplot as plt


#%%

G = 6.67*10**-11   #Gravitational constant
 
M = 5*10**5        #Center Body Mass

n = 10             #Number of particles

simulation_frame = 100

time_resoultion = 1

e = 1            #coefficient of restitution

#save_perframe = 1


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
r = 435 #小天體的半徑

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
R[:,0:3] += [1000,1000,1000]

#給定速度(等速前進)
R[:,3] *= 0#-250000  
R[:,4] *= 0
R[:,5] *= 0
R[:,6] *= M #粒子質量
R[:,7] *= 20 #粒子半徑

#Center Mass

R[0,0:6] = 0
R[0,6] = 10**15
R[0,7] = 300

R_datas = np.zeros((simulation_frame,n,3))
R_datas[0,:,:3] = R[:,:3] #儲存所有frame的位置資訊
#%% algorithm
@njit(parallel=True)
def algorithm(R,empty_array):
    # gravity
    empty_array[:,6:] = R[:,6:]
    global n,G,time_resoultion,e
    for i in prange(n):

        m = np.zeros((7,3))
        k = np.zeros((7,3))
        
        #for j in range(n):
        #    if j!=i:
        if i == 0:
            b = R[1:].copy()
        elif i == n-1:
            b = R[:-1].copy()
        else:
            b = np.vstack((R[:i],R[i+1:])).copy()
        
        
        #pos = np.zeros((n-1,3))
        #rad = np.zeros((n-1,1))
        pos  = b[:, :3].copy()
        rad  = b[:,7:8].copy()
        
            
        rad += R[i,7:8]
        pos -= R[i,0:3]
        
        dis  = np.sqrt(np.sum(pos**2,axis = 1)).reshape((n-1,1))#np.sqrt(pos[:,0]**2+pos[:,1]**2+pos[:,2]**2).reshape((n-1,1))
        res  = (dis-rad)[:,0]
        b    = b[np.where(res>0)]
        
        mass = np.zeros((len(b),3))
        mass[:,0:1]= b[:,6:7]
        mass[:,1:2]= b[:,6:7]
        mass[:,2:3]= b[:,6:7]
        
        k[0] = R[i,3:6].copy()
        r1   = R[i,:3]
        
        v    = b[:,:3]-r1
        lv   = np.sqrt(np.sum(v**2,axis = 1)).reshape(len(v),1)
        m[0] = np.sum(G*mass/(lv**3)*v,axis = 0)
        #        m[0] += (G*R[j,6])/(np.linalg.norm(R[j,:3]-r1)**2)*(R[j,:3]-r1)/np.linalg.norm(R[j,:3]-r1)
        
        k[1] = k[0]+m[0]*time_resoultion/5
        r    = r1  +k[0]*time_resoultion/5
        #for j in range(n):
        #    if j!=i:
        #        m[1] += (G*R[j,6])/(np.linalg.norm(R[j,:3]-r)**2)*(R[j,:3]-r)/np.linalg.norm(R[j,:3]-r)
        v    = b[:,:3]-r
        lv   = np.sqrt(np.sum(v**2,axis = 1)).reshape(len(v),1)
        m[1] = np.sum(G*mass/(lv**3)*v,axis = 0)
                
        k[2] = k[0]+m[0]*time_resoultion*3/40+m[1]*time_resoultion*9/40
        r    = r1  +k[0]*time_resoultion*3/40+k[1]*time_resoultion*9/40
        #for j in range(n):
        #    if j!=i:
        #        m[2] += (G*R[j,6])/(np.linalg.norm(R[j,:3]-r)**2)*(R[j,:3]-r)/np.linalg.norm(R[j,:3]-r)
        v    = b[:,:3]-r
        lv   = np.sqrt(np.sum(v**2,axis = 1)).reshape(len(v),1)
        m[2] = np.sum(G*mass/(lv**3)*v,axis = 0)
        
        k[3] = k[0]+m[0]*time_resoultion*44/45     +m[1]*time_resoultion*(-56/15)     +m[2]*time_resoultion*32/9
        r    = r1  +k[0]*time_resoultion*44/45     +k[1]*time_resoultion*(-56/15)     +k[2]*time_resoultion*32/9
        #for j in range(n):
        #    if j!=i:
        #        m[3] += (G*R[j,6])/(np.linalg.norm(R[j,:3]-r)**2)*(R[j,:3]-r)/np.linalg.norm(R[j,:3]-r)
        v    = b[:,:3]-r
        lv   = np.sqrt(np.sum(v**2,axis = 1)).reshape(len(v),1)
        m[3] = np.sum(G*mass/(lv**3)*v,axis = 0)
                
        k[4] = k[0]+m[0]*time_resoultion*19372/6561+m[1]*time_resoultion*(-25360/2187)+m[2]*time_resoultion*64448/6561+m[3]*time_resoultion*(-212/729)
        r    = r1  +k[0]*time_resoultion*19372/6561+k[1]*time_resoultion*(-25360/2187)+k[2]*time_resoultion*64448/6561+k[3]*time_resoultion*(-212/729)     
        #for j in range(n):
        #    if j!=i:
        #        m[4] += (G*R[j,6])/(np.linalg.norm(R[j,:3]-r)**2)*(R[j,:3]-r)/np.linalg.norm(R[j,:3]-r)
        v    = b[:,:3]-r
        lv   = np.sqrt(np.sum(v**2,axis = 1)).reshape(len(v),1)
        m[4] = np.sum(G*mass/(lv**3)*v,axis = 0)
                
        k[5] = k[0]+m[0]*time_resoultion*9017/3168 +m[1]*time_resoultion*(-355/33)    +m[2]*time_resoultion*46732/5247+m[3]*time_resoultion*49/176    +m[4]*time_resoultion*(-5103/18656)
        r    = r1  +k[0]*time_resoultion*9017/3168 +k[1]*time_resoultion*(-355/33)    +k[2]*time_resoultion*46732/5247+k[3]*time_resoultion*49/176    +k[4]*time_resoultion*(-5103/18656)
        #for j in range(n):
        #    if j!=i:
        #        m[5] += (G*R[j,6])/(np.linalg.norm(R[j,:3]-r)**2)*(R[j,:3]-r)/np.linalg.norm(R[j,:3]-r)
        v    = b[:,:3]-r
        lv   = np.sqrt(np.sum(v**2,axis = 1)).reshape(len(v),1)
        m[5] = np.sum(G*mass/(lv**3)*v,axis = 0)
                
        k[6] = k[0]+m[0]*time_resoultion*35/384                                       +m[2]*time_resoultion*500/1113  +m[3]*time_resoultion*125/192   +m[4]*time_resoultion*(-2187/6784) +m[5]*time_resoultion*11/84 
        r    = r1  +k[0]*time_resoultion*35/384                                       +k[2]*time_resoultion*500/1113  +k[3]*time_resoultion*125/192   +k[4]*time_resoultion*(-2187/6784) +k[5]*time_resoultion*11/84 
        #for j in range(n):
        #    if j!=i:
        #        m[6] += (G*R[j,6])/(np.linalg.norm(R[j,:3]-r)**2)*(R[j,:3]-r)/np.linalg.norm(R[j,:3]-r)
        v    = b[:,:3]-r
        lv   = np.sqrt(np.sum(v**2,axis = 1)).reshape(len(v),1)
        m[6] = np.sum(G*mass/(lv**3)*v,axis = 0)
        
        empty_array[i, :3] = R[i, :3]+5179/57600*time_resoultion*k[0]+7571/16695*time_resoultion*k[2]+393/640*time_resoultion*k[3]-92097/339200*time_resoultion*k[4]+187/2100*t*k[5]+1/40*time_resoultion*k[6]
        empty_array[i,3:6] = R[i,3:6]+5179/57600*time_resoultion*m[0]+7571/16695*time_resoultion*m[2]+393/640*time_resoultion*m[3]-92097/339200*time_resoultion*m[4]+187/2100*t*m[5]+1/40*time_resoultion*m[6]
    # collision
    
    for i in range(n//2+1):
        pos = np.zeros((n,3))
        pos[:, :3]  = empty_array[:, :3]
        rad1  = empty_array[:,7:8]
        
        rad = rad1+rad1[i]
        pos -= pos[i]
        pos *= -1
        
        dis  = np.sqrt(pos[:,0]**2+pos[:,1]**2+pos[:,2]**2).reshape((n,1))
        res  = (dis-rad)[:,0]
        target, = np.where(res<0)
        if len(target)!=0:
            for j in target:      
                if j!=i and np.dot(pos[j],empty_array[i,3:6]-empty_array[j,3:6]) <0: # dot xj-xi vj-vi
                    
                    v1_vertical   = np.dot(empty_array[i,3:6],pos[j]/np.linalg.norm(pos[j]))*(pos[j])/np.linalg.norm(pos[j])
                    v1_horizontal = empty_array[i,3:6]-v1_vertical
                    v2_vertical   = np.dot(empty_array[j,3:6],pos[j]/np.linalg.norm(pos[j]))*(pos[j])/np.linalg.norm(pos[j])
                    v2_horizontal = empty_array[j,3:6]-v2_vertical

                    v1_vertical_fn = (e*empty_array[j,6]*(v2_vertical-v1_vertical)+empty_array[i,6]*v1_vertical+empty_array[j,6]*v2_vertical)/(empty_array[i,6]+empty_array[j,6])
                    v2_vertical_fn = (e*empty_array[i,6]*(v1_vertical-v2_vertical)+empty_array[i,6]*v1_vertical+empty_array[j,6]*v2_vertical)/(empty_array[i,6]+empty_array[j,6])
                    
                    empty_array[i,3:6] = v1_vertical_fn+v1_horizontal
                    empty_array[j,3:6] = v2_vertical_fn+v2_horizontal     

#%%

def frame(): #用於計算
    
    #global G
    #global time_resoultion
    #global e
    
    global R,empty_array     
    algorithm(R,empty_array)#,G,time_resoultion,e)
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
#繪圖
def update_graph(t):
    graph._offsets3d = (R_datas[t,:,0],R_datas[t,:,1],R_datas[t,:,2])
fig   = plt.figure()
ax    = fig.add_subplot(111, projection='3d')
ax.set_axis_on()
graph = ax.scatter(R_datas[0,1:,0],R_datas[0,1:,1],R_datas[0,1:,2],c = 'k')
ax.set_xlim(-1000,1000)
ax.set_ylim(-1000,1000)
ax.set_zlim(-1000,1000)
ani = a.FuncAnimation(fig, update_graph,simulation_frame, 
                               interval=1, blit=False, repeat =True)
