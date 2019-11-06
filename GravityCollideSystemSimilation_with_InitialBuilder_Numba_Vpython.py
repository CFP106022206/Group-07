'''
TO SUCESSFULLY RUN THIS VERSION
YOU NEED TO HAVE ANACONDA WITH PYTHON3

AND TO ENSURE YOU HAVE DONE THESE SEVERAL INSTALLATION:
pip install vpython             //FOR THE ANIMATION AND GRAPHS
pip install mss                 //FOR GRABBING THE SCREENSHOT
pip install imageio-ffmpeg      //TO PRODUCE THE FINAL MP4 FILE
pip install progressbar2        //FOR THE PROGRESSBAR DISPLAY

PLEASE REMEMBER TO CHANGE THE PATH OF SAVING FILES ACCORDING TO YOUR COMPUTER'S SITUATION

注意，请确认Vpython中Grab的图片存放位置（通常是运行python文件的目录）并更改mp4_maker下的文件路径才能使mp4_maker正常运作。
已关闭所有np.save

若要使用mp4_maker 在vpython启动浏览器运行完毕以后不要关闭浏览器，否则会导致程序中断。
请直接回到编译器中继续操作（输入1启动 mp4_maker）
Vpython中抓截图的速度很快，若电脑速度慢可能会导致前几张截图时还在开启浏览器的白画面。在启动mp4 maker（输入1）前可以先到目标资料夹确认
2019/11/6
'''

import numpy as np
import math
from numba import njit, prange
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as a
import matplotlib.pyplot as plt

from vpython import *
import mss
import mss.tools

import imageio #Making videos
import os

import time
from progressbar import * #進度條,使用pip install progressbar2

from colorama import init, Fore, Back, Style #测试终端字体颜色
init(autoreset=True)
class Colored(object):
    def green(self, s):
        return Fore.GREEN + s + Fore.RESET
    def red(self, s):
        return Fore.RED + s + Fore.RESET
    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET
    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET
    def cyan(self, s):
        return Fore.CYAN + s + Fore.RESET   
zi_color = Colored()

#------設定每個小粒子參數------
n = 100 #Particle's amount
M = 10**10 #Mass of one particle
particle_radii = 70 #每個小粒子的半徑
seperate_pos = [0,5000,0] #小粒子團初始位置
r = 10  #初始情況下小粒子的球型扩散半徑

v_x = 11.54 #給定小粒子初始x方向速度
v_y = 0 #給定小粒子初始y方向速度
v_z = 0 #給定小粒子初始z方向速度

#------設定中心天體參數------
M_Center = 10**16 #中心天體质量
Center_Radius = 1000 #中心天體半徑

#------常數/係數/參數設定------
G = 6.67*10**-11   #Gravitational constant
e = 0.9            #coefficient of restitution

simulation_frame = 4000
time_resoultion = 1

#-----------------------Vpython動畫設定------------------------
#-------显示设置---------
Center_Object_Mode = True #False       #是否有中央主星？若为两团质点对撞请关闭。

Particle_color = vector(51/255,1,185/255)     #调整粒子颜色(双色)
Particle_color2 = vector(171/255,35/255,250/255)

Show_Trail = True                #尾迹是否可视化？
Trail_Type = str("points")        #尾迹形态(curve/points)
Trail_Length = 40             #尾迹长度
Trail_Interval = 2            #尾迹取点间隔，数值大造成曲线变成折线
Trail_Color = vector(185/255,185/255,185/255)          #尾迹颜色

#-------自行定义画布大小--------
scene = canvas(title="Group7 - Roche's Limit--洛希极限", width=1420, height=700)

#-------动画设置---------
Grab_the_Image = True           #是否启动ImageGrab？

Camera_mode = 0          # 0-相机预设位置/ 1-环绕模式/ 2-追踪模式/ 3-相机指定位

Follow_Object_NUM = 80 #追踪第？个粒子（非追踪模式时不必设定）

Surrounding_Period = 15000 #环绕周期(秒)（非环绕模式时不必设定）

