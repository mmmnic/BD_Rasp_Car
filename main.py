import cv2
import numpy as np
import math
from Setup import *


sleep(1) #delay for hardware setup
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    src = frame.array
       
    #User code start here
    cv2.imshow("Frame", src)
    key = cv2.waitKey(1) & 0xFF
    #User code end
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # exit Program
    #if isBut3:
    #   break
    # --------------------- IMPORTANT ---------------------
    #when compete remember to remove or comment 2 lines below to improve performance
    #if cv2.waitKey(1) == 27: #ESC key = 27
    #    break
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()
setSpeed(0)
