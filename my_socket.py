import socket, time
import numpy as np
from io import BytesIO
import cv2

SPLT = b'---||'

class server():
    def __init__(self):
        pass
    @staticmethod
    def startServer(callback):
        port=7555
        server_socket=socket.socket() 
        server_socket.bind(('',port))
        server_socket.listen(1)
        print('waiting for a connection...')
        cnt = 0
        while True:
            try:
                client_connection,client_address=server_socket.accept()
                print('connected to ',client_address[0])
                ultimate_buffer=b''
                cnt = (cnt + 1 ) % 30

                while True:
                    receiving_buffer = client_connection.recv(1024)
                    if not receiving_buffer: break
                    if SPLT in receiving_buffer:
                        arr = receiving_buffer.split(SPLT)
                        ultimate_buffer += arr[0]
                        final_image=np.load(BytesIO(ultimate_buffer))['frame']
                        callback(final_image)                        
                        ultimate_buffer = arr[1]
                    else: 
                        ultimate_buffer += receiving_buffer

                final_image=np.load(BytesIO(ultimate_buffer))['frame']

                cv2.imshow('frame', final_image)
                cv2.waitKey(50)
                client_connection.close()
            except Exception as e:
                print(e)
        server_socket.close()
        print('\nframe received')
        return final_image

class client():
    def __init__(self, server_address = '127.0.0.1', port = 7555):
        self.server_address = server_address
        self.port = port
        self.client_socket = socket.socket()
    def connect(self):
        try:
            self.client_socket.connect((self.server_address, self.port))
            print('Connected to %s on port %s' % (self.server_address, self.port))
        except socket.error as e:
            print('Connection to %s on port %s failed: %s' % (self.server_address, self.port, e))
        return self
    def send(self, image):
        if not isinstance(image,np.ndarray):
            print('not a valid numpy image')
            return
        f = BytesIO()
        np.savez_compressed(f,frame=image)
        # np.savez(f,frame=image)
        f.seek(0)
        out = f.read()
        self.client_socket.sendall(out)
        self.client_socket.sendall(SPLT)
    def disconnect(self):
        client_socket.shutdown(1)
        client_socket.close() 