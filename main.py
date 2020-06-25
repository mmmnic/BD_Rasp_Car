from Setup import *

def nothing(x):
   pass

'''
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
'''

def process(frame):
    frame = cv2.resize(frame, (320, 180))  
    frame = frame[90:160, 0:320]
    ##### Tracking bar ######
    '''l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")'''
    #lower = np.uint8([l_h, l_s, l_v])
    #upper = np.uint8([u_h, u_s, u_v])
    lower = np.uint8([0, 0, 140])
    upper = np.uint8([180, 100, 255])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask = white_mask)

    ################ Detect lane #################
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray , 180, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('thresh_hold', thresh)
    ima, contours, hier = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    sum_cx = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        print("area: ", area)
        if area < 11000:
         continue
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
        M = cv2.moments(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        sum_cx = sum_cx + cx
        count = count + 1
    if count > 0:
        X = sum_cx / count
        cv2.circle(frame ,(int(X), 20), 10, (0,0,255), -1)
        angle = GetAngle(X)
        speed = GetSpeed(angle)
        
        print('Angle: ', angle)
        print('Speed: ', speed)
        
        setTurn(angle)
        setSpeed(speed)
    cv2.imshow('contour', frame)

# ------------------------------------------ MAIN ------------------------------------------ #
                    # --------------------- GUIDE --------------------- #
                    # Press button 1 to start running
                    # Press button 2 or ESC to stop running and wait for next button
                    # Press button 3 to stop program
def main():
    print("Main")
    while(1):
        setLED1(1)
        setLED3(1)
        if isBut1():
            setLED1(0)
            setLED2(1)
            setLED3(0)
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                #User code start here
                process(image)
                cv2.imshow("Frame", image)
                #User code end
                rawCapture.truncate(0)              # clear the stream in preparation for the next frame
                cv2.waitKey(1)
                # --------------------- Exit Program ---------------------
                if isBut2():
                    setAllDeviceToZero()
                    cv2.destroyAllWindows()
                    break
        if isBut3(): # Button 3 to stop program
            break
    setAllDeviceToZero()
    cv2.destroyAllWindows()
    motor.stop()
    servo.stop()
    
if __name__ == "__main__":
   main()