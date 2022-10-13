import machine
from machine import Pin, Timer
import socket

def blink():
    intled = machine.Pin("LED", machine.Pin.OUT)
    tim = Timer()
    def tick(timer):
        intled.toggle()
        
    tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)

def server():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(('192.168.4.1',10000))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        from_client = ''
        while True:
            data = conn.recv(4096).decode()
            if not data: break
            from_client += data
            print(from_client)
            if from_client == 'blink':
                blink()
            conn.send("I am SERVER")
        conn.close()
        print('client disconnected')
