import RPi.GPIO as GPIO
from time import time, sleep, clock
from ultraModule import getDistance
from TurnModule import *
from go_any import *

#kturn_list = [rightSwingTurn_alignment, rightPointTurn_alignment, 
#        leftSwingTurn_alignment, leftPointTurn_alignment]
kturn_list = [leftPointTurn_alignment, leftSwingTurn_alignment]
dturn_speed = 40
dis = 20  # ??
obstacle = 1
rspeed = 43
lspeed = 39

def alignment_front():
    right_speed = 43
    left_speed = 39

    go_forward_any_alignment(right_speed, left_speed)
    while True:
        command = raw_input("turn : ")
        if command == "a":
            left_speed -= 1
        elif command == "d":
            right_speed -= 1
        elif command == "q":
            break
        go_forward_any_alignment(right_speed, left_speed)
    stop()
    print("right : {} ,   left : {}".format(right_speed, left_speed))

def run_turn(turn, dturn_speed):
    # ultra sensor replies the distance back
    while True:
        objdis = getDistance()
        print('objdis= ', objdis)

        # when the objdis is above the dis, moving object forwards
        if (objdis > dis):
            go_forward_any_alignment(rspeed, lspeed)
            print('obstacle=', obstacle)

        # when the distance is below the dis, moving object stops
        else:
            stop()
            sleep(1.5)
            turn(dturn_speed)
            start_time = time.time()
            raw_input()
            stop()
            end_time = time.time()
            print(turn.__name__ , " : {}".format(end_time-start_time))
            break

def alignment_turns():
    for turn in kturn_list:
        while True:
            run_turn(turn, dturn_speed)
            want = raw_input("next? y or n :")
            if want == "y":
                break

if __name__ == "__main__":
    try:
        GPIO.setwarnings(False)
        pwm_setup()
        alignment_front()
        raw_input("turn checking")
        alignment_turns()
        pwm_low()

    except KeyboardInterrupt:
        pwm_low()
