# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:25:19 2019

@author: Julius 本機
"""

import imageio #Making videos
import os

fileList = []
for file in os.listdir('C:/Users/林彥興/.spyder-py3/Computation of physics/Final Project/frame/'):
    if file.startswith('Roche_limit_'):
        complete_path = 'C:/Users/林彥興/.spyder-py3/Computation of physics/Final Project/frame/' + file
        fileList.append(complete_path)

writer = imageio.get_writer('test.mp4', fps=20)

for im in fileList:
    writer.append_data(imageio.imread(im))
writer.close()