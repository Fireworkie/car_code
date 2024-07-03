from compass import main_loop
import time
import json
import socket

data_stop={
    'command':'stop'
}

data_left={
    'command':'turn_left'
}
json_data_stop = json.dumps(data_stop).encode('utf-8')
json_data_left = json.dumps(data_left).encode('utf-8')

def stop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8001))
    sock.sendall(json_data_stop)
    sock.close()

def left():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8001))
    sock.sendall(json_data_left)
    sock.close()

result = main_loop()
while (not(result>=100 and result<=120)):
    left()
    time.sleep(0.5)
    result = main_loop()
stop()