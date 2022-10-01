from time import sleep
from machine import Pin, PWM, UART
import utime
import _thread

pwm1 = PWM(Pin(6))
pwm1.freq(50)
pwm2 = PWM(Pin(7))
pwm2.freq(50)
pwm3 = PWM(Pin(8))
pwm3.freq(50)
pwm4 = PWM(Pin(9))
pwm4.freq(50)
flag = True
uart = UART(0, 115200)
# low = 20000
# pwm.duty_u16(0)
# pwm.duty_u16(20000)
# while True:
#     pwm.duty_u16(low)
    



def calibrate(pwm):
    t = utime.ticks_ms()
    timeout = 3000
    
    while (utime.ticks_ms() - t) < timeout:
        pwm.duty_u16(16530)#17530
    
    pwm.duty_u16(0)    

def run(pwm, accel):
#     low = 17530
#     test = 0
#     while True:
#         test += 100
#         sleep(1)
#         pwm.duty_u16(low + test)
#         if test == 500:
#             pwm.duty_u16(0)
#             break
    pwm.duty_u16(accel)

def calibrateAll():
    calibrate(pwm1)
    calibrate(pwm2)
    calibrate(pwm3)
    calibrate(pwm4)

def stopAll():
    flag = False
    print("im here")
    run(pwm1, 0)
    run(pwm2, 0)
    run(pwm3, 0)
    run(pwm4, 0)

def runAll():
    low = 18530
    test = 18530
    run(pwm1, test)
    run(pwm2, test)
    run(pwm3, test)
    run(pwm4, test)
#     while True:
#         test += 50
#         
#         run(pwm1, test)
#         run(pwm2, test)
#         run(pwm3, test)
#         run(pwm4, test)
#         
#         if test == low + (3 * 50):
#             pwm1.duty_u16(0)
#             pwm2.duty_u16(0)
#             pwm3.duty_u16(0)
#             pwm4.duty_u16(0)
#             break
        
