#!/usr/bin/python3
#
# COMP 332, Spring 2023
# Chat server
# Katelyn McCall
#
# Usage:
#   python3 chat_server.py <host> <port>
#

import socket
import sys
import threading

class ChatProxy():

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1
        self.chat_list = {}
        self.chat_id = 0
        self.lock = threading.Lock()
        self.start()


    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
        except OSError as e:
            print ("Unable to open server socket")
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for user connection
        while True:
            conn, addr = server_sock.accept()
            self.add_user(conn, addr)
            thread = threading.Thread(target = self.serve_user,
                    args = (conn, addr, self.chat_id))
            thread.start()

    def add_user(self, conn, addr):
        self.chat_id = self.chat_id + 1
        print ('User ' + str(self.chat_id) + ' has connected', addr) 
        self.lock.acquire()
        self.chat_list[self.chat_id] = (conn, addr)
        self.lock.release()


    def read_data(self, conn):

        # receive set size length
        length = conn.recv(4).decode('utf-8')

        if length == '':
            
            return '&&&&'

        length = int(length,16)
        
        # receive given length of source and payload minus length
        source_and_payload = conn.recv(length).decode('utf-8')
        
        # Separate into values
        spl = source_and_payload.split("//")
        source = spl[0]
        data = spl[1]

        # Remove all instances of \ to avoid issue with ANSI escape codes
        data = data.replace('\\', '')

        # search chat_list for the id corresponding to this connection
        for i,val in self.chat_list.items():
            if val[0] == conn:
                addr = val[1]
        

        
        return data

    def send_data(self, user, data):

        # TO DO:

        # In the send data function you will loop through all of the available connections and 
        # send the message to every other client, excepting the original sending client.
        


        self.lock.acquire()

        packet = self.make_pkt(self.server_host, data).encode('utf-8')

        for i,val in self.chat_list.items():
            if not val[0] == user:
                val[0].sendall(packet)

        self.lock.release()

    def make_pkt(self, source, payload):
        lengthSourcePayload = len(source + payload) # find length of source and payload
        length = "0x{:02x}".format(lengthSourcePayload + 6)
        packet = length + source + '//' + payload
        return packet
    
    def cleanup(self, conn):

        # TO DO:

        # in the cleanup function you will close the socket being served in the thread as well as
        # remove the connection from the list of connections available

        self.lock.acquire()

        # Fill this out
        for i,val in self.chat_list.items():
            if val[0] == conn:
                del self.chat_list[i]
                break
        
        conn.close()

        self.lock.release()

    def serve_user(self, conn, addr, user):
        
        # TO DO: 

        # In the serve user function you will use the read data function to continuously read
        # data from the socket (i.e., chat client) being served in that thread. Whenever you
        # have read a complete message you will send it to all other clients using the send data
        # function. Note: you should not access the chat list variable in this function.


        # Fill this out
        print("In serve user")
        
        while True:
            
            msg = self.read_data(conn)
            if msg: 
                
                if msg == '&&&&':
                    self.cleanup(conn)
                    print(str(addr) + ' has disconnected.')
                    return None

                print(msg)
                self.send_data(conn, msg)
            

def main():

    print (sys.argv, len(sys.argv))
    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    chat_server = ChatProxy(server_host, server_port)

if __name__ == '__main__':
    main()
