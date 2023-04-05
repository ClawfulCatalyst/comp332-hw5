#!/usr/bin/python3
#
# COMP 332, Spring 2023
# Chat client
# Katelyn McCall
#
# Example usage:
#
#   python3 chat_client.py <chat_host> <chat_port>
#

import socket
import sys
import threading


class ChatClient:

    def __init__(self, chat_host, chat_port):
        self.chat_host = chat_host
        self.chat_port = chat_port
        self.name = ''
        self.start()

    def start(self):

        # Open connection to chat
        try:
            chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            chat_sock.connect((self.chat_host, self.chat_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ",e)
            if chat_sock:
                chat_sock.close()
            sys.exit(1)

        threading.Thread(target=self.read_sock, args=(chat_sock,)).start()
        threading.Thread(target=self.write_sock, args=(chat_sock,)).start()
        
    def make_pkt(self, source, payload):
        lengthSourcePayload = len(source + payload) # find length of source and payload
        length = "0x{:02x}".format(lengthSourcePayload + 6)
        packet = length + source + '//' + payload
        return packet
    
    def write_sock(self, sock):

        # TO DO:

        # In the write sock function you will continuously read data from the command line
        # (i.e., user input), put your protocol header on it, and write it to the chat server. Your
        # protocol header should comprise several fields, including at least the length (in bytes)
        # of the data. You will need some way of determining when the header terminates, and
        # when the data being sent (payload) begins.

        # Fill this out
        
        self.name = input("Enter username: ") + ': '
        while True:
            
            LINE_UP = '\033[1A'
            LINE_CLEAR = '\x1b[2K'

            msg = self.name + input(self.name)
            print(LINE_UP, end=LINE_CLEAR)
            print(msg)

            packet = self.make_pkt(self.chat_host, msg).encode('utf-8')
            sock.sendall(packet)    
        

    def read_sock(self, sock):

        # TO DO:

        # In the read sock function you will continuously read data from the socket with the
        # server, parse the protocol header that the server put on the data it sent, determine
        # how much data to read, read until you get the expected amount of data, and display it
        # (print) to the screen. When you print to the screen, you should format the display so
        # that the name of the user who sent the data comes first, followed by a colon, followed
        # by the data, as in, “user: data”.

        # Fill this out

        while True:
            # receive set size length
            length = sock.recv(4).decode('utf-8')
            if length == '':
                pass
            else:
                length = int(length,16)
                # receive given length of source and payload minus length
                source_and_payload = sock.recv(length).decode('utf-8')
                
                # Separate into values
                spl = source_and_payload.split("//")
                if source_and_payload:
                    print('\u001b[1F' + '\n' + spl[1] + '\n' + self.name, end = '')
            

def main():

    print (sys.argv, len(sys.argv))
    chat_host = 'localhost'
    chat_port = 50007

    if len(sys.argv) > 1:
        chat_host = sys.argv[1]
        chat_port = int(sys.argv[2])

    chat_client = ChatClient(chat_host, chat_port)

if __name__ == '__main__':
    main()
