######################################################################
### Date: 2017/10/5
### file name: project3_student.py
### Purpose: this code has been generated for the three-wheeled moving
###         object to perform the project3 with ultra sensor
###         swing turn, and point turn
### this code is used for the student only
######################################################################

# =======================================================================
# import GPIO library and time module
# =======================================================================
import RPi.GPIO as GPIO
from time import sleep

# =======================================================================
#  set GPIO warnings as false
# =======================================================================
GPIO.setwarnings(False)

# =======================================================================
# import getDistance() method in the ultraModule
# =======================================================================
from ultraModule import getDistance

# =======================================================================
# import TurnModule() method
# =======================================================================
from TurnModule import *


# =======================================================================
# rightPointTurn() and leftPointTurn() in TurnModule module
# =======================================================================
# student assignment (1)
# student assignment (2)



# =======================================================================
# import go_forward_any(), go_backward_any(), stop(), LeftPwm(),
# RightPwm(), pwm_setup(), and pwm_low() methods in the module of go_any
# =======================================================================
from go_any import *

# implement rightmotor(x)  # student assignment (3)
# implement go_forward_any(speed): # student assignment (4)
# implement go_backward_any(speed): # student assignment (5)
# implement go_forward(speed, running_time)  # student assignment (6)
# implement go_backward(speed, running_time)  # student assignment (7)

# =======================================================================
# setup and initilaize the left motor and right motor
# =======================================================================
pwm_setup()

# =======================================================================
#  define your variables and find out each value of variables
#  to perform the project3 with ultra sensor
#  and swing turn
# =======================================================================
dis = 20  # ??
obstacle = 1

# when obstacle=1, the power and
# running time of the first turn
rspeed = 43
lspeed = 39
turn_speed = 30
rswing = 1.01288986206
rpoint = 0.686996936798
lswing = 0.4533599663
lpoint = 0.25910313606
flag = True
try:
    while True:
        # ultra sensor replies the distance back
        objdis = getDistance()
        print('objdis= ', objdis)

        # when the objdis is above the dis, moving object forwards
        if (objdis > dis):
            go_forward_any_alignment(rspeed, lspeed)
            print('obstacle=', obstacle)

        # when the distance is below the dis, moving object stops
        else:
            # stop and wait 1 second
            stop()
            sleep(1.5)
            if flag:
                print("swingTurn")
                leftPointTurn(turn_speed, lpoint)
                #rightSwingTurn(turn_speed, rswing) 
                flag = False
                sleep(0.5)
            else:
                #rightPointTurn(turn_speed, rpoint)
                flag = True
                leftSwingTurn(40, lswing) 
                sleep(0.5)


            ########################################################
            ### please continue the code or change the above code
            ### # student assignment (10)
            ########################################################


# when the Ctrl+C key has been pressed,
# the moving object will be stopped

except KeyboardInterrupt:
    pwm_low()