Initial_Camera_pos = vector(6184.62,1173.66,6507.04)      #相机初始位置（非相机指定位模式时不必设定）
Initial_Camera_axis = vector(-6184.62,-1173.66,-6507.04)     #相机初始视角（非相机指定位模式时不必设定）

Set_Rate =1000                    #动画帧率(此数值为设定上限，若高于电脑计算速度则显示速度取决于计算速度)
#-------以下为不常用设置--------
Star_Light = True                #星光模式,光频跟粒子颜色相同

Distance_Light = False            #是否开启环绕灯
Center_Light = False              #是否开启中心灯
C_Lamp_Color = color.red         #中心灯光颜色

Collide_mode = False           #对撞模式
Collide_Moment = 600          #对撞帧

Axis_anable = False              #是否开启坐标轴？
Axis_color = color.red           #坐标轴颜色
Axis_Length = 10000              #坐标轴长度
Axis_Radius = 200                #坐标轴粗细  


#----------------------------Build_Initial_Condition.py------------------------------

#R is the main array that stores the 3D position and velocity of the particles
R = np.ones((n,8)) #建构n行8列都是1的矩阵
R.astype('float64')
R = R.copy(order='C') #Make sure it works in C, dark magic

#給定 Initial Condition
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
R[:,0:3] += seperate_pos
#R[:,0:3] += [0,1234186562*0.7,0]

#給定速度(等速前進)
R[:,3] *= v_x
R[:,4] *= v_y
R[:,5] *= v_z
R[:,6] *= M #粒子質量
R[:,7] *= particle_radii #粒子半徑

#Center Mass
R[0,0:6] = 0
R[0,6] = M_Center #中心質量
R[0,7] = Center_Radius #695510000 #中心半径

#np.save(r'/Users/richard/Documents/VS_Code/Grape7_Final/initial.npy',R)
print(zi_color.yellow('\n\n---- Build I.C. completed ----\n'))

#-------------------------------numba_blackmagic.py---------------------------------
"""
Created on Tue Jul 16 22:19:03 2019

@author: 王一晨
"""
#%%
#R is the main array that stores the 3D position and velocity of the particles
#R = np.load(r'/Users/richard/Documents/VS_Code/Grape7_Final/initial.npy')
#This is an array that is used for the C module
empty_array = np.empty_like(R)
empty_array = empty_array.copy(order='C')

#%%
n = np.shape(R)[0]
R_datas = np.zeros((simulation_frame,n,3))
R_datas[0,:,:3] = R[:,:3] #儲存所有frame的位置資訊
print('Simulation frame = ',simulation_frame, zi_color.yellow('\n正在编译中... \n\n'))

#%% 
# gravity
@njit(parallel=True)
def gravity(R,empty_array):
    empty_array[:,6:] = R[:,6:]
    global n,G,time_resoultion
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
@njit(parallel=True)
def collition(empty_array):
    global n,e
    check_list = np.zeros((n,3))
    
    center = np.zeros(3)
    center[0] = np.mean(empty_array[:,0])
    center[1] = np.mean(empty_array[:,1])
    center[2] = np.mean(empty_array[:,2])
    
    for i in prange(n):
        for j in prange(3):
            if empty_array[i,j] >= center[j]:
                check_list[i,j] = 1
    
    region = check_list[:,0]*4 + check_list[:,1]*2 + check_list[:,2]
    
    for k in prange(8):
        reg = empty_array[region == k]
        ta, = np.where(region == k)
        if len(reg)>1:
            for i in range(len(reg)):
                pos = np.zeros((len(reg),3))
                pos[:, :3]  = reg[:, :3]
                rad1  = reg[:,7:8]
                
                rad = rad1+rad1[i]
                pos -= pos[i]
                pos *= -1
                
                dis  = np.sqrt(pos[:,0]**2+pos[:,1]**2+pos[:,2]**2).reshape((len(reg),1))
                res  = (dis-rad)[:,0]
                target, = np.where(res<0)
                
                if len(target)!=0:
                    for j in target:      
                        if j!=i and np.dot(pos[j],reg[i,3:6]-reg[j,3:6]) <0: # dot xj-xi vj-vi
                            
                            v1_vertical   = np.dot(reg[i,3:6],pos[j]/np.linalg.norm(pos[j]))*(pos[j])/np.linalg.norm(pos[j])
                            v1_horizontal = reg[i,3:6]-v1_vertical
                            v2_vertical   = np.dot(reg[j,3:6],pos[j]/np.linalg.norm(pos[j]))*(pos[j])/np.linalg.norm(pos[j])
                            v2_horizontal = reg[j,3:6]-v2_vertical
            
                            v1_vertical_fn = (e*reg[j,6]*(v2_vertical-v1_vertical)+reg[i,6]*v1_vertical+reg[j,6]*v2_vertical)/(reg[i,6]+reg[j,6])
                            v2_vertical_fn = (e*reg[i,6]*(v1_vertical-v2_vertical)+reg[i,6]*v1_vertical+reg[j,6]*v2_vertical)/(reg[i,6]+reg[j,6])
                            
                            reg[i,3:6] = v1_vertical_fn+v1_horizontal
                            reg[j,3:6] = v2_vertical_fn+v2_horizontal 
            
            for number in range(len(ta)):
                empty_array[ta[number],:] = reg[number,:]
