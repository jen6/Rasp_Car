######################################################################
### Date: 2017/10/5
### file name: ultra.py
### Purpose: this code has generated for the return
###         the distance between the moving object and obstacle
###         ultra sensor
### this code is used for the student only
######################################################################


import RPi.GPIO as GPIO # import GPIO librery
import time

GPIO.setmode(GPIO.BOARD)

trig=33
echo=31

#ultrasonic sensor setting
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

def getDistance():
    GPIO.output(trig,False)
    time.sleep(0.03)
    GPIO.output(trig,True)
    time.sleep(0.00001)
    GPIO.output(trig,False)
    while GPIO.input(echo)==0:
        pulse_start=time.time()
    while GPIO.input(echo)==1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17000
    distance=round(distance,2)
    return distance

if __name__ == "__main__":
    while True:
        print(getDistance())
