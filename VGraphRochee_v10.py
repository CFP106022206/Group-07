#   Vpython Graphing Tool
#   Version 1.0
#   Create by Richard 2019/6/3 00:44

from vpython import *
from PIL import ImageGrab
from subprocess import call
import numpy as np
import math
import os

#-----------------------------Paste your RawData path here----------------------------
raw_data = np.load(r'xxx\xxx\xxx\xxx.npy')
NUM_raw_data_frame = raw_data.shape[0]
NUM_raw_data_particals = raw_data.shape[1]
NUM_raw_data_coordinate = raw_data.shape[2]

#----------------------------Display setting--------------------------

Particle_Radius = 30             #Particle Radius

Particle_color = vector(51/255,1,185/255)      #Particle color
Particle_color2 = vector(171/255,35/255,250/255)
Particle_color3 = vector(250/255,164/255,35/255)
Particle_color4 = vector(250/255,32/255,17/255)

Star_Light = True                #starLight Mode, all particles have light emitting

Distance_Light = False            #background Light (parallel light source)
Center_Light = False              #Center light (radial light source)
C_Lamp_Color = color.red          #Center light color

Show_Trail = True                 #enable Trail
Trail_Type = str("points")        #Trail type (curve/points)
Trail_Length = 130             #Trail length
Trail_Interval = 1            #Trail fineness
Trail_Color = vector(185/255,185/255,185/255)          #Trail color

Center_Object_Mode = True       #Display main object
C_Particle_Radius = 10000         #Main object radius


Axis_anable = False              #Enable Axis
Axis_color = color.red           #Axis color
Axis_Length = 10000              #Axis length
Axis_Radius = 200                #Axis thickness  

#------------------------Effect setting---------------------------

Set_Rate = 40                    #The real animation speed is depend on the computing power, this value only determine the upper bound

Grab_the_Image = False           #Output Image or not？

Camera_mode = 2          # 0-Set the camera position/ 1-Camera rounding mode / 2-Tracing mode

Initial_Camera_pos = vector(6184.62,1173.66,6507.04)      #Enter the initial position if you have chosen 0 mode
Initial_Camera_axis = vector(-6184.62,-1173.66,-6507.04)     #Enter the initial axis if you have chosen 0 mode

Follow_Object_NUM = 10 #Enter the sequence number you want to trace if you have chosen 2 mode

Surrounding_Period = 2500 #Enter the camera cycling time if you have chosen 1 mode

#-----------------------------------------------------------------------------------------------------
from colorama import init, Fore, Back, Style

init(autoreset=True)
class Colored(object):
    def red(self, s):
        return Fore.RED + s + Fore.RESET
zi_color = Colored()
scene = canvas(title="Group7 - Roche's Limit--洛希极限", width=1230, height=580)
scene.lights = []

if Distance_Light == True:                            
    scene.light = [distant_light(direction=vector(0.22, 0.44, 0.88), color=color.gray(0.8)), distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.gray(0.3))] #预设灯光

if Axis_anable == True:
    x_axis = cylinder(pos = vector(0,0,0), axis = vector(Axis_Length,0,0), radius = Axis_Radius, color = Axis_color)
    y_axis = cylinder(pos = vector(0,0,0), axis = vector(0,Axis_Length,0), radius = Axis_Radius, color = Axis_color)
    z_axis = cylinder(pos = vector(0,0,0), axis = vector(0,0,Axis_Length), radius = Axis_Radius, color = Axis_color)

for lp in range(0,NUM_raw_data_particals):
    if Show_Trail == True:
        locals()["partical"+str(lp)] = sphere(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), radius = Particle_Radius, color = Particle_color, make_trail=True, trail_type=Trail_Type, interval=Trail_Interval, retain=Trail_Length, trail_color = Trail_Color)
    else:
        locals()["partical"+str(lp)] = sphere(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), radius = Particle_Radius, color = Particle_color)

    if Star_Light == True:
        locals()["partical"+str(lp)].emissive = True
        locals()["lamp"+str(lp)] = local_light(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), color = Particle_color)

if Center_Light == True:
    C_Lamp = local_light(pos=vector(0,0,0),color=C_Lamp_Color)

if Center_Object_Mode == True:
    locals()["partical"+str(0)].radius = C_Particle_Radius
    locals()["partical"+str(0)].color = color.white
    locals()["partical"+str(0)].texture = textures.granite
    #earthlabel = label(pos= locals()["partical"+str(0)].pos , text='Earth', xoffset=50, yoffset=32, space= 100, height=30, border=10,font='sans')
    if Star_Light == True:
        locals()["partical"+str(0)].emissive = False

if Camera_mode == 0:
    scene.camera.pos = Initial_Camera_pos
    scene.camera.axis = Initial_Camera_axis
elif Camera_mode == 2:
    scene.camera.follow(locals()["partical"+str(Follow_Object_NUM - 1)])

t = 0
fnum = 0
while t < NUM_raw_data_frame:
    rate(Set_Rate)
    
    for lp in range(0,NUM_raw_data_particals):
        locals()["partical"+str(lp)].pos.x = raw_data[t,lp,0]
        locals()["partical"+str(lp)].pos.y = raw_data[t,lp,1]
        locals()["partical"+str(lp)].pos.z = raw_data[t,lp,2]    

    if Star_Light == True:
        for lp in range(0,NUM_raw_data_particals):
            locals()["lamp"+str(lp)].pos.x = raw_data[t,lp,0]
            locals()["lamp"+str(lp)].pos.y = raw_data[t,lp,1]
            locals()["lamp"+str(lp)].pos.z = raw_data[t,lp,2]
    scene.title = "Group7 - Roche's Limit--洛希極限       Current Time = "+str(t+1)+'s'

    if Camera_mode == 1:
        Camera_pos = vector((14 + 8*math.sin(10/Surrounding_Period*t))*C_Particle_Radius*math.sin(2*math.pi/Surrounding_Period*t), 6*C_Particle_Radius*math.sin(1.4*math.pi/Surrounding_Period*t), -(14 + 8*math.sin(10/Surrounding_Period*t))*C_Particle_Radius*math.cos(2*math.pi/Surrounding_Period*t))
        scene.camera.pos = Camera_pos
        scene.camera.axis = -Camera_pos

    if Grab_the_Image == True:
        if t > 1 and t%1 == 0 : 
            #im = ImageGrab.grab(bbox=(10,121,1800,1200))
            im = ImageGrab.grab(bbox = (10,121,10+1535,121+753))
            im_num = '00' + repr(fnum)
            #im.save(os.path.join(r'C:\Users\richa\Documents\Code\User\Python\Course_Final_Project_Grape7\Result_Picture\\',os.path.basename()))
            im.save('img-' + im_num[-4:]+'.png')
            fnum += 1
    t += 1

print(scene.camera.pos)
print(scene.camera.axis)

print(zi_color.red('----# Graph Completed #----'))