import network #import required module
import socket

ssid = 'PicoW'
password = '123456789'

wlan = network.WLAN(network.AP_IF) #initialize the wlan object
wlan.config(essid=ssid)
wlan.active(True) #activates the wlan interface
wlan.connect(ssid)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    sleep(1)
ip = wlan.ifconfig()[0]
print(f'Connected on {ip}')
print(ip)

while wlan.active == False:
    pass
print("access point active")
print(wlan.ifconfig())

# accessPoints = wlan.scan() #perform a WiFi Access Points scan
# for ap in accessPoints: #this loop prints each AP found in a single row on shell
#     print(ap)
def open_socket(ip):
    # Open a socket
    address = (ip, 10000)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    while True:
        conn, addr = connection.accept()
        from_client = ''
        while True:
            data = conn.recv(4096).decode()
            print(data)
            if not data: break
            from_client += data
            print(from_client)
            conn.send("I am SERVER")
        conn.close()
        print('client disconnected')
    return connection
open_socket(ip)