#%%

def frame(): #用於計算
    global R,empty_array     
    gravity(R,empty_array)#,G,time_resoultion,e
    collition(empty_array)
    R = empty_array
    
def store(t): #用於儲存不同時間的位置資訊
    global R_datas
    global R
    R_datas[t,:,:3] = R[:,:3]

#%%
widgets = ['Progress:  ',Percentage(), '   ', Bar('#'),'    ', Timer(),'    ', ETA(),'    ',FileTransferSpeed()]#进度条屬性
pBar = ProgressBar(widgets= widgets, maxval=10*simulation_frame+1).start() #进度条
for t in range(1,simulation_frame): #執行主程式
    frame()
    store(t)
    pBar.update(10*t + 1) #讓一開始的進度條顯示1而不是顯示空
    #print(t)
pBar.finish()#結束進度條
#%%
#繪圖
'''
def update_graph(t):
    graph._offsets3d = (R_datas[t,:,0],R_datas[t,:,1],R_datas[t,:,2])
fig   = plt.figure()
ax    = fig.add_subplot(111, projection='3d')
ax.set_axis_on()
graph = ax.scatter(R_datas[0,1:,0],R_datas[0,1:,1],R_datas[0,1:,2],c = 'k')
ax.set_xlim(-1000,1000)
ax.set_ylim(-1000,1000)
ax.set_zlim(-1000,1000)
ani = a.FuncAnimation(fig, update_graph,simulation_frame, interval=1, blit=False, repeat =True)
'''
# %%
#np.save(r'/Users/richard/Documents/VS_Code/Grape7_Final/result.npy',R_datas)
print(zi_color.green('\n---- Complete the Algorithm     Result Saved----\n\n'))

#-------------------------------------Vpython--------------------------------------------
#------输入RawData文件名(已更改)------
ini_data = R
raw_data = R_datas
'''
ini_data = np.load(r'/Users/richard/Documents/VS_Code/Grape7_Final/initial.npy')
raw_data = np.load(r'/Users/richard/Documents/VS_Code/Grape7_Final/result.npy')
'''

NUM_raw_data_frame = raw_data.shape[0] #时刻数（阵列层数）
NUM_raw_data_particals = raw_data.shape[1] #粒子总数（行数）
NUM_raw_data_coordinate = raw_data.shape[2] #x,y,z （维数）

#-------改变预设灯光--------
scene.lights = []
if Center_Light == True:
    C_Lamp = local_light(pos=vector(0,0,0),color=C_Lamp_Color)
if Distance_Light == True:                                   #开启环绕灯光效果
    scene.light = [distant_light(direction=vector(0.22, 0.44, 0.88), color=color.gray(0.8)), distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.gray(0.3))] #预设灯光

