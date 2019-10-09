import cv2
import numpy as np
import math
from Setup import *


sleep(1) #delay for hardware setup
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    src = frame.array
       
    #User code start here
    cv2.imshow("Frame", src)
    if isBut1():
        setLED1(1);
        setSpeed(50)
    if isBut2():
        setLED2(1);
        setHeadlight(1);
    #User code end
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # --------------------- Exit Program ---------------------
    if isBut3():
       break
    # IMPORTANT when compete remember to remove or comment 2 lines below to improve performance
    if cv2.waitKey(1) == 27: #ESC key = 27
       break
    
cv2.destroyAllWindows()
setLED1(0)
setLED2(0)
setLED3(0)
setBuzzer(0)
setHeadlight(0)
setSpeed(0)