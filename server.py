from os import close
import socket
import flask,time,threading
from flask import Flask,render_template


ip_address = '127.0.0.1'
port_number = 12345

thread_index = 0
THREADS = []
CMD_INPUT = {}
#CMD_OUTPUT = {}
IPS = {}

def close_connection(connection,thread_index):    
    THREADS[thread_index]=''
    IPS[thread_index]=''
    CMD_INPUT[thread_index]=''
    CMD_OUTPUT[thread_index]=''
    connection.close()
app = Flask(__name__)

def handle_connection(connection,address,thread_index):
    
    global CMD_INPUT
    global CMD_OUTPUT
    
    msg = connection.recv(1024).decode()
    CMD_INPUT[thread_index] = msg
    print(msg)
    
    while CMD_INPUT[thread_index] != 'quit' or CMD_INPUT[thread_index]!=" ":
        
        msg = CMD_INPUT[thread_index]
        connection.send(msg.encode())        
        msg = connection.recv(1024).decode()        
        print (msg)
        CMD_INPUT[thread_index]=msg        
        print (CMD_INPUT)
    close_connection(connection,thread_index)

def server_socket():
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    ss.bind((ip_address,port_number))    
    ss.listen(5)    
    global THREADS
    global IPS
    
    while True:
        connection,address = ss.accept()        
        thread_index = len(THREADS)        
        t = threading.Thread(target=handle_connection,args=(connection,address,len(THREADS)))
        THREADS.append(t)
        IPS[thread_index]=address          
        print(f"IPSConnected to {IPS}")               
        t.start()  

def create_app():  
       
    server_thread = threading.Thread(target=server_socket)   
    server_thread.start()
    
    @app.route("/agents")
    def agents():
        global THREADS
        global IPS
        return render_template('agents.html',ips=IPS)
        
    @app.route("/")
    def index():
        return render_template('index.html')
    return app

if __name__ == '__main__':   
    app = create_app() 
    app.run(IPS)
    