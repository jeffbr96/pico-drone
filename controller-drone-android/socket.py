import machine
import utime,time
import _thread
import utime
from time import sleep
import esc as sc

SSID='AI-THINKER_E2895A'
password = ''
ServerIP = '192.168.4.2'
Port = '10000'

uart = machine.UART(0, 115200)
splock = _thread.allocate_lock()

def sendCMD(cmd,ack,timeout=2000):
    uart.write(cmd+'\r\n')
    t = utime.ticks_ms()
    while (utime.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode()
            print(s)
            
            if(s.find(ack) >= 0):
                return True
    return False


def connect():
    
    uart.write('+++')
    time.sleep(1)
    if(uart.any()>0):uart.read()
    sendCMD("AT","OK")
    sendCMD("AT+CWMODE=3","OK")
    sendCMD("AT+CWJAP=\""+SSID+"\",\""+password+"\"","OK",20000)
    sendCMD("AT+CIFSR","OK")
    sendCMD("AT+CIPSTART=\"TCP\",\""+ServerIP+"\","+Port,"OK",10000)
    sendCMD("AT+CIPMODE=1","OK")
    sendCMD("AT+CIPSEND",">")

    uart.write(' ESP8266 TCP Client\r\n')
    while True:
        splock.acquire()
        talk()
        splock.release()

def talk():
    s=uart.read()
    
    if(s != None):
        s = s.decode()
        print('receiving')
        print(s)
        if (s == 'temp'):
            t = "Hello!!"
            uart.write(str(t) +'C \r\n')
        if(s == 'calibrate'):
            sc.calibrateAll() 
            print('successfully calibrated')
        if(s == 'run'):
            sc.runAll()
            print('successfully ran all brushless')
        if(s == "stop"):
            sc.stopAll()
            print('successfuly stoped')