# Group-07

## Members: <br/>
1. 王一晨 106022212<br/>
2. 陳重名 106022206<br/>
3. 林彥興 106020008<br/>
4. 呂長益 106022109<br/>
5. 黃禕煒 x1072165<br/>
6. 陳重衡 106020087 <br/><br/><br/>


## Title: <br/>
Numerical Simulation of the Tidal Effect on small body close to Roche limit<br/><br/><br/>

## What is Roche Limit
The distance within which a celestial body, held together only by its own gravity, will disintegrate due to a second celestial body's tidal forces exceeding the first body's gravitational self-attraction.<br/>
--Wiki<br/><br/><br/>

## Goal
模擬小天體接近大天體洛希極限時會如何在潮汐力的作用下解體。<br/>
探討小天體的質量、密度與黏滯性等特性如何影響解體過程。<br/>
Simulate the destruction process of the small body when it comes close to the Roche limit.<br/>
Discuss how would viscosity, density, mass, and other variables influence the process.<br/><br/><br/>

## Simulation Method
以多個具有質量與體積的小粒子組合為小天體，粒子間具有重力交互作用，並會發生非彈性碰撞。給定初始條件後即可觀察結果。<br/><br/><br/>

## Important functions that has to be construct
1. 初始條件的給定 Giving initial condition
2. 粒子間與主星體的重力交互作用 Gravity
3. 粒子間非彈性碰撞 Inelastic Collision
4. 動畫繪製 Animation<br/><br/><br/>

## Division of work
主架構：王一晨、林彥興<br/>
演算法：王一晨、黃禕煒<br/>
繪圖與其他：陳重名、呂長益、陳重衡、林彥興<br/><br/>

### Final Project Briefing (PPT)
https://onedrive.live.com/view.aspx?resid=71703B636B6F91B5!14452&ithint=file%2cpptx&authkey=!AN6ia9tUKMHqf5I

### Research for the relation between distance and destruction time
請各位下載 Main_Code_Circular.py，其中有三個地方需要修改：<br/>
1. distance：小天體與主星之間的距離。目前我是以250為單位增加，已經完成1000-2250。<br/>
2. Simulation_frame：模擬的時間長度。2250以上可能需要10000以上才能夠完成，distance越長，需要的frame越多。這也是需要各位協助的主要原因。<br/>
3. 檔名：最後面的np.save裡面的檔名，請設為'R=xxxx.npy'。<br/>
完成模擬後，請各位將這份.npy檔傳給我。<br/>
分配：(填上自己的名字)<br/>
2500-2750:<br/>
3000-3750:<br/>
4000-5000:<br/>
