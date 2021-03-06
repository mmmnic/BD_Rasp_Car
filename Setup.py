import cv2
import time
import math
import RPi.GPIO     as GPIO
import numpy        as np
from picamera.array import PiRGBArray
from picamera       import PiCamera
from picamera.array import PiRGBArray
from picamera       import PiCamera
from time           import sleep

# --------------------- DATA THAT CAN CHANGEABLE --------------------- #
y = 180
factor = 2
minsp = 0.2

# --------------------- DO NOT CONFIG BELOW --------------------- #
# set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define parameters
servoFre = 50
motorFre = 120
servoCenterDutyCycle = 7.5
servoMaxDutyCycle = 10.5
servoMaxAngle = 45
servoRatio  = (servoMaxDutyCycle - servoCenterDutyCycle)/servoMaxAngle
#5.5 max left
#10.5 max right
#7.5 center

#define pin
Pin_MOTOR = 2
Pin_GPIO3 = 3
Pin_GPIO4 = 4
Pin_GPIO17 = 17
Pin_GPIO27 = 27
Pin_GPIO22 = 22
Pin_BUT1 = 10
Pin_LED1 = 9
Pin_BUT2 = 11
Pin_LED2 = 0
Pin_BUT3 = 5
Pin_LED3 = 6
Pin_BUZZER = 13
Pin_SERVO = 19
Pin_HEADLIGHT = 26

#Setup pin as output or input
GPIO.setup(Pin_MOTOR, GPIO.OUT)
GPIO.setup(Pin_LED1, GPIO.OUT)
GPIO.setup(Pin_LED2, GPIO.OUT)
GPIO.setup(Pin_LED3, GPIO.OUT)
GPIO.setup(Pin_BUZZER, GPIO.OUT)
GPIO.setup(Pin_SERVO, GPIO.OUT)
GPIO.setup(Pin_HEADLIGHT, GPIO.OUT)
GPIO.setup(Pin_BUT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Pin_BUT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Pin_BUT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Setup PWM for motor and servo
motor = GPIO.PWM(Pin_MOTOR, motorFre)
servo = GPIO.PWM(Pin_SERVO, servoFre)
motor.start(0)
servo.start(servoCenterDutyCycle)
#Global function
def setLED1(Status):
    GPIO.output(Pin_LED1, not(Status))
    return

def setLED2(Status):
    GPIO.output(Pin_LED2, not(Status))
    return

def setLED3(Status):
    GPIO.output(Pin_LED3, not(Status))
    return

def setBuzzer(Status):
    GPIO.output(Pin_BUZZER, not(Status))
    return

def setHeadlight(Status):
    GPIO.output(Pin_HEADLIGHT, Status)
    return

def setSpeed(speed):
    if speed >100:
        speed = 100
    elif speed<0:
        speed = 0
    motor.ChangeDutyCycle(speed)
    return

def setTurn(angle):
    #limit turn angle
    if (angle > servoMaxAngle):
        angle = servoMaxAngle
    elif (angle < -servoMaxAngle):
        angle = -servoMaxAngle
    #convert turn angle to duty cycle 
    turnDutyCycle = servoCenterDutyCycle + angle*servoRatio 
    servo.ChangeDutyCycle(turnDutyCycle)
    return

def isBut1():
    if not GPIO.input(Pin_BUT1):
        setBuzzer(1)
        sleep(0.15)
        setBuzzer(0)
        return 1
    return 0

def isBut2():
    if not GPIO.input(Pin_BUT2):
        setBuzzer(1)
        sleep(0.15)
        setBuzzer(0)
        return 1
    return 0

def isBut3():
    if not GPIO.input(Pin_BUT3):
        setBuzzer(1)
        sleep(0.15)
        setBuzzer(0)
        return 1
    return 0

def setAllDeviceToZero():
    setSpeed(0)
    setTurn(0)
    setLED1(0)
    setLED2(0)
    setLED3(0)
    setBuzzer(0)
    setHeadlight(0) 
    return 0

# Calculate Angle
def GetAngle(x, xshape = 160):
    value = math.atan2((x-xshape), y)
    result = value * 180 / math.pi
    result = result * factor
    new_result = (result / 30) * 2
    return result

# Calculate Speed
def GetSpeed(angle):
    speed = (abs(angle) / 45) * (100 - minsp)
    return speed

setAllDeviceToZero()
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(1) #delay for hardware setup
