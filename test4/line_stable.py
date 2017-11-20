import RPi.GPIO as GPIO
from go_any import *
from ultraModule import *
import time
from functools import reduce

# =======================================================================
#  set GPIO warnings as :false
# =======================================================================
GPIO.setwarnings(False)

# =======================================================================
# set up GPIO mode as BOARD
# =======================================================================
GPIO.setmode(GPIO.BOARD)
    

pwm_setup()

# =======================================================================
# declare the pins of 16, 18, 22, 40, 32 in the Rapberry Pi
# as the control pins of 5-way trackinmg sensor in order to
# control direction
# 
#  leftmostled    leftlessled     centerled     rightlessled     rightmostled
#       16            18              22             40              32
#
# led turns on (1) : trackinmg sensor led detects white playground
# led turns off(0) : trackinmg sensor led detects black line

# leftmostled off : it means that moving object finds black line
#                   at the position of leftmostled
#                   black line locates below the leftmostled of the moving object
#
# leftlessled off : it means that moving object finds black line
#                   at the position of leftlessled
#                   black line locates below the leftlessled of the moving object
# 
# centerled off : it means that moving object finds black line
#                   at the position of centerled
#                   black line locates below the centerled of the moving object
# 
# rightlessled off : it means that moving object finds black line
#                   at the position of rightlessled
#                   black line locates below the rightlessled  of the moving object
# 
# rightmostled off : it means that moving object finds black line
#                   at the position of rightmostled
#                   black line locates below the rightmostled of the moving object
# =======================================================================

leftmostled=16
leftlessled=18
centerled=22
rightlessled=40
rightmostled=32

GPIO.setup(leftmostled, GPIO.IN)
GPIO.setup(leftlessled, GPIO.IN)
GPIO.setup(centerled,   GPIO.IN)
GPIO.setup(rightlessled, GPIO.IN)
GPIO.setup(rightmostled, GPIO.IN)



# =======================================================================
# GPIO.input(leftmostled) method gives the data obtained from leftmostled
# leftmostled returns (1) : leftmostled detects white playground
# leftmostled returns (0) : leftmostled detects black line
#
#
# GPIO.input(leftlessled) method gives the data obtained from leftlessled
# leftlessled returns (1) : leftlessled detects white playground
# leftlessled returns (0) : leftlessled detects black line
#
# GPIO.input(centerled) method gives the data obtained from centerled
# centerled returns (1) : centerled detects white playground
# centerled returns (0) : centerled detects black line
#
# GPIO.input(rightlessled) method gives the data obtained from rightlessled
# rightlessled returns (1) : rightlessled detects white playground
# rightlessled returns (0) : rightlessled detects black line
#
# GPIO.input(rightmostled) method gives the data obtained from rightmostled
# rightmostled returns (1) : rightmostled detects white playground
# rightmostled returns (0) : rightmostled detects black line
#
# =======================================================================

sensor_weight = [-9, -2, 0,2, 9]
last_error = 0
error_sum = 0
dt = 0.02
def calculatePower():
    left = 50
    right = 50
    kp, kd, ki = 8, 22, 0.4
    global last_error, error_sum
    signal_list = get_tracksensor()


    error = 0
    sensor_cnt = 0
    flag = False
    for idx in range(len(sensor_weight)):
        if signal_list[idx]:
            sensor_cnt += 1
            flag = flag or True
            error += sensor_weight[idx]
            
    error = error / sensor_cnt
    pv = 0
    if not flag:
        print("return to coruse")
        pv = kp * last_error
    else:
        error_sum += error * dt
        pv = kp * error + kd * (error - last_error) + ki * error_sum
        last_error = error

    if pv > 40:
        pv = 40
    if pv < -40:
        pv = -40

    if pv < 0:
        left += pv
        right -= pv
    elif pv >= 0:
        left += pv
        right -= pv

    return (right, left)

def Avoiding():
    while  is_on_track():
        go_forward_any_alignment(10, 90)
        sleep(0.2)
    go_forward_any_alignment(50, 50)
    sleep(0.6)
    while not  is_on_track():
        print("are you?")
        go_forward_any_alignment(70, 10)
        sleep(0.2)

def get_tracksensor():
    ret = [GPIO.input(leftmostled), GPIO.input(leftlessled), GPIO.input(centerled), GPIO.input(rightlessled), GPIO.input(rightmostled)]
    return list(map(lambda x : not x, ret))

def is_on_track():
    ret = get_tracksensor()
    result = reduce(lambda a, b: a or b, ret, False)
    return result

if __name__ == "__main__":
    dist = 30
#    dist = 0
    count = 0
    try:
        while True:
            if count % 4 == 0:
                if dist > getDistance():
                    print("avoid!!!")
                    Avoiding()
                    count = 0

            right, left = calculatePower()
            count += 1
            print(right, left)
#right, eft
            go_forward_any_alignment(right, left)
            sleep(0.02)

    except KeyboardInterrupt:
        pwm_low()
    finally:
        pwm_low()

