# Group-07

## Members and division of work<br/>
1. 王一晨 106022212：Main Code Construction / Calculation of collision and gravity<br/>
2. 陳重名 106022206：Visualization<br/>
3. 林彥興 106020008：Main Code Construction / Scientific Analysis<br/>
4. 呂長益 106022109：Art Supporter / Theoretical analyze<br/>
5. 黃禕煒 x1072165：Art Supporter / Calculation of Collision and Gravity<br/>
6. 陳重衡 106020087：Initial condition generation<br/><br/>

## Title <br/>
Numerical Simulation of the Tidal Effect on small body inside Roche limit<br/><br/>

## What is Roche Limit <br/>
The distance within which a celestial body, held together only by its own gravity, will disintegrate due to a second celestial body's tidal forces exceeding the first body's gravitational self-attraction.<br/>
--Wiki<br/>
In the following introduction, we will use "Main Body" as the heavier central body, and "Small Body" as the small celestial body that would be destroy by the tiday force.
<br/><br/>

## Goal <br/>
模擬小天體接近大天體洛希極限時會如何在潮汐力的作用下解體。<br/>
探討小天體的質量、密度與黏滯性等特性如何影響解體過程。<br/>
Simulate the destruction process of the small body when it comes inside Roche limit.<br/>
Discuss how would density, mass, distance, and other variables influence the process.<br/><br/>

## Simulation Method <br/>
以多個具有質量與體積的小粒子組合為小天體，粒子間具有重力交互作用，並會發生非彈性碰撞。給定初始條件後即可觀察結果。<br/>
Algorithm for calculation of gravity and collision: Runge-Kutta methods
https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
<br/><br/>

## Important functions that has to be construct <br/>
1. 初始條件的給定 Giving initial condition
2. 粒子間與主星體的重力交互作用 Gravity
3. 粒子間非彈性碰撞 Inelastic Collision
4. 動畫繪製 Animation<br/><br/>

## Final Project Briefing (PPT) <br/>
https://onedrive.live.com/view.aspx?resid=71703B636B6F91B5!14452&ithint=file%2cpptx&authkey=!AN6ia9tUKMHqf5I
<br/><br/>

## Final Presentation PPT
https://1drv.ms/p/s!ArWRb2tjO3BxgP5lsV84oj4M-0eUlA?e=bPfCDU
<br/><br/>

## How to run the code
Algorithm<br/>
1. Check the enviroment<br/>
(a) run Final_Project_Main_Code.py<br/>
case1 : program works well. You don't need to read this anymore! Just run it and have fun.<br/>
case2 : Error: test cannot find....<br/>
  This is because the enviroment doesn't support to run Cython and C. Make sure you had install Cython and Visual Studio.<br/>
(b) Or you can dowload the package here:<br/>
  https://drive.google.com/open?id=1ZMO0dPUJR1jgOTxViZA_03Wyuc9u6RRm
2. How to use the package<br/>
  (a) If you want to see the sphere distributed particle, use algorithm file. Click at algorithm.exe and key in some parameters.<br/>
  (b) If you want to see any other case. Please build the initial.npy frist and put it in the algorithm1 fold and run algorithm1.exe
3. What does initial.npy looks like?<br/>
  It is n * 8 matrix. Each column represents  x y z vx vy vz mass radious
4. Output<br/>
  Both algorithm.exe and algorithm1.exe will output result.npy. It is m * n * 3 matrix. m for each simulation frames, n for number of particles and 3 for x,y,z.
</br></br>

## Scientific Research <br/>
We want to know the destruction process of the small body. To do this, we have to come up with a way to quantify the "Destruction level". The way we do this is by calculating the position of the center of mass of the small body. </br><br>
If the small body is compact, the position of it's C.o.M. should be equal to the orbital radius. If it is totally destroyed and formed a ring, C.o.M. should be at the center of the ring. Using this method, we can quantify the destruction level and do the analysis.
We define if the C.o.M position is smaller than 0.2 orbital radius, the small body is "Destroyed".</br></br>
To simplfy the condition, we set the small body on a circular orbit around the main body.</br></br>

### Research for the relation between distance and destruction time <br/>
In theory, we expect that the destruction time will diverge to infinity when the distance comes close to the Roche limit. But what is the relation between distance and destruction time within the Roche limit? That's what we want to find out in this research.<br/>
#### Method
1. Calculate the destruction time for the small body for distance from 1000 to 6000.
2. Plot the result and analyze their relation. Fit with y = a * t ^ b + c.
#### Result
![image](https://github.com/CFP106022206/Group-07/blob/master/final_linear.png)
<br/>
#### Discussion
Surprisingly, we found that in the distance range from 1000 to 6000, the time it takes to destroy the small body is proportional to the distance to the power of 2.5. Which is an interesting result.<br/>
We tried to use some rough idea to derive the power of 2.5 in the result. The details can be found in the PPT of our final presentation.
<br/>
<br/>

### Research for the relation between radius of the small body and destruction time <br/>
The radius of the small body will influence how strong the small body could gravitationally bond itself together. In this research, we want to find out the relation between radius of the small body and destruction time.
#### Method
1. Set the distance between Main and small body to be 1500.
2. Calculate the destruction time for the small body for r from 100 to 500.
3. Plot the result and analyze their relation. Fit with y = a * t ^ -b + c.
#### Result
![image](https://github.com/CFP106022206/Group-07/blob/master/Destruction%20time%20-%20Radius%20Relation.png)
#### Discussion
We can see that this result doesn't fit with a power law curve as good as the previous one. And we are still thinking about the science and mechanism behind it.

## Coding with numba(2019/7/18 update)
`numba_blackmagic.py` is using numba to achieve parallel and vectorization calculation, which can calculate more efficiently.
Althought numba would need more time to compile when the function is called at first, it still save a lot of time with the large particles simulation.
### How to use numba
1. Add `@njit(parallel = True)` before the function.
2. Change `for i in range`  into  `for i in prange` if the algorithm can be parallel computing.
3. Make sure that the version of Numba is higher then 0.40.0 .
### Comparison (1000 particles  20 frames) (without compile)
| Method                    | Time Used(sec)| 
| ------------------------- |---------:|
| Pure python(no module)    | 2437.1225 |
| Wapper C with Cython      |   48.2399 |
| Numpy + vectorization     |   16.8510 |
| Numba(2 cores  4 threads) |    7.2422 |
| Numba(6 cores 12 threads) |    5.3497 |
| Numba(6C12T order = 'C')  |    5.0016 |
`The algorithm only makes gravitational calculation parallel compute`
