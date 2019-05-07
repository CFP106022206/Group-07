# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:25:19 2019

@author: Julius 本機
"""

import imageio #Making videos
import os
import time

start = time.time()

fileList = []
for file in os.listdir('C:/Users/林彥興/.spyder-py3/Computation of physics/Final Project/frame_Earth_far/'):
    if file.startswith('Roche_limit_'):
        complete_path = 'C:/Users/林彥興/.spyder-py3/Computation of physics/Final Project/frame_Earth_far/' + file
        fileList.append(complete_path)

writer = imageio.get_writer('Roche_limit_Earth_circular.mp4', fps=20)

t = 0

for im in fileList:
    writer.append_data(imageio.imread(im))
    t += 1
    print(t)

writer.close()

end = time.time()

print('Saving time: ' + str(end-start))

