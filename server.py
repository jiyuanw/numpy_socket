from my_socket import server

def process_frame(small_frame):
    print('received frame')

server.startServer(process_frame)
