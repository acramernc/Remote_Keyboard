#This program accepts keyboard inputs from a remote pc via a socket connection

import socket, threading, time
import keyboard

print("Welcome to KeyServer, Made by Adam Cramer\n")
#this IP is not necessarily accurate
hostName = socket.gethostname()
myIP = socket.gethostbyname(hostName)
print("Your ip is ", myIP)

#port to wait for a connection on
port = 25565
alive = True

#this method is to recieve remote inputs and translate them to local inputs
def rcv():
    global alive
    #setup the socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as r:
        r.bind(('', port))
        r.listen()
        #when someone tries to connect, accept the connection
        conn, addr = r.accept()
        #maintain the connection and accept data from remote
        with conn:
            print('\nConnected by', addr)
            while True:
                try:
                    data = conn.recv(1024)
                except(Exception):
                    # in case of crash, make sure no keys are held down, this prevents a stuck modifier key
                    keyboard.restore_state([])
                    break

                if not data: break
                rmsg = data.decode('utf-8')

                #keypresses are seperated by a cairrage return
                msglist = rmsg.split("\r")

                #print(msglist)
                for m in msglist:
                    #prevent crash in case of empty string from end of split
                    if m == "":
                        continue
                    #seperate the direction (dir) and the keypress (key)
                    (dir, key) = m.split("\a")
                    if dir == "down":
                        #press down the key (set to lowercase to prevent double uppercase issues)
                        keyboard.press(key.lower())
                    else:
                        keyboard.release(key.lower())

                if not alive:
                    #another failsafe
                    keyboard.restore_state([])
                    break
            print("The other client has disconnected")
            alive = False
            keyboard.restore_state([])

#keeps threads alive until we dont need them
def dummy():
    while alive:
        time.sleep(.2)

#setup threads
dThread = threading.Thread(target=dummy) #dummy thread
rThread = threading.Thread(target=rcv, daemon = True) #recieving thread

#start our threads
dThread.start()
rThread.start()

