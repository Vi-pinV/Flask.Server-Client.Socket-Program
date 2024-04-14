import socket,time
ip_address = '127.0.0.1'
port_number = 12345

cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.connect((ip_address,port_number))

msg = input("Enter msg to send : ")

while msg!='quit':
    #time.sleep(1)
    cs.send(msg.encode())
    #time.sleep(1)
    msg = cs.recv(1024).decode()
    #time.sleep(1)
    print(msg)
    msg = input("Enter msg to send :")

#if __name__ == '__main__':

cs.close()
