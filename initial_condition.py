# -*- coding: utf-8 -*-
"""
log
2019/05/10  01:02 修改者：王一晨
    刪除r3變量，因為會形成4層結構
    新增position
    改速度以向量輸入
    設定默認值
    優化函數
    新增錯誤輸入提示
"""

import numpy as np
def initial_condition_generater(vel,d1,d2,d3,r1,r2,r,a,n,position=[0,0,0],m_max=10**6):

    #vel      質心速度[vx,vy,vz]
    #d1 最內層的地殼密度/或最內區質點的質量
    #d2 中層地殼密度/或中層質點的質量
    #d3 最外側地殼密度/或最外質點的質量
    #r1,r2 各層地殼距離中心距離
    #r 小行星球形分佈半徑
    #a每質點動量交換半徑 默認為碎片半徑  因此我們在下面會帶入  4/3*a^3*np.pi*r^3*d(i)=mass
    #n質點個數
    #position 質心位置[x,y,z] 默認[0,0,0]
    #m_max 每片質量 默認10**6
    
    
    if  m_max<=4/3*a**3*np.pi*max(d1,d2,d3) :
        raise ValueError("input maxium mass/density ilegal")
        #print(str(m_max)+' and '+str(4/3*a**3*np.pi*max(d1,d2,d3)))
    if r1>=r2 or r2>=r: 
        raise ValueError("input ilegal !!\n r1 should bigger than r2 and r2 should bigger than r")
    if a<=1 :
        raise ValueError("particle radius too small!!\n should bigger than 1")
        
    
    coor_trans = np.zeros((n,3))
    coor_trans[:,0] = r
    coor_trans[:,1] = np.pi
    coor_trans[:,2] = 2*np.pi
    R=np.zeros((n,8))
    R[:,7]  =a
    R[:,3:6]=vel
    spherical = np.random.rand(n,3)*coor_trans


    R[:,0] = spherical[:,0]*np.sin(spherical[:,1])*np.cos(spherical[:,2])
    R[:,1] = spherical[:,0]*np.sin(spherical[:,1])*np.sin(spherical[:,2])
    R[:,2] = spherical[:,0]*np.cos(spherical[:,1])

    del coor_trans,spherical
    
    for i in range(n):    
        if   np.linalg.norm(R[i,:3])<=r1:
            R[i,6]=4/3*np.pi*a**3*d1
        elif np.linalg.norm(R[i,:3])<=r2:
            R[i,6]=4/3*np.pi*a**3*d2
        else:
            R[i,6]=4/3*np.pi*a**3*d3

    R[:,:3] += position
    return R
#a = initial_condition_generater([10,10,10],10**1.12,10**1.45,10**1.65,50,100,200,10,70) 
