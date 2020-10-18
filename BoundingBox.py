# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 14:50:28 2020
Running the script in the folder containing the images and their masks. 
Change the image_name variable - set the name as (file number - 10) ex. if first file is 000670.png then enter 670-10 = 660
The program will create the csv file named as folder and store [x, y, w, h, cx, cv] for each image in the folder

@author: hitarth
"""


import cv2
import numpy as np
import sys
import pandas as pd
import os
import csv

#name of the first image
image_name = 640

#Create a file to store the masks
with open('{}.csv'.format(os.path.basename(os.getcwd())), 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['File_name', 'x', 'y', 'w', 'h', 'cx', 'cy'])

num_of_files = len([name for name in os.listdir('.') if os.path.isfile(name)])//2

for i in range(num_of_files):
    
    image_name2 = image_name+(10*(i+1))
    prefix1 = '000'
    prefix2 = '00'
    if(image_name2 >= 1000):
        masked_img = cv2.pyrDown(cv2.imread('{}{}_m.png'.format(prefix2, image_name2), cv2.IMREAD_UNCHANGED))
    else:
        masked_img = cv2.pyrDown(cv2.imread('{}{}_m.png'.format(prefix1, image_name2), cv2.IMREAD_UNCHANGED))    
    
    #Calculating contours
    ret, threshed_img = cv2.threshold(cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        x1, y1 = x+w, y+h
        #Center of the bounding box
        cx, cy = (x+x1)/2, (y+y1)/2
        #Data to store        
        df = np.array([x, y, w, h, cx, cy])
        
        #Storing the data into the file in .csv format
        with open('{}.csv'.format(os.path.basename(os.getcwd())), 'a', newline='') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(df)