#--------建立坐标轴---------
if Axis_anable == True:
    x_axis = cylinder(pos = vector(0,0,0), axis = vector(Axis_Length,0,0), radius = Axis_Radius, color = Axis_color)
    y_axis = cylinder(pos = vector(0,0,0), axis = vector(0,Axis_Length,0), radius = Axis_Radius, color = Axis_color)
    z_axis = cylinder(pos = vector(0,0,0), axis = vector(0,0,Axis_Length), radius = Axis_Radius, color = Axis_color)

#--------建立初始位置---------
for lp in range(0,NUM_raw_data_particals):
    Particle_Radius = ini_data[lp,7]    #直接在initial资料矩阵中取得各质点半径。提到前面宣告是因为直接放在下行中好像有问题。
    if Show_Trail == True:
        locals()["partical"+str(lp)] = sphere(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), radius = Particle_Radius, color = Particle_color, make_trail=True, trail_type=Trail_Type, interval=Trail_Interval, retain=Trail_Length, trail_color = Trail_Color)
    else:
        locals()["partical"+str(lp)] = sphere(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), radius = Particle_Radius, color = Particle_color)

    if Star_Light == True:
        locals()["partical"+str(lp)].emissive = True #打开粒子自发光
        locals()["lamp"+str(lp)] = local_light(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), color = Particle_color)

#--------修改中央主星外观-------
if Center_Object_Mode == True:
    #locals()["partical"+str(0)].radius = C_Particle_Radius
    locals()["partical"+str(0)].color = color.white
    locals()["partical"+str(0)].texture = textures.granite
    #earthlabel = label(pos= locals()["partical"+str(0)].pos , text='Earth', xoffset=50, yoffset=32, space= 100, height=30, border=10,font='sans') 
    if Star_Light == True:
        locals()["partical"+str(0)].emissive = False  #中心星球关闭发光
    
#-------读取摄像机默认位置的初始距离-------
Now_CameraPos = scene.camera.pos #环绕模式初始化使用

#--------架设初始摄像机位置--------
if Camera_mode == 3:
    scene.camera.pos = Initial_Camera_pos
    scene.camera.axis = Initial_Camera_axis

#--------开启摄像机跟随模式---------
if Camera_mode == 2:
    scene.camera.follow(locals()["partical"+str(Follow_Object_NUM - 1)])

#------建立初始时间轴参数-------
t = 0

#----初始化抓取帧数序号-----
fnum = 0

