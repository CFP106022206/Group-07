#   Vpython Graphing Tool
#   Version 2.0
#   Create by Richard 2019/6/13 16:29

from vpython import *
from PIL import ImageGrab
from subprocess import call
import numpy as np
import math
import os

from colorama import init, Fore, Back, Style 
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

#-----------------------------Input RawData path----------------------------
ini_data = np.load(r'C:\xxxx.npy')
raw_data = np.load(r'C:\xxxxx.npy')


NUM_raw_data_frame = raw_data.shape[0] 
NUM_raw_data_particals = raw_data.shape[1] 
NUM_raw_data_coordinate = raw_data.shape[2] 
#-------------------------------Setting----------------------------------------
#-------Display---------

Particle_color = vector(51/255,1,185/255)     #particle color
Particle_color2 = vector(171/255,35/255,250/255)
Particle_color3 = vector(250/255,164/255,35/255)
Particle_color4 = vector(250/255,32/255,17/255)

Star_Light = True                

Distance_Light = False            
Center_Light = False              
C_Lamp_Color = color.red        

Show_Trail = True                
Trail_Type = str("points")        
Trail_Length = 600             
Trail_Interval = 1            
Trail_Color = vector(185/255,185/255,185/255)          

Center_Object_Mode = True       

Collide_mode = True           
Collide_Moment = 600          

Axis_anable = False              
Axis_color = color.red           
Axis_Length = 10000              
Axis_Radius = 200                 

#-------Animation set--------

Set_Rate =1000                    

Grab_the_Image = True           

Camera_mode = 0          

Follow_Object_NUM = 80 

Surrounding_Period = 14000 

Initial_Camera_pos = vector(6184.62,1173.66,6507.04)      
Initial_Camera_axis = vector(-6184.62,-1173.66,-6507.04)    

#-----------------------------------------------------------------------------------------------------

scene = canvas(title="Group7 - Roche's Limit--洛希极限", width=1230, height=580)


scene.lights = []
if Center_Light == True:
    C_Lamp = local_light(pos=vector(0,0,0),color=C_Lamp_Color)
if Distance_Light == True:                                
    scene.light = [distant_light(direction=vector(0.22, 0.44, 0.88), color=color.gray(0.8)), distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.gray(0.3))] #预设灯光

if Axis_anable == True:
    x_axis = cylinder(pos = vector(0,0,0), axis = vector(Axis_Length,0,0), radius = Axis_Radius, color = Axis_color)
    y_axis = cylinder(pos = vector(0,0,0), axis = vector(0,Axis_Length,0), radius = Axis_Radius, color = Axis_color)
    z_axis = cylinder(pos = vector(0,0,0), axis = vector(0,0,Axis_Length), radius = Axis_Radius, color = Axis_color)

for lp in range(0,NUM_raw_data_particals):
    Particle_Radius = ini_data[lp,7]   
    if Show_Trail == True:
        locals()["partical"+str(lp)] = sphere(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), radius = Particle_Radius, color = Particle_color, make_trail=True, trail_type=Trail_Type, interval=Trail_Interval, retain=Trail_Length, trail_color = Trail_Color)
    else:
        locals()["partical"+str(lp)] = sphere(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), radius = Particle_Radius, color = Particle_color)

    if Star_Light == True:
        locals()["partical"+str(lp)].emissive = True
        locals()["lamp"+str(lp)] = local_light(pos = vector(raw_data[0,lp,0], raw_data[0,lp,1], raw_data[0,lp,2]), color = Particle_color)


if Center_Object_Mode == True:
    locals()["partical"+str(0)].color = color.white
    locals()["partical"+str(0)].texture = textures.granite
    if Star_Light == True:
        locals()["partical"+str(0)].emissive = False  
    

Now_CameraPos = scene.camera.pos 


if Camera_mode == 3:
    scene.camera.pos = Initial_Camera_pos
    scene.camera.axis = Initial_Camera_axis


if Camera_mode == 2:
    scene.camera.follow(locals()["partical"+str(Follow_Object_NUM - 1)])

t = 0


fnum = 0

   
while t < NUM_raw_data_frame:
    rate(Set_Rate)
    
    for lp in range(0,NUM_raw_data_particals):
        locals()["partical"+str(lp)].pos.x = raw_data[t,lp,0]
        locals()["partical"+str(lp)].pos.y = raw_data[t,lp,1]
        locals()["partical"+str(lp)].pos.z = raw_data[t,lp,2]    
        
        if lp >= 1/2*NUM_raw_data_particals: 
            locals()["partical"+str(lp)].color = Particle_color2 
            locals()["partical"+str(lp)].trail_color = Particle_color2 
        
    if Star_Light == True:
        for lp in range(0,NUM_raw_data_particals):
            locals()["lamp"+str(lp)].pos.x = raw_data[t,lp,0]
            locals()["lamp"+str(lp)].pos.y = raw_data[t,lp,1]
            locals()["lamp"+str(lp)].pos.z = raw_data[t,lp,2]
            
            if lp >= 1/2*NUM_raw_data_particals: 
                locals()["lamp"+str(lp)].color = Particle_color2
            
    scene.title = "Group7 - Roche's Limit--洛希极限       Current Time = "+str(t+1)+'s'

    if Camera_mode == 1:
        Main_Radius = ini_data[0,7] 

        if Collide_mode == True:                                       
            Camera_pos = vector((100 + 30*math.sin(6/Surrounding_Period*t))*100*math.sin(2*math.pi/Surrounding_Period*t), 60*Main_Radius*math.sin(5*math.pi/Surrounding_Period*t), -(100 + 30*math.sin(6/Surrounding_Period*t))*100*math.cos(2*math.pi/Surrounding_Period*t))      
        else: 
            Camera_pos = vector((100 + 50*math.sin(10/Surrounding_Period*t))*Main_Radius*math.sin(2*math.pi/Surrounding_Period*t), 20*Main_Radius*math.sin(1.4*math.pi/Surrounding_Period*t), -(100 + 50*math.sin(10/Surrounding_Period*t))*Main_Radius*math.cos(2*math.pi/Surrounding_Period*t))
        scene.camera.pos = Camera_pos   
        scene.camera.axis = -Camera_pos 

    #----PIL Grab----
    if Grab_the_Image == True:
        if t > 1 and t%1 == 0 :

            im = ImageGrab.grab(bbox = (10,121,10+1535,121+753))
            im_num = '00' + repr(fnum)
            im.save('img-' + im_num[-4:]+'.gif')
            fnum += 1
    t += 1




if Grab_the_Image == True:
    print(zi_color.green('\n\nImage Output: '), zi_color.yellow('ON\n'))
else:
    print(zi_color.green('\n\nImage Output: '), zi_color.blue('OFF\n'))

print(zi_color.green('Final Camera Position: '), scene.camera.pos)
print(zi_color.green('Final Camera Orientation: '), scene.camera.axis)

print(zi_color.yellow('\n----  Graph Completed  ----\n'))