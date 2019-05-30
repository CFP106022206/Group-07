# Group-07

## Members <br/>
1. 王一晨 106022212：Main Code Construction / Calculation of collision and gravity<br/>
2. 陳重名 106022206：Visualization<br/>
3. 林彥興 106020008：Main Code Construction / Scientific Analysis<br/>
4. 呂長益 106022109：Art Supporter<br/>
5. 黃禕煒 x1072165：Art Supporter / Calculation of Collision and Gravity<br/>
6. 陳重衡 106020087：Initial Condition generation<br/><br/><br/>


## Title <br/>
Numerical Simulation of the Tidal Effect on small body  Roche limit<br/><br/><br/>

## What is Roche Limit <br/>
The distance within which a celestial body, held together only by its own gravity, will disintegrate due to a second celestial body's tidal forces exceeding the first body's gravitational self-attraction.<br/>
--Wiki<br/>
In the following introduction, we will use "Main Body" as the heavier central body, and "Small Body" as the small celestial body that would be destroy by the tiday force.
<br/><br/>

## Goal <br/>
模擬小天體接近大天體洛希極限時會如何在潮汐力的作用下解體。<br/>
探討小天體的質量、密度與黏滯性等特性如何影響解體過程。<br/>
Simulate the destruction process of the small body when it comes inside Roche limit.<br/>
Discuss how would density, mass, distance, and other variables influence the process.<br/><br/><br/>

## Simulation Method <br/>
以多個具有質量與體積的小粒子組合為小天體，粒子間具有重力交互作用，並會發生非彈性碰撞。給定初始條件後即可觀察結果。<br/>
Algorithm for calculation of gravity and collision: Runge-Kutta methods
https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
<br/><br/><br/>

## Important functions that has to be construct <br/>
1. 初始條件的給定 Giving initial condition
2. 粒子間與主星體的重力交互作用 Gravity
3. 粒子間非彈性碰撞 Inelastic Collision
4. 動畫繪製 Animation<br/><br/><br/>

## Division of work <br/>
主架構：王一晨、林彥興<br/>
演算法：王一晨、黃禕煒<br/>
繪圖與其他：陳重名、呂長益、陳重衡、林彥興<br/><br/>

## Final Project Briefing (PPT) <br/>
https://onedrive.live.com/view.aspx?resid=71703B636B6F91B5!14452&ithint=file%2cpptx&authkey=!AN6ia9tUKMHqf5I
<br/><br/>
## Scientific Research <br/>
### Research for the relation between distance and destruction time
1. Set the distance between Main and small body to be 1500.
2. Calculate the destruction time for the small body for r from 100 to 500.
3. Plot the result and analyze their relation.
<br/>
'''
請各位下載 Main_Code_Circular.py，其中有三個地方需要修改：<br/>
1. distance：小天體與主星之間的距離。目前我是以250為單位增加，已經完成1000-2250。<br/>
2. Simulation_frame：模擬的時間長度。2250以上可能需要10000以上才能夠完成，distance越長，需要的frame越多。這也是需要各位協助的主要原因。<br/>
3. 檔名：最後面的np.save裡面的檔名，請設為'R=xxxx.npy'。<br/>
完成模擬後，請各位將這份.npy檔傳給我。<br/>
分配：(填上自己的名字)<br/>
2500-2750: Jason<br/>
3000-3750: 王一晨<br/>
4000-5000: 王一晨<br/>
'''<br/>
### Reserrch for the relation between radius of the small body and destruction time
1. Set the distance between Main and small body to be 1500.
2. Calculate the destruction time for the small body for r from 100 to 500.
3. Plot the result and analyze their relation.
