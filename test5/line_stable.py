import RPi.GPIO as GPIO
from go_any import *
import time
import sys
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
avoid_flag = False

intersection_case = [[1,1,1,1,1], [0,0,1,1,1], [1,1,1,0,0], [0,1,1,1,1], [1,1,1,1,0]]
intersection_next_case = [[0,0,0,0,0], [0,0,1,0,0]]
intersection_direction = [(0, 0, "r"), (0, 1, "r"), (1, 0, "r"), (1,1,"r"), 
        (2, 0, "l"), (2, 1, "f"), (3, 0, "r"),(3, 1, "r"), (4, 0, "l"), (4, 1, "f")]

def calculatePower():
    left = 50
    right = 50
    turn_left = 50
    turn_right = 50
    kp, kd, ki = 12, 15, 0.4
    global last_error, error_sum
    signal_list = get_tracksensor()
    print(signal_list)

    direction = is_intersection(signal_list)
    if direction != "":
        print("way to go : " + str(direction))
        if direction != "f":
            doing_turn(direction)

    error = 0
    sensor_cnt = 0
    flag = False
    for idx in range(len(sensor_weight)):
        if signal_list[idx]:
            sensor_cnt += 1
            flag = flag or True
            error += sensor_weight[idx]
    if sensor_cnt == 2:
        error = error/2

    pv = 0
    error_derive = 0
    if not flag and error == 0:
        print('uturn')
        doing_turn('u')
        return -1, -1
    elif not flag:
        print("return to coruse")
        pv = kp * last_error
    else:
        error_sum += error * dt
        error_derive = error - last_error
        pv = kp * error + kd * error_derive + ki * error_sum
        last_error = error
    print("error_derive : ", error_derive)

    if pv > 50:
        pv = 50
    if pv < -50:
        pv = -50

    if pv < 0:
        left += pv
        right -= pv
    elif pv >= 0:
        left += pv
        right -= pv

    return (right, left)

def get_tracksensor():
    center = GPIO.input(centerled)
    rl = GPIO.input(rightlessled)
    ll = GPIO.input(leftlessled)
    rm = GPIO.input(rightmostled)
    lm = GPIO.input(leftmostled)
    ret = [lm, ll, center, rl, rm]
    return list(map(lambda x : not x, ret))

def is_on_track():
    ret = get_tracksensor()
    result = reduce(lambda a, b: a or b, ret, False)
    return result

def is_almost_lcenter():
    ret = get_tracksensor()
    ret = ret[2:4]
    print("center : ", ret)
    result = reduce(lambda a, b: a or b, ret, False)
    return result

def is_almost_rcenter():
    ret = get_tracksensor()
    ret = ret[1:3]
    print("center : ", ret)
    result = reduce(lambda a, b: a or b, ret, False)
    return result

def is_on_center():
    ret = get_tracksensor()
    flag = ret[0] or ret[1] or ret[3] or ret[4]
    return ret[2]

def is_intersection(sensor):
    if sensor in intersection_case:
        last_idx = intersection_case.index(sensor)
        print('intersection! : ', sensor)
        sleep(0.1)
        sensor = get_tracksensor()
        print('next intersection! : ', sensor)
        if True in sensor[1:4]:
            print(sensor)
            sensor = [0,0,1,0,0]
            print("changed")
        print('next intersection! : ', sensor)
        if sensor in intersection_next_case:
            next_idx = intersection_next_case.index(sensor)
            for direction in intersection_direction:
                ldx, ndx = direction[0], direction[1]
                if ldx == last_idx and next_idx == ndx:
                    return direction[2]
        else:
            print("no way")
            return ""
    else:
        return ""
def doing_turn(direction):
    right, left = 0, 0
    if direction == "r":
        stop()
        sleep(0.3)
        left = 45
        while is_on_track():
            go_ruturn(30)
            sleep(0.05)
        while not is_almost_rcenter():
            go_ruturn(30)
            sleep(0.05)
        stop()
        sleep(0.3)
        while not is_on_center():
            go_luturn(25)
            sleep(0.05)
    elif direction == "l":
        stop()
        sleep(0.3)
        right = 40
        while is_on_track():
            go_luturn(40)
            sleep(0.05)
        while not is_almost_lcenter():
            go_luturn(40)
            sleep(0.05)
        stop()
        sleep(0.3)
        while not is_on_center():
            go_ruturn(25)
            sleep(0.05)
    elif direction == "u":
        sleep(0.3)
        stop()
        sleep(0.3)
        while not is_almost_rcenter():
            go_ruturn(30)
            sleep(0.05)
        stop()
        sleep(0.3)
        while not is_on_center():
            go_luturn(30)
            sleep(0.05)
        stop()
        sleep(0.3)
        return

    print("fuck turn")
    stop()
    sleep(0.1)


def is_finishline(sensor):
    n = 0
    for s in sensor:
        if s:
            n += 1
    return n>= 4

if __name__ == "__main__":
    try:
        while True:
            right, left = calculatePower()
            if right== 0 and left == 0:
                stop()
                break
            elif right == -1 and left == -1:
                continue
            print(right, left)
#right, eft
            go_forward_any_alignment(right, left)
            sleep(0.05)

    except KeyboardInterrupt:
        pwm_low()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    finally:
        pwm_low()

