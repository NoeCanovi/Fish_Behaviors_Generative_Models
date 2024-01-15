'''   Extract frames from a video and saved them in folder Frames   '''


'''   imports   '''
import cv2
import numpy as np


vidcap = cv2.VideoCapture("D:/Internship/Step1/Videos/2022/30.06/8/Clips/GH070023/JS_122.2510000000002_127.MP4")

success,image = vidcap.read()
count = 0


while success:

  width = image.shape[1]
  height = image.shape[0]
 
  cv2.imwrite("Clips/Frames/frame%d.jpg" % count, image)     # save frame as JPEG file 
  

  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1

  #if count == 400:
  #  break