#----主循环----    
while t < NUM_raw_data_frame:
    rate(Set_Rate)
    
    for lp in range(0,NUM_raw_data_particals):
        locals()["partical"+str(lp)].pos.x = raw_data[t,lp,0]
        locals()["partical"+str(lp)].pos.y = raw_data[t,lp,1]
        locals()["partical"+str(lp)].pos.z = raw_data[t,lp,2]    
        
        if lp >= 1/2*NUM_raw_data_particals: #双色
            locals()["partical"+str(lp)].color = Particle_color2 #更改粒子颜色
            locals()["partical"+str(lp)].trail_color = Particle_color2 #更改尾迹颜色
        '''
        elif lp%5 == 0:
            locals()["partical"+str(lp)].color = Particle_color3
            locals()["partical"+str(lp)].trail_color = Particle_color3
        elif lp%7 == 0:
            locals()["partical"+str(lp)].color = Particle_color4
            locals()["partical"+str(lp)].trail_color = Particle_color4
        '''
        
    if Star_Light == True:
        for lp in range(0,NUM_raw_data_particals):
            locals()["lamp"+str(lp)].pos.x = raw_data[t,lp,0]
            locals()["lamp"+str(lp)].pos.y = raw_data[t,lp,1]
            locals()["lamp"+str(lp)].pos.z = raw_data[t,lp,2]
            
            if lp >= 1/2*NUM_raw_data_particals: #双色
                locals()["lamp"+str(lp)].color = Particle_color2
            '''
            elif lp%5 == 0:
                locals()["partical"+str(lp)].color = Particle_color3
            elif lp%7 == 0:
                locals()["partical"+str(lp)].color = Particle_color4
            '''
    scene.title = "Group7 - Roche's Limit--洛希极限       Current Time = "+str(t+1)+'s'

    #----开启相机环绕模式-------
    if Camera_mode == 1:
        Main_Radius = ini_data[0,7] #资料库中第一颗星的半径(参考视角距离用)

        if Collide_mode == True:                                       #碰撞模式
            Camera_pos = vector((100 + 30*math.sin(6/Surrounding_Period*t))*100*math.sin(2*math.pi/Surrounding_Period*t), 60*Main_Radius*math.sin(5*math.pi/Surrounding_Period*t), -(100 + 30*math.sin(6/Surrounding_Period*t))*100*math.cos(2*math.pi/Surrounding_Period*t))      
        else: 
            Camera_pos = vector((100 + 50*math.sin(10/Surrounding_Period*t))*Main_Radius*math.sin(2*math.pi/Surrounding_Period*t), 20*Main_Radius*math.sin(1.4*math.pi/Surrounding_Period*t), -(100 + 50*math.sin(10/Surrounding_Period*t))*Main_Radius*math.cos(2*math.pi/Surrounding_Period*t))
        scene.camera.pos = Camera_pos   
        scene.camera.axis = -Camera_pos #锁定视角指向原点

    #----更新 mss Grab----
    if Grab_the_Image == True:
        if t > 1 and t%10 == 0 : #每10时间单位取一帧
            with mss.mss() as sct:
            # The screen part to capture
                monitor = {"top": 60, "left": 5, "width": 1504, "height": 760}
                im_num = repr(fnum) #將對象轉換成對應的字串
                #數字前加零以對齊位數：
                if fnum < 10:
                    z_ord = "0000"
                elif fnum >= 10 and fnum < 100:
                    z_ord = "000"
                elif fnum>= 100 and fnum < 1000:
                    z_ord = "00"
                else:
                     z_ord = ""  # ⚠️ 未測試此行是否正確
                output = z_ord + im_num[-4:] + ".png".format(**monitor)

                # Grab the data
                sct_img = sct.grab(monitor)

                # Save to the picture file
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
                print(output)
            fnum += 1

    t += 1

#若需要调整视角，开启以下内容以获得当前视角资讯

if Grab_the_Image == True:
    print(zi_color.green('Image Output: '), zi_color.cyan('ON\n'))
else:
    print(zi_color.green('Image Output: '), zi_color.blue('OFF\n'))

print(zi_color.green('Final Camera Position: '), scene.camera.pos)
print(zi_color.green('Final Camera Orientation: '), scene.camera.axis)

print(zi_color.yellow('\n----  Graph Completed  ----\n'))

#-----------------------------mp4_maker.py---------------------------
#%%
"""
Created on Mon May  6 21:25:19 2019

@author: Julius 本機
"""
make_mp4 = int(input('make mp4? (Yes: 1)'))
if make_mp4 == 1:
    start = time.time()
    fileList = []
    for file in os.listdir('/Users/richard/Documents/VS_Code/'):
        if file.startswith('0'):
            complete_path = '/Users/richard/Documents/VS_Code/' + file
            fileList.append(complete_path)

    fileList.sort() #20191031 圖片順序混亂問題，重新排列解決。
    writer = imageio.get_writer('Roche_limit_Earth_circular.mp4', fps=30)

    t = 0

    widgets = ['Progress:  ',Percentage(), '   ', Bar('#'),'    ', Timer(),'    ', ETA(),'    ',FileTransferSpeed()]#进度条屬性
    pBar = ProgressBar(widgets= widgets, maxval=10*len(fileList)+1).start() #进度条
    for im in fileList:
        writer.append_data(imageio.imread(im))
        t += 1
        pBar.update(10*t + 1)

    pBar.finish()
    writer.close()

    end = time.time()

    print('\nSaving time: ' + str(end-start),'\n\n')
    print(complete_path)

# %%
