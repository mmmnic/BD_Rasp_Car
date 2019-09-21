import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define
servoFre = 50
motorFre = 500
servoCenterDutyCle = 7.5
servoMaxDutyCycle = 10.5
servoMaxAngle = 45
servoRatio  = (servoMaxDutyCycle - servoCenterDutyCle)/servoMaxAngle
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

#Setup pin
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
GPIO.setup(3, GPIO.OUT)

#Setup for motor and servo
motor = GPIO.PWM(Pin_MOTOR, motorFre)
servo = GPIO.PWM(Pin_SERVO, servoFre)
testPWM = GPIO.PWM(3, 60)
motor.start(0)
servo.start(0)
testPWM.start(0)

GPIO.output(Pin_LED1, GPIO.HIGH)
GPIO.output(Pin_LED2, GPIO.HIGH)
GPIO.output(Pin_LED3, GPIO.HIGH)
GPIO.output(Pin_BUZZER, GPIO.HIGH)
GPIO.output(Pin_HEADLIGHT, GPIO.LOW)

def LED1_on(Status):
    GPIO.output(Pin_LED1, not(Status))
    return;

def LED2_on(Status):
    GPIO.output(Pin_LED2, not(Status))
    return;

def LED3_on(Status):
    GPIO.output(Pin_LED3, not(Status))
    return;

def Buzzer_on(Status):
    GPIO.output(Pin_BUZZER, not(Status))
    return;

def isBut1():
    if not GPIO.input(Pin_BUT1):
        sleep(0.2)
        return 1;
    return 0;

def isBut2():
    if not GPIO.input(Pin_BUT2):
        sleep(0.2)
        return 1;
    return 0;

def isBut3():
    if not GPIO.input(Pin_BUT3):
        sleep(0.2)
        return 1;
    return 0;
    